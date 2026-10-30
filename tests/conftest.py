from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope='session')
def mock_module():
    mock_module = MagicMock()
    mock_module.__name__ = 'my.python.module'
    return mock_module
