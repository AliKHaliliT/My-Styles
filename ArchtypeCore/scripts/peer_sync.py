from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import argparse
import asyncio

from app.core.config.settings import settings
from app.core.security.local_auth import LocalAuthAdapter
from app.repositories.sqlalchemy.uow import SQLAlchemyUnitOfWork
from app.services.vpn.wireguard import WireGuardProvider


async def sync_peers(remove_disabled: bool = True, dry_run: bool = False) -> None:

    """
    
    Sync network peers with the database using UoW and Abstract Providers.
    
    """

    print("🔄 Synchronizing network peers with the database...")
    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    if not remove_disabled:
        print("ℹ️  Removal of disabled peers is disabled")

    auth_manager = LocalAuthAdapter()
    uow = SQLAlchemyUnitOfWork(auth_manager=auth_manager)
    vpn_provider = WireGuardProvider(settings=settings)

    async with uow:
        enabled_devices = await uow.devices.get_enabled_devices_with_enabled_users()
        enabled_identifiers = {device.client_identifier for device in enabled_devices}
        current_peers = set(await vpn_provider.list_peers())

        added_count = 0
        for device in enabled_devices:
            if device.client_identifier not in current_peers:
                
                # Fetch user name for display logging cleanly
                user = await uow.users.get(id=device.user_id)
                username = user.username if user else "unknown"

                if dry_run:
                    print(f"📋 [DRY RUN] Would add peer {device.client_identifier} ({username})")
                else:
                    try:
                        await vpn_provider.provision_client(
                            client_identifier=device.client_identifier, 
                            ip_address=device.ip_address, 
                            protocol_data=device.protocol_data
                        )
                        print(f"✅ Added peer {device.client_identifier} ({username})")
                    except RuntimeError as e:
                        print(f"❌ Failed to add peer {device.client_identifier}: {e}")
                added_count += 1

        removed_count = 0
        if remove_disabled:
            for identifier in current_peers:
                if identifier not in enabled_identifiers:
                    if dry_run:
                        print(f"📋 [DRY RUN] Would remove disabled peer {identifier}")
                    else:
                        try:
                            # Protocol specific context
                            await vpn_provider.revoke_client(client_identifier=identifier, protocol_data={})
                            print(f"✅ Removed disabled peer {identifier}")
                        except RuntimeError as e:
                            print(f"❌ Failed to remove peer {identifier}: {e}")
                    removed_count += 1

    if dry_run:
        print(f"🔍 Dry run complete. Would add: {added_count}, Would remove: {removed_count}")
    else:
        print(f"✅ Peer synchronization complete. Added: {added_count}, Removed: {removed_count}")


def main() -> None:

    """
    
    CLI entrypoint.
    
    """
    
    parser = argparse.ArgumentParser(
        description="Synchronize network peers with database records",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--no-remove", action="store_true", help="Skip removal of disabled peers")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

    args = parser.parse_args()

    if args.verbose:
        print("🔊 Verbose mode enabled")

    try:
        asyncio.run(sync_peers(remove_disabled=not args.no_remove, dry_run=args.dry_run))
    except KeyboardInterrupt:
        print("\n⚠️  Peer synchronization interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during peer synchronization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
