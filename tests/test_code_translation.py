import pytest

from pywrapr.docs_conversion import translate_python_row


@pytest.mark.parametrize(
    'python_code, r_code',
    [
        ("a = 1", "a <- 1"),
        ("{x: 1, y: 2}", "list(x=1, y=2)"),
        ("{1: 'string', 2: 'other'}", 'list("1"=\'string\', "2"=\'other\')'),
    ],
)
def test_code_translation(python_code, r_code):
    assert translate_python_row(python_code) == r_code
