import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from py_simple_package.src.py_simple.easy_ai import (
    EasyAgent,
    EasyAIError,
    _is_exit_command,
    ai_chat,
    ask_ai,
    get_model,
    summarize_text,
    translate_text,
    rewrite_text,
    analyze_sentiment,
)


def test_summarize_text_success():
    """Test that summarize_text correctly returns model response content."""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Summary result content."
    mock_model.invoke.return_value = mock_response

    result = summarize_text(mock_model, "Some text to summarize.")

    assert result == "Summary result content."
    mock_model.invoke.assert_called_once()


def test_summarize_text_error():
    """Test that summarize_text wraps execution errors in EasyAIError."""
    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("Model timeout")

    with pytest.raises(EasyAIError) as exc_info:
        summarize_text(mock_model, "Some text")

    assert "Model timeout" in str(exc_info.value)


def test_translate_text():
    """Test that translate_text correctly returns model response content."""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Hola mundo"
    mock_model.invoke.return_value = mock_response

    result = translate_text(mock_model, "Hello world", "Spanish")

    assert result == "Hola mundo"
    mock_model.invoke.assert_called_once()


@pytest.mark.parametrize(
    "text, expected",
    [
        ("exit", True),
        ("QUIT", True),
        ("Stop", True),
        ("bye", True),
        ("hello", False),
        ("", False),
    ],
)
def test_is_exit_command(text, expected):
    """Test command recognition for exiting interactive chat sessions."""
    assert _is_exit_command(text) == expected


def test_get_model_anthropic():
    """Test successful model creation for Anthropic provider."""
    with patch("langchain_anthropic.ChatAnthropic") as mock_cls:
        mock_cls.return_value = MagicMock()
        model = get_model("anthropic", "claude-sonnet-4-6", api_key="fake-key")

    mock_cls.assert_called_once()
    assert model is mock_cls.return_value


def test_get_model_ollama_default_url():
    """Test default base URL assignment for Ollama models."""
    with patch("langchain_ollama.ChatOllama") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("ollama", "llama3")

    _, kwargs = mock_cls.call_args
    assert kwargs["base_url"] == "http://localhost:11434"


def test_get_model_provider_case_insensitive():
    """Test that model provider string inputs are processed case-insensitively."""
    with patch("langchain_anthropic.ChatAnthropic") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("ANTHROPIC", "claude-sonnet-4-6")

    mock_cls.assert_called_once()


def test_get_model_unsupported_provider():
    """Test that requesting an invalid model provider raises an EasyAIError."""
    with pytest.raises(EasyAIError):
        get_model("not-a-real-provider", "some-model")


def test_ask_ai_success():
    """Test that ask_ai sends prompts and returns expected string answers."""
    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="Hi there!")

    result = ask_ai(mock_model, "hello")

    assert result == "Hi there!"
    mock_model.invoke.assert_called_once_with("hello")


def test_ask_ai_wraps_errors():
    """Test that ask_ai safely catches exceptions and raises an EasyAIError."""
    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("boom")

    with pytest.raises(EasyAIError) as exc_info:
        ask_ai(mock_model, "hello")

    assert "boom" in str(exc_info.value)


def test_ai_chat_exits_on_command(capsys):
    """Test that ai_chat loop breaks immediately upon receiving an exit command."""
    mock_model = MagicMock()

    with patch("builtins.input", side_effect=["quit"]):
        ai_chat(mock_model)

    captured = capsys.readouterr()
    assert "Talk to you later!" in captured.out
    mock_model.invoke.assert_not_called()


def test_ai_chat_sends_message_then_exits(capsys):
    """Test that ai_chat processes a message interaction before terminating."""
    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="Hi!")

    with patch("builtins.input", side_effect=["hello", "exit"]):
        ai_chat(mock_model)

    captured = capsys.readouterr()
    assert "AI: Hi!" in captured.out
    mock_model.invoke.assert_called_once()


def test_translate_text_success():
    """Test that translate_text correctly returns model response content."""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Hello world"
    mock_model.invoke.return_value = mock_response

    result = translate_text(mock_model, "Hola mundo", target_lang="English")

    assert result == "Hello world"
    mock_model.invoke.assert_called_once()


def test_translate_text_default_target_lang():
    """Test that translate_text defaults to English when target_lang not specified."""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Good morning"
    mock_model.invoke.return_value = mock_response

    result = translate_text(mock_model, "Buenos días")

    assert result == "Good morning"
    # verify the prompt included "English"
    call_args = mock_model.invoke.call_args[0][0]
    assert "English" in call_args


def test_translate_text_error():
    """Test that translate_text wraps execution errors in EasyAIError."""
    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("Model timeout")

    with pytest.raises(EasyAIError) as exc_info:
        translate_text(mock_model, "Bonjour")

    assert "Model timeout" in str(exc_info.value)


def test_get_model_openai():
    from py_simple_package.src.py_simple.easy_ai import get_model
    from unittest.mock import patch, MagicMock

    with patch("langchain_openai.ChatOpenAI") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("openai", "gpt-4")
    mock_cls.assert_called_once()


def test_get_model_google():
    from py_simple_package.src.py_simple.easy_ai import get_model
    from unittest.mock import patch, MagicMock

    with patch("langchain_google_genai.ChatGoogleGenerativeAI") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("google", "gemini-pro")
    mock_cls.assert_called_once()


