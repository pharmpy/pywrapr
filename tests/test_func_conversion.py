# SPDX-FileCopyrightText: 2025-2026 Rikard Nordgren and Stella Belin
#
# SPDX-License-Identifier: LGPL-3.0-or-later


from typing import Mapping

import pandas as pd
import pytest

from pywrapr.func_conversion import create_r_func


def test_create_r_func_strings(mock_module):
    def func(a: str, b: str = 'x', c: str | None = None):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(a, b=\'x\', c=NULL)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'func_out <- my$python$module$func(a, b=b, c=c)' in r_func
    assert 'func_out <- convert_output(func_out)' in r_func
    assert 'return(func_out)' in r_func


def test_create_r_func_numbers(mock_module):
    def func(x: int, y: float = 1.5, z: float | int | None = None):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(x, y=1.5, z=NULL)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'my$python$module$func(x, y=y, z=z)' in r_func
    assert 'x <- convert_input(x, "int")' in r_func
    assert 'y <- convert_input(y, "int")' not in r_func
    assert 'z <- convert_input(z, "int")' not in r_func


def test_create_r_func_bool(mock_module):
    def func(flag: bool = True, verbose: bool | None = None):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(flag=TRUE, verbose=NULL)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'func_out <- my$python$module$func(flag=flag, verbose=verbose)' in r_func


def test_create_r_func_lists(mock_module):
    def func(list1: list[str], list2: list[str], list3: list[int] | None = None):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(list1, list2, list3=NULL)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'list1 <- convert_input(list1, "list")' in r_func
    assert 'list2 <- convert_input(list2, "list")' in r_func
    assert 'list3 <- convert_input(list3, "list")' in r_func
    assert 'func_out <- my$python$module$func(list1, list2, list3=list3)' in r_func


def test_convert_r_func_optional_list(mock_module):
    def func(items: list):
        pass

    with pytest.raises(ValueError, match='Parameter `items` has partial type hint'):
        create_r_func(func, mock_module, skip=[], full_trace=False)

    def func(items: list | None):
        pass

    with pytest.raises(ValueError, match='Parameter `items` has partial type hint'):
        create_r_func(func, mock_module, skip=[], full_trace=False)


def test_create_r_func_mapping(mock_module):
    def func(mapping: Mapping[str, str]):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(mapping)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'mapping <- convert_input(mapping, "Mapping")' in r_func
    assert 'func_out <- my$python$module$func(mapping)' in r_func


def test_create_r_func_pandas(mock_module):
    def func(series: pd.Series, df: pd.DataFrame):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(series, df)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'series <- convert_input(series, "pd.Series")' in r_func
    assert 'df <- convert_input(df, "pd.DataFrame")' in r_func
    assert 'func_out <- my$python$module$func(series, df)' in r_func


def test_create_r_func_pandas_multiple_dfs(mock_module):
    def func(df1: pd.DataFrame, df2: pd.DataFrame):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(df1, df2)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'df1 <- convert_input(df1, "pd.DataFrame")' in r_func
    assert 'df2 <- convert_input(df2, "pd.DataFrame")' in r_func
    assert 'func_out <- my$python$module$func(df1, df2)' in r_func


def test_create_r_func_multiple_types(mock_module):
    def func(value: str | int | None = None, data: list[str] | None = None):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(value=NULL, data=NULL)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'value <- convert_input(value, "int")' in r_func
    assert 'data <- convert_input(data, "list")' in r_func
    assert 'func_out <- my$python$module$func(value=value, data=data)' in r_func


def test_create_r_func_var_args(mock_module):
    def func(required: str, *args):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(required, ...)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func


def test_create_r_func_kwargs(mock_module):
    def func(required: str, **kwargs):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(required, ...)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func


def test_create_r_func_full_trace(mock_module):
    def func(a: str, b: str = 'x', c: str | None = None):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=True)
    assert 'func <- function(a, b=\'x\', c=NULL)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'func_out <- my$python$module$func(a, b=b, c=c)' in r_func
    assert 'func_out <- convert_output(func_out)' in r_func
    assert 'return(func_out)' in r_func
    assert 'tryCatch' in r_func
    assert 'err <- reticulate::py_last_error()' in r_func
    assert 'err$type %in% c("InputValidationError", "DispatchingError")' in r_func


def test_create_r_func_return_basic(mock_module):
    def func(a: str, b: str = 'x', c: str | None = None) -> str:
        return a

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'return(func_out)' in r_func


def test_create_r_func_return_null(mock_module):
    def func(a: str, b: str = 'x', c: str | None = None) -> None:
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'return(func_out)' not in r_func
