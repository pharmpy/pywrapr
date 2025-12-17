import inspect

from pywrapr.docs_conversion import create_r_doc
from pywrapr.func_conversion import create_r_func


def create_module_functions(module, skip=None):
    funcs = inspect.getmembers(module, inspect.isfunction)
    func_str = ''
    module_name = getattr(module, '__name__')
    if module_name:
        package_name = module_name.split('.')[0]
    else:
        package_name = ''
    for name, func in funcs:
        if name not in module.__all__:
            continue
        if not skip:
            skip = []
        r_func = create_r_func(func, module, skip)
        r_doc = create_r_doc(func, package_name, skip)
        func_str += f'{r_doc}\n{r_func}\n\n'
    return func_str
