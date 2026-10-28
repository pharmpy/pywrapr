# SPDX-FileCopyrightText: 2025-2026 Rikard Nordgren and Stella Belin
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pharmpy.modeling
import pharmpy.tools

from pywrapr.build_functions import create_module_functions


def test_build_functions():
    create_module_functions(pharmpy.modeling, skip=['sympy', 'symengine', 'numpy'])
    create_module_functions(pharmpy.tools, skip=['sympy', 'symengine', 'numpy'], full_trace=True)
