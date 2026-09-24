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
    detect_language,
    get_model,
    summarize_text,
    translate_text,
)


# ---------------------------------------------------------------------------
# summarize_text
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# translate_text
# ---------------------------------------------------------------------------

def test_translate_text_success():
    """Test that translate_text correctly returns model response content."""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Hola mundo"
    mock_model.invoke.return_value = mock_response

    result = translate_text(mock_model, "Hello world", "Spanish")

    assert result == "Hola mundo"
    mock_model.invoke.assert_called_once()


def test_translate_text_default_target_lang():
    """Test that translate_text defaults to English when target_lang not specified."""
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Good morning"
    mock_model.invoke.return_value = mock_response

    result = translate_text(mock_model, "Buenos días")

    assert result == "Good morning"
    call_args = mock_model.invoke.call_args[0][0]
    assert "English" in call_args


def test_translate_text_error():
    """Test that translate_text wraps execution errors in EasyAIError."""
    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("Model timeout")

    with pytest.raises(EasyAIError) as exc_info:
        translate_text(mock_model, "Bonjour")

    assert "Model timeout" in str(exc_info.value)


# ---------------------------------------------------------------------------
# _is_exit_command
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# get_model
# ---------------------------------------------------------------------------

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
    """Test that provider string inputs are processed case-insensitively."""
    with patch("langchain_anthropic.ChatAnthropic") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("ANTHROPIC", "claude-sonnet-4-6")

    mock_cls.assert_called_once()


def test_get_model_unsupported_provider():
    """Test that an invalid provider raises an EasyAIError."""
    with pytest.raises(EasyAIError):
        get_model("not-a-real-provider", "some-model")


def test_get_model_openai():
    """Test successful model creation for OpenAI provider."""
    with patch("langchain_openai.ChatOpenAI") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("openai", "gpt-4")

    mock_cls.assert_called_once()


def test_get_model_google():
    """Test successful model creation for Google provider."""
    with patch("langchain_google_genai.ChatGoogleGenerativeAI") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("google", "gemini-pro")

    mock_cls.assert_called_once()


def test_get_model_mistral():
    """Test successful model creation for Mistral provider."""
    with patch("langchain_mistralai.ChatMistralAI") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("mistral", "mistral-large")

    mock_cls.assert_called_once()


# ---------------------------------------------------------------------------
# ask_ai
# ---------------------------------------------------------------------------

def test_ask_ai_success():
    """Test that ask_ai sends prompts and returns expected string answers."""
    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="Hi there!")

    result = ask_ai(mock_model, "hello")

    assert result == "Hi there!"
    mock_model.invoke.assert_called_once_with("hello")


def test_ask_ai_wraps_errors():
    """Test that ask_ai catches exceptions and raises an EasyAIError."""
    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("boom")

    with pytest.raises(EasyAIError) as exc_info:
        ask_ai(mock_model, "hello")

    assert "boom" in str(exc_info.value)


# ---------------------------------------------------------------------------
# ai_chat
# ---------------------------------------------------------------------------

def test_ai_chat_exits_on_command(capsys):
    """Test that ai_chat breaks immediately upon receiving an exit command."""
    mock_model = MagicMock()

    with patch("builtins.input", side_effect=["quit"]):
        ai_chat(mock_model)

    captured = capsys.readouterr()
    assert "Talk to you later!" in captured.out
    mock_model.invoke.assert_not_called()


def test_ai_chat_sends_message_then_exits(capsys):
    """Test that ai_chat processes a message before terminating."""
    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="Hi!")

    with patch("builtins.input", side_effect=["hello", "exit"]):
        ai_chat(mock_model)

    captured = capsys.readouterr()
    assert "AI: Hi!" in captured.out
    mock_model.invoke.assert_called_once()


def test_ai_chat_exception_caught(capsys):
    """Test that ai_chat prints the error instead of crashing."""
    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("test exception")

    with patch("builtins.input", side_effect=["hello", "exit"]):
        ai_chat(mock_model)

    captured = capsys.readouterr()
    assert "test exception" in captured.out


###################################
####                ###

        ########
####################################
def test_easy_agent_init_success():
    """Test that EasyAgent loads a .txt master prompt correctly."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        f.write(b"test prompt")
        f_path = f.name
    try:
        agent = EasyAgent(f_path)
        assert agent.master_prompt == "test prompt"
    finally:
        os.remove(f_path)


def test_easy_agent_init_unsupported_ext():
    """Test that unsupported file extensions raise an EasyAIError."""
    with pytest.raises(EasyAIError) as exc_info:
        EasyAgent("prompt.md")
    assert "not supported" in str(exc_info.value)


def test_easy_agent_init_not_found():
    """Test that a missing file raises an EasyAIError."""
    with pytest.raises(EasyAIError) as exc_info:
        EasyAgent("nonexistent_prompt.txt")
    assert "No such file or directory" in str(exc_info.value)


# ---------------------------------------------------------------------------
# detect_language
# ---------------------------------------------------------------------------

def test_detect_language_english():
    """Test that detect_language recognizes English text."""
    assert detect_language("Hello, how are you?") == "English"


def test_detect_language_italian():
    """Test that detect_language recognizes Italian text."""
    assert detect_language("Ciao, come stai?") == "Italian"


def test_detect_language_spanish():
    """Test that detect_language recognizes Spanish text."""
    assert detect_language("Hola, que tal? El perro es de mi amigo") == "Spanish"


def test_detect_language_unknown():
    """Test that detect_language returns 'Unknown' for unrecognized text."""
    assert detect_language("xyz 123 qqq") == "Unknown"


def test_detect_language_empty_raises():
    """Test that detect_language raises EasyAIError on empty input."""
    with pytest.raises(EasyAIError):
        detect_language("")


def test_detect_language_whitespace_raises():
    """Test that detect_language raises EasyAIError on whitespace-only input."""
    with pytest.raises(EasyAIError):
        detect_language("   \n\t ")


def test_detect_language_non_string_raises():
    """Test that detect_language raises EasyAIError on non-string input."""
    with pytest.raises(EasyAIError):
        detect_language(123)
