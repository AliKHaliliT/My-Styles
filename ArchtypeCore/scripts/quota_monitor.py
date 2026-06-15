from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import argparse
import asyncio
from typing import Any

from app.core.config.settings import settings
from app.core.security.local_auth import LocalAuthAdapter
from app.domain.interfaces.uow import IUnitOfWork
from app.domain.schemas.devices import DeviceUpdate
from app.domain.schemas.users import UserUpdate
from app.repositories.sqlalchemy.uow import SQLAlchemyUnitOfWork
from app.services.vpn.wireguard import WireGuardProvider


async def fetch_all_devices_mapped(uow: IUnitOfWork) -> dict[str, Any]:

    """
    
    Fetch all devices and map them by client_identifier.
    
    """

    devices = await uow.devices.get_multi(limit=10000)
    return {device.client_identifier: device for device in devices}


async def update_user_usage(
    uow: IUnitOfWork,
    device_map: dict[str, Any],
    transfer_data: dict[str, int],
    dry_run: bool = False
) -> set[Any]:
    
    """
    
    Update used_bytes for users based on device transfer data.
    
    """

    updated_users = set()

    for identifier, transferred_bytes in transfer_data.items():
        if (device := device_map.get(identifier)) and transferred_bytes > 0:
            
            user = await uow.users.get(id=device.user_id)
            if not user:
                continue

            if dry_run:
                print(f"📋 [DRY RUN] Would add {transferred_bytes} bytes to user '{user.username}' (device: {identifier[:16]}...)")
            else:
                new_used_bytes = user.used_bytes + transferred_bytes
                await uow.users.update(
                    db_obj=user, 
                    obj_in=UserUpdate(used_bytes=new_used_bytes)
                )
                updated_users.add(user)

    if updated_users and not dry_run:
        await uow.commit()
        print(f"✅ Updated usage for {len(updated_users)} users")

    return updated_users


async def enforce_quotas(
    uow: IUnitOfWork, 
    vpn_provider: WireGuardProvider, 
    dry_run: bool = False
) -> list[Any]:

    """
    
    Disable users who exceeded their quota.
    
    """

    users_to_disable = await uow.users.get_users_over_quota()
    disabled_users =[]

    for user in users_to_disable:
        usage_percent = (user.used_bytes / user.quota_bytes) * 100
        print(f"⚠️  User '{user.username}' exceeded quota ({usage_percent:.1f}% used)")

        if dry_run:
            print(f"📋 [DRY RUN] Would disable user '{user.username}' and their devices")
            disabled_users.append(user)
            continue

        try:
            for device in user.devices:
                await vpn_provider.revoke_client(
                    client_identifier=device.client_identifier, 
                    protocol_data=device.protocol_data
                )
                await uow.devices.update(
                    db_obj=device, 
                    obj_in=DeviceUpdate(status="disabled")
                )
                print(f"✅ Disabled device {device.ip_address} for user '{user.username}'")

            await uow.users.update(
                db_obj=user, 
                obj_in=UserUpdate(status="disabled")
            )
            disabled_users.append(user)
            print(f"✅ User '{user.username}' disabled in database")

        except Exception as e:
            print(f"❌ Failed to disable user '{user.username}': {e}")

    if disabled_users and not dry_run:
        await uow.commit()

    return disabled_users


async def get_quota_status(uow: IUnitOfWork) -> tuple[int, int]:

    """
    
    Get statistics about quota usage.
    
    """

    total_users = await uow.users.get_all_users_count()
    near_quota_users = await uow.users.get_near_quota_users_count()
    
    return total_users, near_quota_users


async def monitor_quotas(dry_run: bool = False, verbose: bool = False) -> None:

    """
    
    Monitor quotas and disable users exceeding their limits.
    
    """

    print("🔍 Monitoring user quotas..." if dry_run else "📊 Checking user quotas...")
    if dry_run:
        print("📋 DRY RUN MODE - No changes will be made")

    auth_manager = LocalAuthAdapter()
    uow = SQLAlchemyUnitOfWork(auth_manager=auth_manager)
    vpn_provider = WireGuardProvider(settings=settings)

    async with uow:
        if verbose:
            total_users, near_quota = await get_quota_status(uow)
            print(f"ℹ️  System status: {total_users} total users, {near_quota} near quota (80%+)")

        transfer_data = await vpn_provider.get_usage_stats()
        if verbose:
            print(f"ℹ️  Retrieved transfer data for {len(transfer_data)} devices")

        device_map = await fetch_all_devices_mapped(uow)
        
        updated_users = await update_user_usage(
            uow=uow, 
            device_map=device_map, 
            transfer_data=transfer_data, 
            dry_run=dry_run
        )
        
        disabled_users = await enforce_quotas(
            uow=uow, 
            vpn_provider=vpn_provider, 
            dry_run=dry_run
        )

        if dry_run:
            print("🔍 Dry run complete:")
            print(f"   - Would update usage for {len(updated_users)} users")
            print(f"   - Would disable {len(disabled_users)} users for exceeding quota")
        else:
            print("✅ Quota check complete:")
            print(f"   - Updated usage for {len(updated_users)} users")
            print(f"   - Disabled {len(disabled_users)} users for exceeding quota")


def main() -> None:

    """
    
    CLI entrypoint.
    
    """
    
    parser = argparse.ArgumentParser(
        description="Monitor network data quotas and disable users who exceed their limits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making actual changes")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed information and system status")
    args = parser.parse_args()

    try:
        asyncio.run(monitor_quotas(dry_run=args.dry_run, verbose=args.verbose))
    except KeyboardInterrupt:
        print("\n⚠️  Quota monitoring interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during quota monitoring: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
