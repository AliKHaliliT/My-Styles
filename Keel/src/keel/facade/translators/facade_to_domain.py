from keel.domain.schemas.runs import RunSpec
from keel.facade.schemas import RunRequest


def facade_to_domain_run_request(request: RunRequest) -> RunSpec:

    """

    Convert a facade RunRequest to a domain RunSpec.

    """

    return RunSpec(**request.model_dump())
