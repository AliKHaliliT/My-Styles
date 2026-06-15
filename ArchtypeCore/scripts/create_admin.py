from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import argparse
import asyncio
from getpass import getpass
import os
import re

from app.core.security.local_auth import LocalAuthAdapter
from app.domain.schemas.admins import AdminCreate
from app.repositories.sqlalchemy.uow import SQLAlchemyUnitOfWork


def is_password_strong(password: str) -> tuple[bool, str | None]:
    
    """
    
    Validate password strength based on common security rules.
    
    """

    rules =[
        (r".{8,}", "Password must be at least 8 characters long"),
        (r"[A-Z]", "Password must contain at least one uppercase letter"),
        (r"[a-z]", "Password must contain at least one lowercase letter"),
        (r"\d", "Password must contain at least one digit"),
        (r"[!@#$%^&*(),.?\":{}|<>]", "Password must contain at least one special character"),
    ]
    for pattern, message in rules:
        if not re.search(pattern, password):
            return False, message
    return True, None


async def create_admin(username: str, password: str, role: str = "admin") -> bool:

    """
    
    Create a new admin user asynchronously via UoW.
    
    """

    auth_manager = LocalAuthAdapter()
    uow = SQLAlchemyUnitOfWork(auth_manager=auth_manager)

    try:
        async with uow:
            if await uow.admins.get_by_username(username=username):
                print(f"❌ Admin with username '{username}' already exists.")
                return False

            if not (is_strong := is_password_strong(password))[0]:
                print(f"❌ Password too weak: {is_strong[1]}")
                return False

            match role.lower():
                case "admin" | "superadmin":
                    normalized_role = role.lower()
                case _:
                    print("⚠️  Invalid role provided. Defaulting to 'admin'.")
                    normalized_role = "admin"

            admin_data = AdminCreate(username=username, password=password, role=normalized_role)
            
            await uow.admins.add(entity_in=admin_data)
            await uow.commit()

            print(f"✅ Admin user '{username}' with role '{normalized_role}' created successfully.")
            return True

    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        return False


def get_username(args: argparse.Namespace) -> str:
    return args.username or os.getenv("ADMIN_USERNAME") or input("Enter username: ").strip()


def get_password(args: argparse.Namespace) -> str | None:
    if password := args.password or os.getenv("ADMIN_PASSWORD"):
        return password

    password = getpass("Enter password: ")
    if password != getpass("Confirm password: "):
        print("❌ Passwords do not match.")
        return None
    return password


def get_role(args: argparse.Namespace) -> str:
    return (args.role or os.getenv("ADMIN_ROLE", "admin")).lower()


def main() -> None:
    
    """
    
    Main entry point for CLI admin creation.
    
    """

    parser = argparse.ArgumentParser(
        description="Create a new admin user for ArchetypeCore",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-u", "--username", help="Username for the new admin")
    parser.add_argument("-p", "--password", help="Password for the new admin")
    parser.add_argument("-r", "--role", choices=["admin", "superadmin"], default="admin", help="Role of the new admin")
    args = parser.parse_args()

    username = get_username(args)
    if not (password := get_password(args)):
        return

    role = get_role(args)
    success = asyncio.run(create_admin(username=username, password=password, role=role))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
