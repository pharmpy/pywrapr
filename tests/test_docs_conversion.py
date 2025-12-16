import pytest
from pharmpy.modeling import calculate_eta_shrinkage, set_estimation_step, set_initial_estimates
from pharmpy.tools import run_iivsearch

from pywrapr.docs_conversion import create_r_doc


@pytest.mark.parametrize(
    'func, params_expected, return_expected, example_expected',
    [
        (
            set_initial_estimates,
            [
                'model (Model)',
                'inits (list(str=numeric))',
                'move_est_close_to_bounds (logical)',
                'strict (logical)',
            ],
            'Model',
            [
                'set_initial_estimates(model, results$parameter_estimates)',
                'set_initial_estimates(model, list(\'POP_CL\'=2.0))',
                'model$parameters[\'POP_CL\']',
            ],
        ),
        (
            set_estimation_step,
            [
                'model (Model)',
                'method (str)',
                'idx (numeric)',
                '...',
            ],
            'Model',
            [
                'opts <- list(\'NITER\'=1000, \'ISAMPLE\'=100)',
                'model <- set_estimation_step(model, \'IMP\', evaluation=TRUE, tool_options=opts)',
                'model$execution_steps[1]',
            ],
        ),
        (
            calculate_eta_shrinkage,
            [
                'model (Model)',
                'parameter_estimates (array)',
                'individual_estimates (data.frame)',
                'sd (logical)',
            ],
            'Series',  # FIXME: this should be array
            [
                'pe <- results$parameter_estimates',
                'ie <- results$individual_estimates',
                'calculate_eta_shrinkage(model, pe, ie, sd=TRUE)',
            ],
        ),
        (
            run_iivsearch,
            [
                'model (Model)',
                'results (ModelfitResults)',
                'algorithm (str)',
                'iiv_strategy (str)',
                'rank_type (str)',
                'linearize (logical)',
                'cutoff (numeric (optional))',
                'keep (array(str) (optional))',
                'strictness (str)',
                'correlation_algorithm (str (optional))',
                'E_p (numeric or str (optional))',
                'E_q (numeric or str (optional))',
                'parameter_uncertainty_method (str (optional))',
                '.search_space (str (optional))',
                '.as_fullblock (logical)',
                '...',
            ],
            'IIVSearchResults',
            [
                'run_iivsearch(model=model, results=results, algorithm=\'td_brute_force\')',  # FIXME: This is changed
            ],
        ),
    ],
)
def test_create_r_doc(func, params_expected, return_expected, example_expected):
    r_doc = create_r_doc(func)
    assert all(s.startswith('#\'') for s in r_doc.split('\n'))
    assert all(f'@param {param}' in r_doc for param in params_expected)
    assert f'@return ({return_expected})' in r_doc
    assert all(example in r_doc for example in example_expected)
