from datetime import UTC, datetime
from typing import Any

import pytest

from app.domain.exceptions import DuplicateEntityError
from app.domain.interfaces.repositories import (IAdminRepository,
                                                IDeviceRepository,
                                                IUserRepository)
from app.domain.schemas.admins import AdminCreate, AdminInDB, AdminUpdate
from app.domain.schemas.devices import Device, DeviceCreate, DeviceUpdate
from app.domain.schemas.users import User, UserCreate, UserUpdate
from app.services.access import UserService

# Every fake below stands in for one of the interfaces in app/domain/interfaces, which is the
# only place a collaborator may be substituted. Nothing here patches a module.

STAMP = datetime(2026, 1, 1, tzinfo=UTC)


def make_user(user_id: int, username: str) -> User:
    return User(
        id=user_id,
        username=username,
        quota_bytes=0,
        used_bytes=0,
        status="enabled",
        devices=[],
        created_at=STAMP,
        updated_at=STAMP,
    )


def make_device(device_id: int, entity_in: DeviceCreate, client_identifier: str, ip_address: str | None) -> Device:
    return Device(
        id=device_id,
        user_id=entity_in.user_id,
        device_name=entity_in.device_name,
        client_identifier=client_identifier,
        protocol_data={},
        ip_address=ip_address,
        status="enabled",
        created_at=STAMP,
        updated_at=STAMP,
    )


class FakeAdminRepository:

    async def get(self, id: Any) -> AdminInDB | None:
        return None

    async def get_by_username(self, username: str) -> AdminInDB | None:
        return None

    async def add(self, entity_in: AdminCreate) -> AdminInDB:
        raise NotImplementedError

    async def update(self, db_obj: AdminInDB, obj_in: AdminUpdate) -> AdminInDB:
        raise NotImplementedError

    async def delete(self, id: int) -> AdminInDB:
        raise NotImplementedError


class FakeUserRepository:

    def __init__(self, existing: list[User] | None = None) -> None:
        self.by_id: dict[int, User] = {user.id: user for user in existing or []}
        self.by_username: dict[str, User] = {user.username: user for user in existing or []}
        self.added: list[UserCreate] = []

    async def get(self, id: Any) -> User | None:
        return self.by_id.get(id)

    async def get_by_username(self, username: str) -> User | None:
        return self.by_username.get(username)

    async def get_multi(self, skip: int = 0, limit: int = 100) -> list[User]:
        return list(self.by_id.values())[skip : skip + limit]

    async def get_users_over_quota(self) -> list[User]:
        return []

    async def get_all_users_count(self) -> int:
        return len(self.by_id)

    async def get_near_quota_users_count(self) -> int:
        return 0

    async def add(self, entity_in: UserCreate) -> User:
        self.added.append(entity_in)
        user = make_user(len(self.by_id) + 1, entity_in.username)
        self.by_id[user.id] = user
        self.by_username[user.username] = user
        return user

    async def update(self, db_obj: User, obj_in: UserUpdate) -> User:
        return db_obj

    async def delete(self, id: int) -> User:
        return self.by_id.pop(id)


class FakeDeviceRepository:

    def __init__(self, next_ip: str = "10.0.0.2") -> None:
        self.next_ip = next_ip
        self.added: list[dict[str, Any]] = []

    async def get(self, id: Any) -> Device | None:
        return None

    async def get_multi(self, skip: int = 0, limit: int = 100) -> list[Device]:
        return []

    async def get_multi_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Device]:
        return []

    async def get_enabled_devices_with_enabled_users(self) -> list[Device]:
        return []

    async def add(self, entity_in: DeviceCreate, client_identifier: str, protocol_data: dict[str, Any], ip_address: str | None) -> Device:
        self.added.append({
            "device_name": entity_in.device_name,
            "user_id": entity_in.user_id,
            "client_identifier": client_identifier,
            "protocol_data": protocol_data,
            "ip_address": ip_address,
        })
        return make_device(len(self.added), entity_in, client_identifier, ip_address)

    async def update(self, db_obj: Device, obj_in: DeviceUpdate) -> Device:
        return db_obj

    async def delete(self, id: int) -> Device:
        raise NotImplementedError

    async def get_next_ip(self) -> str:
        return self.next_ip


