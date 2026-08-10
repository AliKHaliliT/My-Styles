"""One live pass over WireGuardProvider against a real wg interface inside a container.

Run from the repository root with Docker available; the container gets NET_ADMIN, builds a
real WireGuard interface, and drives every subprocess path of the provider against it:

docker run --rm --cap-add NET_ADMIN -v "$PWD:/repo:ro" python:3.14-slim bash -c '
  apt-get update -qq > /dev/null && apt-get install -y -qq wireguard-tools iproute2 > /dev/null
  pip install -q -r /repo/requirements.txt
  SERVER_PRIV=$(wg genkey); export SERVER_PUBKEY=$(echo "$SERVER_PRIV" | wg pubkey)
  ip link add archetype0 type wireguard
  echo "$SERVER_PRIV" > /tmp/sk && wg set archetype0 private-key /tmp/sk listen-port 51820
  ip addr add 10.13.13.1/24 dev archetype0 && ip link set up dev archetype0
  python /repo/scripts/wg_smoke.py'
"""

import asyncio
import os
import sys

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SERVER_IP", "10.13.13.1")
os.environ.setdefault("SECRET_KEY", "container-smoke-secret-key-of-length-32plus")

sys.path.insert(0, "/repo")

from app.core.config.settings import Settings  # noqa: E402
from app.services.vpn.wireguard import WireGuardProvider  # noqa: E402


async def main() -> int:
    """Exercise every subprocess path once and report what actually happened."""
    settings = Settings(SERVER_PUBKEY=os.environ["SERVER_PUBKEY"])
    provider = WireGuardProvider(settings)

    await provider.validate_interface()
    print("PASS validate_interface: the interface answers")

    client_id, protocol_data = await provider.generate_credentials()
    assert client_id and protocol_data.get("privkey"), "credentials came back empty"
    print(f"PASS generate_credentials: pubkey {client_id[:12]}...")

    await provider.provision_client(client_identifier=client_id, ip_address="10.13.13.2", protocol_data=protocol_data)
    print("PASS provision_client: peer added")

    peers = await provider.list_peers()
    assert client_id in peers, f"provisioned peer missing from {peers!r}"
    print(f"PASS list_peers: {len(peers)} peer(s), ours present")

    stats = await provider.get_usage_stats()
    assert client_id in stats, f"peer missing from transfer stats {stats!r}"
    print(f"PASS get_usage_stats: {stats[client_id]} bytes for our peer")

    config = await provider.get_client_config(client_identifier=client_id, ip_address="10.13.13.2", protocol_data=protocol_data)
    assert "[Interface]" in config and "[Peer]" in config, "client config missing sections"
    print("PASS get_client_config: renders Interface and Peer sections")

    await provider.revoke_client(client_identifier=client_id, protocol_data=protocol_data)
    peers_after = await provider.list_peers()
    assert client_id not in peers_after, "peer survived revocation"
    print("PASS revoke_client: peer removed")

    print("\nEvery WireGuardProvider subprocess path ran against a live interface.")
    return 0


sys.exit(asyncio.run(main()))
