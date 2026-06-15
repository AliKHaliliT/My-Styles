from app.domain.schemas.devices import Device as DomainDevice
from app.models.device import Device as DBDevice


def db_to_domain_device(db_device: DBDevice) -> DomainDevice:

    """

    Convert Database Device to Domain Device.

    """

    return DomainDevice.model_validate(db_device, from_attributes=True)
