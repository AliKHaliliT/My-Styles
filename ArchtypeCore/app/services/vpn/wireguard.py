import asyncio
import logging
import textwrap
from typing import Any

from app.core.config.settings import Settings
from app.domain.interfaces.vpn import IVPNProvider


class WireGuardProvider(IVPNProvider):

    """

    WireGuard implementation of the IVPNProvider interface.


    Usage
    -----
    This class provides methods for managing WireGuard peers, including credential generation, provisioning, revocation, and configuration retrieval.
    It executes WireGuard commands asynchronously and parses their output to perform the necessary operations.
    ```python
    from app.services.vpn import WireGuardProvider
    from app.core.config.settings import Settings

    settings = Settings()
    wg_provider = WireGuardProvider(settings)

    # Validate interface
    await wg_provider.validate_interface()
    # Generate credentials
    pubkey, protocol_data = await wg_provider.generate_credentials()
    # Provision client
    await wg_provider.provision_client(client_identifier=pubkey, ip_address="10.0.0.2")
    # Get client config
    config = await wg_provider.get_client_config(client_identifier=pubkey, ip_address="10.0.0.2")
    print(config)
    # Revoke client    
    await wg_provider.revoke_client(client_identifier=pubkey)
    ```

    """

    def __init__(self, settings: Settings) -> None:

        """

        Constructor for the WireGuardProvider.


        Parameters
        ----------
        settings : Settings
            The application settings.


        Returns
        -------
        None.

        """

        if not isinstance(settings, Settings):
            raise TypeError(f"settings must be a Settings. Received: {settings} with type {type(settings)}")


        self.interface = settings.WG_INTERFACE
        self.wg_show_path = settings.WG_SHOW_PATH
        self.wg_quick_path = settings.WG_QUICK_PATH
        self.server_ip = settings.SERVER_IP
        self.server_pubkey = settings.SERVER_PUBKEY
        self.logger = logging.getLogger(__name__)


    async def _run_command(self, command: list[str], input_text: str | None = None) -> str:

        """

        Executes a shell command asynchronously and captures its output.

        
        Parameters
        ----------
        command : list[str]
            A list of strings representing the command and its arguments.

        input_text : str | None
            Optional text to be passed to the command's stdin.


        Returns
        -------
        str
            The stripped stdout from the command.

        """

        if not isinstance(command, list):
            raise TypeError(f"command must be a list. Received: {command} with type {type(command)}")


        proc = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE if input_text else None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(input_text.encode() if input_text else None), timeout=30
        )
        
        if proc.returncode != 0:
            raise RuntimeError(f"Command failed: {stderr.decode().strip()}")
            
        return stdout.decode().strip()


    async def validate_interface(self) -> None:

        """

        Validates that the configured WireGuard interface is accessible.

        """

        await self._run_command([self.wg_show_path, "show", self.interface])


    async def generate_credentials(self) -> tuple[str, dict[str, Any]]:

        """

        Generates a new WireGuard private and public key pair.

        
        Returns
        -------
        tuple[str, dict[str, Any]]
            A tuple containing the client_identifier (pubkey) and protocol_data (privkey).

        """

        privkey = await self._run_command([self.wg_show_path, "genkey"])
        pubkey = await self._run_command([self.wg_show_path, "pubkey"], input_text=privkey)
        
        protocol_data = {"privkey": privkey}
        
        return pubkey, protocol_data


    async def provision_client(self, client_identifier: str, ip_address: str | None, protocol_data: dict[str, Any]) -> None:

        """

        Adds a new peer to the WireGuard interface.


        Parameters
        ----------
        client_identifier : str
            The public key of the peer.

        ip_address : str | None
            The IP address the peer is allowed to use.

        protocol_data : dict[str, Any]
            Protocol specific parameters.

        """

        if not isinstance(client_identifier, str):
            raise TypeError(f"client_identifier must be a str. Received: {client_identifier} with type {type(client_identifier)}")
        if not isinstance(ip_address, str):
            raise TypeError(f"ip_address must be a str. Received: {ip_address} with type {type(ip_address)}")


        command =[self.wg_show_path, "set", self.interface, "peer", client_identifier, "allowed-ips", f"{ip_address}/32"]
        await self._run_command(command)


    async def revoke_client(self, client_identifier: str, protocol_data: dict[str, Any]) -> None:

        """

        Removes a peer from the WireGuard interface.


        Parameters
        ----------
        client_identifier : str
            The public key of the peer.

        protocol_data : dict[str, Any]
            Protocol specific parameters.

        """

        if not isinstance(client_identifier, str):
            raise TypeError(f"client_identifier must be a str. Received: {client_identifier} with type {type(client_identifier)}")


        command =[self.wg_show_path, "set", self.interface, "peer", client_identifier, "remove"]
        await self._run_command(command)


    async def get_client_config(self, client_identifier: str, ip_address: str | None, protocol_data: dict[str, Any]) -> str:

        """

        Generates a WireGuard client configuration file.


        Parameters
        ----------
        client_identifier : str
            The public key of the peer.

        ip_address : str | None
            The IP address of the peer.

        protocol_data : dict[str, Any]
            Protocol specific parameters (must contain privkey).


        Returns
        -------
        str
            The configuration file content.

        """

        if not isinstance(client_identifier, str):
            raise TypeError(f"client_identifier must be a str. Received: {client_identifier} with type {type(client_identifier)}")
        if not isinstance(protocol_data, dict):
            raise TypeError(f"protocol_data must be a dict. Received: {protocol_data} with type {type(protocol_data)}")


        privkey = protocol_data.get("privkey")
        
        return textwrap.dedent(f"""
            [Interface]
            PrivateKey = {privkey}
            Address = {ip_address}/32
            DNS = 1.1.1.1

            [Peer]
            PublicKey = {self.server_pubkey}
            Endpoint = {self.server_ip}:51820
            AllowedIPs = 0.0.0.0/0, ::/0
        """).strip()


    async def get_usage_stats(self) -> dict[str, int]:

        """

        Retrieves the total data transfer (up + down) for each peer.


        Returns
        -------
        dict[str, int]
            A dictionary mapping each peer's public key to its total data transfer in bytes.

        """

        output = await self._run_command([self.wg_show_path, "show", self.interface, "transfer"])
        stats = {}
        
        for line in output.splitlines():
            parts = line.strip().split("\t")
            if len(parts) == 3:
                stats[parts[0]] = int(parts[1]) + int(parts[2])
                
        return stats


    async def list_peers(self) -> list[str]:

        """

        Lists the public keys of all peers on the WireGuard interface.


        Returns
        -------
        list[str]
            A list of peer public keys.

        """

        command =[self.wg_show_path, "show", self.interface, "peers"]
        output = await self._run_command(command)
        
        peers =[line.strip() for line in output.splitlines() if line.strip()]
        return peers