class FakeUnitOfWork:

    # Declared against the interfaces, because that is what the service is handed and what
    # the type checker compares it to.
    admins: IAdminRepository
    users: IUserRepository
    devices: IDeviceRepository

    def __init__(self, users: FakeUserRepository, devices: FakeDeviceRepository) -> None:
        self.admins = FakeAdminRepository()
        self.users = users
        self.devices = devices
        # The same two objects under their concrete types, so a test can read what they
        # recorded without widening what the service sees.
        self.user_records = users
        self.device_records = devices
        self.commits = 0
        self.rollbacks = 0

    async def __aenter__(self) -> "FakeUnitOfWork":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, traceback: Any) -> None:
        return None

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1


class RecordingVPNProvider:

    def __init__(self, client_identifier: str = "peer-key", protocol_data: dict[str, Any] | None = None) -> None:
        self.client_identifier = client_identifier
        self.protocol_data = protocol_data if protocol_data is not None else {"private_key": "generated"}
        self.provisioned: list[dict[str, Any]] = []
        self.revoked: list[str] = []

    async def validate_interface(self) -> None:
        return None

    async def generate_credentials(self) -> tuple[str, dict[str, Any]]:
        return self.client_identifier, self.protocol_data

    async def provision_client(self, client_identifier: str, ip_address: str | None, protocol_data: dict[str, Any]) -> None:
        self.provisioned.append({
            "client_identifier": client_identifier,
            "ip_address": ip_address,
            "protocol_data": protocol_data,
        })

    async def revoke_client(self, client_identifier: str, protocol_data: dict[str, Any]) -> None:
        self.revoked.append(client_identifier)

    async def get_client_config(self, client_identifier: str, ip_address: str | None, protocol_data: dict[str, Any]) -> str:
        return "[Interface]"

    async def get_usage_stats(self) -> dict[str, int]:
        return {}

    async def list_peers(self) -> list[str]:
        return [entry["client_identifier"] for entry in self.provisioned]


def build_service(existing: list[User] | None = None) -> tuple[UserService, FakeUnitOfWork, RecordingVPNProvider]:
    uow = FakeUnitOfWork(FakeUserRepository(existing), FakeDeviceRepository())
    provider = RecordingVPNProvider()
    return UserService(uow, provider), uow, provider


async def test_creating_a_user_carries_provider_credentials_into_both_records() -> None:
    service, uow, provider = build_service()

    created = await service.create_user_with_device(UserCreate(username="ada"), initial_device_name="laptop")

    assert created.username == "ada"
    assert [entity.username for entity in uow.user_records.added] == ["ada"]

    stored_device = uow.device_records.added[0]
    assert stored_device["device_name"] == "laptop"
    assert stored_device["user_id"] == created.id
    assert stored_device["client_identifier"] == provider.client_identifier
    assert stored_device["protocol_data"] == provider.protocol_data
    assert stored_device["ip_address"] == uow.device_records.next_ip

    assert provider.provisioned == [{
        "client_identifier": provider.client_identifier,
        "ip_address": uow.device_records.next_ip,
        "protocol_data": provider.protocol_data,
    }]
    assert uow.commits == 1


async def test_a_duplicate_username_is_refused_before_the_provider_is_touched() -> None:
    service, uow, provider = build_service(existing=[make_user(1, "ada")])

    with pytest.raises(DuplicateEntityError):
        await service.create_user_with_device(UserCreate(username="ada"))

    assert uow.user_records.added == []
    assert uow.device_records.added == []
    assert provider.provisioned == []
    assert uow.commits == 0


async def test_a_blank_initial_device_name_is_refused() -> None:
    service, uow, provider = build_service()

    with pytest.raises(ValueError):
        await service.create_user_with_device(UserCreate(username="ada"), initial_device_name="   ")

    assert provider.provisioned == []
    assert uow.commits == 0


async def test_a_collaborator_that_does_not_satisfy_its_port_is_refused() -> None:
    with pytest.raises(TypeError):
        UserService(object(), RecordingVPNProvider())  # type: ignore[arg-type]  # the guard under test rejects this

    uow = FakeUnitOfWork(FakeUserRepository(), FakeDeviceRepository())
    with pytest.raises(TypeError):
        UserService(uow, object())  # type: ignore[arg-type]  # the guard under test rejects this
