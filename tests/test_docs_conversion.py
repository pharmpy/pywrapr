# SPDX-FileCopyrightText: 2025-2026 Rikard Nordgren and Stella Belin
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Any, Mapping

import pandas as pd

from pywrapr.docs_conversion import create_r_doc


def test_create_r_func_strings():
    def func(a: str, b: str | None = None):
        """Dummy docstring.

        Parameters
        ----------
        a : str
            first string
        b : str or None
            second string
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param a (str) first string' in r_doc
    assert '@param b (str (optional)) second string' in r_doc


def test_create_r_doc_numeric():
    def func(x: int, y: float):
        """Dummy docstring.

        Parameters
        ----------
        x : int
            first number
        y : float
            second number
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param x (numeric) first number' in r_doc
    assert '@param y (numeric) second number' in r_doc


def test_create_r_doc_optional_numeric():
    def func(x: int | None = None, y: float | None = 1.0):
        """Dummy docstring.

        Parameters
        ----------
        x : int or None
            first number
        y : float or None
            second number
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param x (numeric (optional)) first number' in r_doc
    assert '@param y (numeric (optional)) second number' in r_doc


def test_create_r_doc_bool():
    def func(flag: bool = True, verbose: bool | None = None):
        """Dummy docstring.

        Parameters
        ----------
        flag : bool
            a flag
        verbose : bool or None
            whether verbose
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param flag (logical) a flag' in r_doc
    assert '@param verbose (logical (optional)) whether verbose' in r_doc


def test_create_r_doc_lists():
    def func(numbers: list[int], values: list[str | float], optional: list[int] | None = None):
        """Dummy docstring.

        Parameters
        ----------
        numbers : list[int]
            first list
        values : list[str | float]
            second list
        optional : list[int] | None
            third list
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param numbers (array(numeric)) first vector' in r_doc
    assert '@param values (array(str or numeric)) second vector' in r_doc
    assert '@param optional (array(numeric) (optional)) third vector' in r_doc


def test_create_r_doc_tuple():
    def func(values: tuple[int, ...]):
        """Dummy docstring.

        Parameters
        ----------
        values : tuple[int, ...]
            a tuple
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param values (list(numeric,)) a tuple' in r_doc


def test_create_r_doc_mappings():
    def func(
        dict1: Mapping[Any, Any], dict2: Mapping[str, int], dict3: Mapping[int, float] | None = None
    ):
        """Dummy docstring.

        Parameters
        ----------
        dict1 : dict
            first dict
        dict2 : dict
            second dict
        dict3 : dict
            third dict
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param dict1 (list(any=any)) first list' in r_doc
    assert '@param dict2 (list(str=numeric)) second list' in r_doc
    assert '@param dict3 (list(numeric=numeric) (optional)) third list' in r_doc


def test_create_r_doc_mappings_complex():
    def func(dict1: Mapping[int, list[int]], dict2: Mapping[int, str | float]):
        """Dummy docstring.

        Parameters
        ----------
        dict1 : dict
            first dict
        dict2 : dict
            second dict
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param dict1 (list(numeric=array(numeric))) first list' in r_doc
    assert '@param dict2 (list(numeric=str or numeric)) second list' in r_doc


def test_create_r_doc_pandas():
    def func(series: pd.Series, df1: pd.DataFrame, df2: pd.DataFrame | None = None):
        """Dummy docstring.

        Parameters
        ----------
        series : pd.Series
            a series
        df1 : pd.DataFrame
            a data frame
        df2 : pd.DataFrame
            optional data frame
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param series (array) a series' in r_doc
    assert '@param df1 (data.frame) a data frame' in r_doc
    assert '@param df2 (data.frame (optional)) optional data frame' in r_doc


def test_create_r_doc_args():
    def func(required: str, *args):
        """Dummy docstring.

        Parameters
        ----------
        required : str
            a string
        args
            some args
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param required (str) a string' in r_doc
    assert '@param ... some args' in r_doc


def test_create_r_doc_kwargs():
    def func(required: str, **kwargs):
        """Dummy docstring.

        Parameters
        ----------
        required : str
            a string
        kwargs
            some keyword args
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export'])
    assert '@param required (str) a string' in r_doc
    assert '@param ... some keyword args' in r_doc


def test_create_r_func_example():
    def func(a: str):
        """Dummy docstring.

        Parameters
        ----------
        a : str
            a string

        Examples
        --------
        >>> func(a)
        """
        pass

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(
        f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export', 'example']
    )
    assert '@param a (str) a string' in r_doc
    assert '#\' \\dontrun{\n#\' func(a)\n#\' }' in r_doc


def test_create_r_func_return():
    def func(a: str):
        """Dummy docstring.

        Parameters
        ----------
        a : str
            a string

        Returns
        -------
            str
        """
        return a

    r_doc = create_r_doc(func, package_name='', skip=[])
    assert all(row.startswith('#\' ') for row in r_doc.split('\n'))
    assert all(
        f'@{header}' in r_doc for header in ['title', 'description', 'param', 'export', 'return']
    )
    assert '@param a (str) a string' in r_doc
    assert '@return (str)' in r_doc