def test_get_model_mistral():
    from py_simple_package.src.py_simple.easy_ai import get_model
    from unittest.mock import patch, MagicMock

    with patch("langchain_mistralai.ChatMistralAI") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("mistral", "mistral-large")
    mock_cls.assert_called_once()


def test_ai_chat_exception_caught(capsys):
    from py_simple_package.src.py_simple.easy_ai import ai_chat
    from unittest.mock import patch, MagicMock

    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("test exception")
    with patch("builtins.input", side_effect=["hello", "exit"]):
        ai_chat(mock_model)
    captured = capsys.readouterr()
    assert "test exception" in captured.out


def test_easy_agent_init_success():
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"test prompt")
        f_path = f.name
    try:
        agent = EasyAgent(f_path)
        assert agent.master_prompt == "test prompt"
    finally:
        os.remove(f_path)


def test_easy_agent_init_unsupported_ext():
    with pytest.raises(EasyAIError) as exc_info:
        EasyAgent("prompt.md")
    assert "not supported" in str(exc_info.value)


def test_easy_agent_init_not_found():
    with pytest.raises(EasyAIError) as exc_info:
        EasyAgent("nonexistent_prompt.txt")
    assert "No such file or directory" in str(exc_info.value)


def test_rewrite_text_success():
    """Test that rewrite_text changes text tone and returns it"""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "hello py-simple-wrap devs."
    mock_model.invoke.return_value = mock_response
        
    result = rewrite_text(mock_model,"hello devs")
    assert result == "hello py-simple-wrap devs."
    mock_model.invoke.assert_called_once()

def test_rewrite_text_error():
    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("model failed")

    with pytest.raises(EasyAIError) as exc_info:
        rewrite_text(mock_model, "hello devs")

    assert "model failed" in str(exc_info.value)


def test_rewrite_text_includes_tone_in_prompt():
    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="rewritten")
    rewrite_text(mock_model, "hello devs", tone="excited")
    prompt = mock_model.invoke.call_args[0][0]
    assert "excited" in prompt
    assert "hello devs" in prompt


def test_rewrite_text_default_tone():
    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="ok")
    rewrite_text(mock_model, "hello devs")
    assert "calm" in mock_model.invoke.call_args[0][0]

def test_analyze_sentiment_success():
    """Test that analyze_sentiment returns the model's response content."""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Positive"
    mock_model.invoke.return_value = mock_response

    result = analyze_sentiment(mock_model, "Great work on this release!")

    assert result == "Positive"
    mock_model.invoke.assert_called_once()
    prompt_sent = mock_model.invoke.call_args[0][0]
    assert "Great work on this release!" in prompt_sent


def test_analyze_sentiment_error():
    """Test that analyze_sentiment wraps underlying exceptions in EasyAIError."""
    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("API rate limit exceeded")

    with pytest.raises(EasyAIError) as exc_info:
        analyze_sentiment(mock_model, "Some text")

    assert "API rate limit exceeded" in str(exc_info.value)    


def test_detect_language_english():
    from py_simple import detect_language

    assert detect_language("Hello, how are you?") == "English"


def test_detect_language_italian():
    from py_simple import detect_language

    assert detect_language("Ciao, come stai?") == "Italian"


def test_detect_language_spanish():
    from py_simple import detect_language

    assert detect_language("Hola, como estas?") == "Spanish"


def test_detect_language_french():
    from py_simple import detect_language

    assert detect_language("Bonjour, comment allez-vous?") == "French"


def test_detect_language_german():
    from py_simple import detect_language

    assert detect_language("Hallo, wie geht es dir?") == "German"


def test_detect_language_unknown():
    from py_simple import detect_language

    assert detect_language("qwerty zxcvb asdfgh") == "Unknown"


def test_detect_language_empty_text():
    import pytest
    from py_simple import detect_language

    with pytest.raises(Exception):
        detect_language("")


def test_chunk_text_keeps_words_whole():
    from py_simple_package.src.py_simple.easy_ai import chunk_text

    pieces = chunk_text("Pack a lunch and a notebook", max_chars=16)
    assert pieces == ["Pack a lunch and", "a notebook"]
    assert all(len(piece) <= 16 for piece in pieces)


def test_chunk_text_splits_a_word_longer_than_the_limit():
    from py_simple_package.src.py_simple.easy_ai import chunk_text

    assert chunk_text("abcdefghij", max_chars=4) == ["abcd", "efgh", "ij"]


def test_chunk_text_empty_string():
    from py_simple_package.src.py_simple.easy_ai import chunk_text

    assert chunk_text("") == []


def test_chunk_text_rejects_bad_input():
    from py_simple_package.src.py_simple.easy_ai import EasyAIError, chunk_text

    with pytest.raises(EasyAIError):
        chunk_text(12)
    with pytest.raises(EasyAIError):
        chunk_text("hello", max_chars=0)


def test_chunk_text_public_import():
    from py_simple_package.src.py_simple import chunk_text as public_chunk_text
    from py_simple_package.src.py_simple.easy_ai import chunk_text

    assert public_chunk_text is chunk_text


def test_detect_language_invalid_type():
    import pytest
    from py_simple import detect_language

    with pytest.raises(Exception):
        detect_language(None)
def test_summarize_text_success():
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Short summary."
    mock_model.invoke.return_value = mock_response
    result = summarize_text(mock_model, "Very long text here", 10)
    assert result == "Short summary."

def test_summarize_text_error():
    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("API error")
    with pytest.raises(EasyAIError):
        summarize_text(mock_model, "Text", 50)
