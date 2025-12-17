import pandas as pd
import pytest
from pharmpy.model import Model

from pywrapr.help_functions import (
    belongs_to_package,
    is_pandas_dataframe,
    is_pandas_series,
    skip_translation,
)


@pytest.mark.parametrize(
    'obj, expected',
    [
        (pd.DataFrame, True),
        (pd.Series, False),
        (None, False),
        (Model, False),
    ],
)
def test_create_is_pandas_dataframe(obj, expected):
    assert is_pandas_dataframe(obj) == expected


@pytest.mark.parametrize(
    'obj, expected',
    [
        (pd.DataFrame, False),
        (pd.Series, True),
        (None, False),
        (Model, False),
    ],
)
def test_create_pandas_series(obj, expected):
    assert is_pandas_series(obj) == expected


@pytest.mark.parametrize(
    'obj, package_name, expected',
    [
        (type(None), '', False),
        (type(None), 'pandas', False),
        (pd.DataFrame, 'pandas', True),
        (pd.DataFrame, 'sympy', False),
        (pd.DataFrame, '', False),
        (Model, 'pharmpy', True),
        (Model, 'pandas', False),
    ],
)
def test_belongs_to_package(obj, package_name, expected):
    assert belongs_to_package(obj, package_name) == expected


@pytest.mark.parametrize(
    'obj, skip, expected',
    [
        (type(None), [], True),
        (pd.DataFrame, [], False),
        (pd.DataFrame, ['pandas'], True),
        (pd.Series, ['pandas'], True),
        (Model, ['pandas'], False),
        (type(None), ['pandas'], True),
    ],
)
def test_skip_translation(obj, skip, expected):
    assert skip_translation(obj, skip) == expected
