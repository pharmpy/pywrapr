import inspect

from pywrapr.func_conversion import create_r_func
from pywrapr.docs_conversion import create_r_doc


def create_module_functions(module):
    funcs = inspect.getmembers(module, inspect.isfunction)
    func_str = ''
    for name, func in funcs:
        if name not in module.__all__:
            continue
        r_func = create_r_func(func, module)
        r_doc = create_r_doc(func)
        func_str += f'{r_doc}\n{r_func}\n\n'
    return func_str
