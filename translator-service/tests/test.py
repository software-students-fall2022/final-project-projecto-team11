import pytest

@pytest.mark.parametrize("text,output_lang,expected_output", [
    ("hello", "fr", "bonjour"),
    ("goodbye", "de", "auf wiedersehen"),
    ("how are you?", "es", "¿cómo estás?"),
])
def test_translate(text, output_lang, expected_output, model_tr, tokenizers):
    # Ensure that the function returns the expected translation for various input phrases
    assert translate(text, output_lang, model_tr, tokenizers) == expected_output

def test_translate_unsupported_language(model_tr, tokenizers):
    # Ensure that the function raises a KeyError when given an unsupported language
    with pytest.raises(KeyError):
        translate("hello", "xyz", model_tr, tokenizers)






