import pharmpy.modeling
import pharmpy.tools

from pywrapr.build_functions import create_module_functions


def test_build_functions():
    create_module_functions(pharmpy.modeling, skip=['sympy', 'symengine', 'numpy'])
    create_module_functions(pharmpy.tools, skip=['sympy', 'symengine', 'numpy'])
