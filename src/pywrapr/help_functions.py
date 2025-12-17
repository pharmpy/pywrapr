import re
from pathlib import Path
from typing import Any

TYPE_DICT = {
    str: 'str',
    int: 'numeric',
    float: 'numeric',
    bool: 'logical',
    list: 'array',
    None: 'NULL',
    Any: 'any',
    Path: 'str',
}


def is_pandas_dataframe(obj):
    return _is_pandas_obj(obj) and obj.__name__ == 'DataFrame'


def is_pandas_series(obj):
    return _is_pandas_obj(obj) and obj.__name__ == 'Series'


def _is_pandas_obj(obj):
    return getattr(obj, '__module__', '').startswith('pandas')


def belongs_to_package(obj, package_name):
    if package_name:
        return getattr(obj, '__module__', '').startswith(package_name)
    else:
        return False


def skip_translation(obj, packages_to_skip):
    return _belongs_to_packages(obj, packages_to_skip) or obj is type(None)


def _belongs_to_packages(obj, packages):
    return any(belongs_to_package(obj, p) for p in packages)


def py_to_r_arg(arg):
    py_to_r_dict = {'None': 'NULL', 'True': 'TRUE', 'False': 'FALSE', '': '\'\''}

    try:
        return py_to_r_dict[str(arg)]
    except KeyError:
        if isinstance(arg, str):
            return f'\'{arg}\''
        elif isinstance(arg, tuple):

            def _convert(elem):
                if isinstance(elem, str):
                    return f'\'{elem}\''
                return elem

            return f"c({','.join(_convert(elem) for elem in arg)})"
        else:
            return arg


def py_to_r_str(arg, example=False):
    args = {'None': 'NULL', 'True': 'TRUE', 'False': 'FALSE'}

    types = {
        r'\bint\b': 'integer',
        'float': 'numeric',
        r'\bbool\b': 'logical',
        r'\blist\b': 'vector',
        r'\bdict\b': 'list',
        'dictionary': 'list',
        'pd.DataFrame': 'data.frame',
        'pd.Series': 'data.frame',
        r'\w+\[Model\]': 'vector of Model',  # FIXME: more general pattern
        r'\w+\[ModelfitResults\]': 'vector of ModelfitResults',
    }  # FIXME: more general pattern

    py_to_r_dict = {**args, **types}

    if not example:
        py_to_r_dict = {**py_to_r_dict, **{r'\[([0-9]+)\]_*': r'(\1)'}}
        py_to_r_dict = {**py_to_r_dict, **{r'\[([\'\"\w(),\s]+)]': r'c(\1)'}}
        py_to_r_dict = {**py_to_r_dict, **{r'\{(.+:.+,*)+\}': r'list(\1)'}}
        py_to_r_dict = {
            **py_to_r_dict,
            **{r'list\(((.+):(.+),*)+\)': lambda x: x.group().replace(':', "=".format(x.group(1)))},
        }

    arg_sub = arg
    for key, value in py_to_r_dict.items():
        arg_sub = re.sub(key, value, arg_sub)

    return arg_sub
