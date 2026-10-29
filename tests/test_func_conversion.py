# SPDX-FileCopyrightText: 2025-2026 Rikard Nordgren and Stella Belin
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from __future__ import annotations

from typing import Mapping

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
    def func(x: int, y: float = 1.5, z: int | None = None):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(x, y=1.5, z=NULL)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'my$python$module$func(x, y=y, z=z)' in r_func
    assert 'x <- convert_input(x, "int")'
    assert 'y <- convert_input(y, "int")'


def test_create_r_func_bool(mock_module):
    def func(flag: bool = True, verbose: bool | None = None):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(flag=TRUE, verbose=NULL)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'func_out <- my$python$module$func(flag=flag, verbose=verbose)' in r_func


def test_create_r_func_lists(mock_module):
    def func(list1: list[str], list2: list[str]):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(list1, list2)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'list1 <- convert_input(list1, "list")' in r_func
    assert 'list2 <- convert_input(list2, "list")' in r_func
    assert 'func_out <- my$python$module$func(list1, list2)' in r_func


# def test_convert_r_func_optional_list(mock_module):
#     def func(items: list | None = None):
#         pass
#
#     r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
#     assert 'reticulate::py_clear_last_error()' in r_func
#     assert 'func <- function(items, default_list=NULL)' in r_func
#     assert 'items <- convert_input(items, "list")' in r_func
#     assert 'default_list <- convert_input(default_list, "list")' in r_func
#     assert 'func_out <- my$python$module$func(items, default_list=default_list)' in r_func


def test_create_r_func_mapping(mock_module):
    def func(mapping: Mapping[str, str]):
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(mapping)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'mapping <- convert_input(mapping, "Mapping")' in r_func
    assert 'func_out <- my$python$module$func(mapping)' in r_func


def test_create_r_func_pandas(mock_module, mock_pandas):
    def func(series: pd.Series, df: pd.DataFrame):  # noqa: F821
        pass

    func.__globals__['pd'] = mock_pandas

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(series, df)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'series <- convert_input(series, "pd.Series")' in r_func
    assert 'df <- convert_input(df, "pd.DataFrame")' in r_func
    assert 'func_out <- my$python$module$func(series, df)' in r_func


def test_create_r_func_pandas_multiple_dfs(mock_module, mock_pandas):
    def func(df1: pd.DataFrame, df2: pd.DataFrame):  # noqa: F821
        pass

    func.__globals__['pd'] = mock_pandas

    r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
    assert 'func <- function(df1, df2)' in r_func
    assert 'reticulate::py_clear_last_error()' in r_func
    assert 'df1 <- convert_input(df1, "pd.DataFrame")' in r_func
    assert 'df2 <- convert_input(df2, "pd.DataFrame")' in r_func
    assert 'func_out <- my$python$module$func(df1, df2)' in r_func


# def test_create_r_func_multiple_types(mock_module):
#     def func(value: str | int | None = None, data: list | None = None):
#         pass
#
#     r_func = create_r_func(func, mock_module, skip=[], full_trace=False)
#     assert 'func <- function(value=NULL, data=NULL)' in r_func
#     assert 'reticulate::py_clear_last_error()' in r_func
#     assert 'value <- convert_input(value, "int")' in r_func
#     assert 'data <- convert_input(data, "list")' in r_func
#     assert 'func_out <- my$python$module$func(value=value, data=data)' in r_func


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

    r_func = create_r_func(func, mock_module, skip=[], full_trace=True)
    assert 'return(func_out)' in r_func


def test_create_r_func_return_null(mock_module):
    def func(a: str, b: str = 'x', c: str | None = None) -> None:
        pass

    r_func = create_r_func(func, mock_module, skip=[], full_trace=True)
    assert 'return(func_out)' not in r_func
