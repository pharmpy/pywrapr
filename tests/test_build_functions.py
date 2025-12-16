import pharmpy.modeling

from pywrapr.build_functions import create_module_functions


def test_build_functions():
    create_module_functions(pharmpy.modeling)
