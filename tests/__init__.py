import os

import pytest


def requires_env(*envs):
    env = os.environ.get('TEST_ENVIRONMENT', 'remote')

    envs = envs if isinstance(envs, list) else [*envs]

    return pytest.mark.skipif(
        env not in envs,
        reason=f'Not suitable envrionment {env} for current test',
    )
