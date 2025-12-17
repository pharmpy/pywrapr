import pharmpy.modeling
import pytest
from pharmpy.modeling import calculate_eta_shrinkage, set_estimation_step, set_initial_estimates
from pharmpy.tools import run_iivsearch

from pywrapr.func_conversion import create_r_func


@pytest.mark.parametrize(
    'func, module, signature_expected, py_call_expected, conversions_expected',
    [
        (
            set_initial_estimates,
            pharmpy.modeling,
            'function(model, inits, move_est_close_to_bounds=FALSE, strict=TRUE)',
            'pharmpy$modeling$set_initial_estimates(model, inits, move_est_close_to_bounds=move_est_close_to_bounds, '
            'strict=strict)',
            ['convert_input(inits, "Mapping")'],
        ),
        (
            set_estimation_step,
            pharmpy.modeling,
            'function(model, method, idx=0, ...)',
            'set_estimation_step(model, method, idx=idx, ...)',
            ['convert_input(idx, "int")'],
        ),
        (
            calculate_eta_shrinkage,
            pharmpy.modeling,
            'function(model, parameter_estimates, individual_estimates, sd=FALSE)',
            'calculate_eta_shrinkage(model, parameter_estimates, individual_estimates, sd=sd)',
            [
                'convert_input(parameter_estimates, "pd.Series")',
                'convert_input(individual_estimates, "pd.DataFrame")',
            ],
        ),
        (
            run_iivsearch,
            pharmpy.tools,
            'function(model, results, algorithm=\'top_down_exhaustive\', iiv_strategy=\'no_add\', rank_type=\'bic\', '
            'linearize=FALSE, cutoff=NULL, keep=c(\'CL\'), strictness=\'minimization_successful or (rounding_errors '
            'and sigdigs>=0.1)\', correlation_algorithm=NULL, E_p=NULL, E_q=NULL, parameter_uncertainty_method=NULL, '
            '.search_space=NULL, .as_fullblock=FALSE, ...)',
            'run_iivsearch(model, results, algorithm=algorithm, iiv_strategy=iiv_strategy, rank_type=rank_type, '
            'linearize=linearize, cutoff=cutoff, keep=keep, strictness=strictness, correlation_algorithm='
            'correlation_algorithm, E_p=E_p, E_q=E_q, parameter_uncertainty_method=parameter_uncertainty_method, '
            '`_search_space`=.search_space, `_as_fullblock`=.as_fullblock, ...)',
            ['convert_input(keep, "list")'],
        ),
    ],
)
def test_create_r_func(func, module, signature_expected, py_call_expected, conversions_expected):
    r_func = create_r_func(func, module, skip=['sympy', 'symengine', 'numpy'])
    assert f'{func.__name__} <- {signature_expected}' in r_func.split('\n')[0]
    assert py_call_expected in r_func
    assert all(conv in r_func for conv in conversions_expected)
    if func.__name__.startswith('run'):
        assert 'tryCatch' in r_func
        assert 'return(invisible())' in r_func
