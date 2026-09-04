import pytest
from unittest.mock import MagicMock, patch
from py_simple.easy_ai import (
    summarize_text, 
    get_model,
    ask_ai,
    ai_chat,
    _is_exit_command,
    EasyAIError,
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
    assert _is_exit_command(text) == expected

def test_get_model_anthropic():
    with patch("langchain_anthropic.ChatAnthropic") as mock_cls:
        mock_cls.return_value = MagicMock()
        model = get_model("anthropic", "claude-sonnet-4-6", api_key="fake-key")

    mock_cls.assert_called_once()
    assert model is mock_cls.return_value


def test_get_model_ollama_default_url():
    with patch("langchain_ollama.ChatOllama") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("ollama", "llama3")

    _, kwargs = mock_cls.call_args
    assert kwargs["base_url"] == "http://localhost:11434"


def test_get_model_provider_case_insensitive():
    with patch("langchain_anthropic.ChatAnthropic") as mock_cls:
        mock_cls.return_value = MagicMock()
        get_model("ANTHROPIC", "claude-sonnet-4-6")

    mock_cls.assert_called_once()


def test_get_model_unsupported_provider():
    with pytest.raises(EasyAIError):
        get_model("not-a-real-provider", "some-model")

def test_ask_ai_success():
    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="Hi there!")

    result = ask_ai(mock_model, "hello")

    assert result == "Hi there!"
    mock_model.invoke.assert_called_once_with("hello")


def test_ask_ai_wraps_errors():
    mock_model = MagicMock()
    mock_model.invoke.side_effect = Exception("boom")

    with pytest.raises(EasyAIError) as exc_info:
        ask_ai(mock_model, "hello")

    assert "boom" in str(exc_info.value) 

def test_ai_chat_exits_on_command(capsys):
    mock_model = MagicMock()

    with patch("builtins.input", side_effect=["quit"]):
        ai_chat(mock_model)

    captured = capsys.readouterr()
    assert "Talk to you later!" in captured.out
    mock_model.invoke.assert_not_called()


def test_ai_chat_sends_message_then_exits(capsys):
    mock_model = MagicMock()
    mock_model.invoke.return_value = MagicMock(content="Hi!")

    with patch("builtins.input", side_effect=["hello", "exit"]):
        ai_chat(mock_model)

    captured = capsys.readouterr()
    assert "AI: Hi!" in captured.out
    mock_model.invoke.assert_called_once()