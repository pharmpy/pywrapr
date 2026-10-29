from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope='session')
def mock_module():
    mock_module = MagicMock()
    mock_module.__name__ = 'my.python.module'
    return mock_module


@pytest.fixture(scope='session')
def mock_pandas():
    pd_mock = MagicMock()
    pd_mock.Series = MagicMock(spec=type)
    pd_mock.Series.__name__ = 'Series'
    pd_mock.Series.__module__ = 'pandas'
    pd_mock.DataFrame = MagicMock(spec=type)
    pd_mock.DataFrame.__name__ = 'DataFrame'
    pd_mock.DataFrame.__module__ = 'pandas'
    pd_mock.__name__ = 'pandas'
    return pd_mock
