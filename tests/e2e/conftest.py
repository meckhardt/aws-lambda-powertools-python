import pytest
from xdist.scheduler import LoadGroupScheduling

from tests.e2e.utils.infrastructure import call_once
from tests.e2e.utils.lambda_layer.powertools_layer import LocalLambdaPowertoolsLayer


@pytest.fixture(scope="session", autouse=True)
def lambda_layer_build(tmp_path_factory: pytest.TempPathFactory, worker_id: str) -> str:
    """Build Lambda Layer once before stacks are created

    Parameters
    ----------
    tmp_path_factory : pytest.TempPathFactory
        pytest temporary path factory to discover shared tmp when multiple CPU processes are spun up
    worker_id : str
        pytest-xdist worker identification to detect whether parallelization is enabled

    Yields
    ------
    str
        Lambda Layer artefact location
    """

    layer = LocalLambdaPowertoolsLayer()
    yield from call_once(
        task=layer.build,
        tmp_path_factory=tmp_path_factory,
        worker_id=worker_id,
    )


# Hook to use the xdist_group to decide how to schedule tests among the different workers.
# Each test needs to be marked with @pytest.mark.xdist_group(name=...). This way, all
# the tests on each directory will be scheduled on the same worker, thus sharing the
# infrastructure.
def pytest_xdist_make_scheduler(config, log):
    return LoadGroupScheduling(config, log)
