"""
easy_ai wraps common LangChain functionality to make it easier to use.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from langchain_core.language_models import BaseChatModel


class EasyAIError(Exception):
    """
    Raised when a call to an AI model or provider cannot be completed.

    Args:
        message (str): Description of what went wrong.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def _is_exit_command(text: str) -> bool:
    """
    Checks whether a piece of user input should end the chat loop.

    Args:
        text (str): The raw text the user typed.

    Returns:
        True if `text` matches "exit", "quit", "stop", or "bye"
        (case-insensitive), False otherwise.
    """
    return text.lower() in ("exit", "quit", "stop", "bye")


def get_model(
    provider: str,
    model_name: str,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout: int = 30,
) -> BaseChatModel:
    """
    Returns a LangChain chat model instance for the given provider,
    without you having to remember each provider's import path and
    constructor arguments.

    Args:
        provider (str): Name of the LLM provider. One of "openai",
            "ollama", "anthropic", "google", or "mistral". Case-insensitive.
        model_name (str): Name of the model to use (e.g., "gpt-4o",
            "llama3", "claude-sonnet-4-6").
        api_key (str): API key for the provider, if required. Not used
            for "ollama". Defaults to None.
        base_url (str): Custom base URL for the provider. Used for
            "openai" and "ollama" (defaults to
            "http://localhost:11434" for ollama if not provided).
            Defaults to None.
        timeout (int): Request timeout in seconds. Currently only used
            for "anthropic". Defaults to 30.

    Returns:
        A LangChain chat model instance corresponding to the given
        provider.

    Raises:
        EasyAIError: If `provider` isn't one of the supported providers.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_model

            model = get_model("anthropic", "claude-sonnet-4-6")
            ```

        === "The Traditional Way"
            ```python
            from langchain_anthropic import ChatAnthropic

            model = ChatAnthropic(
                model_name="claude-sonnet-4-6",
                timeout=30,
                stop=None
            )
            ```
    """

    provider = provider.lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        model = ChatOpenAI(model=model_name, api_key=api_key, base_url=base_url)
        return model

    elif provider == "ollama":
        from langchain_ollama import ChatOllama

        url = base_url if base_url else "http://localhost:11434"
        model = ChatOllama(model=model_name, base_url=url)
        return model

    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        from pydantic import SecretStr

        api_key = SecretStr(api_key) if api_key is not None else None
        model = ChatAnthropic(
            model_name=model_name,
            api_key=api_key,
            timeout=timeout,
            stop=None,
        )
        return model

    elif provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        model = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
        )
        return model

    elif provider == "mistral":
        from langchain_mistralai import ChatMistralAI

        model = ChatMistralAI(
            api_key=api_key,
            model_name=model_name,
        )
        return model

    else:
        raise EasyAIError(
            f"\n\n\nERROR: Provider '{provider}' is not supported yet!"
        )


def ask_ai(
    ai_model: BaseChatModel,
    question: str | list,
) -> str | list[str | dict[Any, Any]]:
    """
    Sends a question to a LangChain chat model and returns the
    content of the response, without you having to reach into the
    returned message object yourself.

    Args:
        ai_model (BaseChatModel): A LangChain chat model instance,
            such as one returned by `get_model()`.
        question (str | list): Either a single question as plain
            text, or a list of LangChain message objects
            (HumanMessage/AIMessage) representing the conversation
            so far. Pass a list to give the model memory of prior
            turns; the caller is responsible for building and
            updating that list.

    Returns:
        The model's response content. Usually a plain string, but
        some providers may return a list of content blocks instead.

    Raises:
        EasyAIError: If the underlying call to the model fails for
            any reason (e.g. invalid API key, network error, timeout).

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_model, ask_ai

            model = get_model("anthropic", "claude-sonnet-4-6")
            answer = ask_ai(model, "hi")
            ```

        === "The Traditional Way"
            ```python
            from langchain_anthropic import ChatAnthropic

            model = ChatAnthropic(model_name="claude-sonnet-4-6")
            answer = model.invoke("hi").content
            ```
    """

    try:
        message = ai_model.invoke(question).content
        return message
    except Exception as e:
        raise EasyAIError(f"\n\n\nERROR: {e}") from None


def ai_chat(ai_model: BaseChatModel) -> None:
    """
    Runs an interactive chat loop in the terminal against a LangChain
    chat model, without you having to write the input/print loop,
    exit handling, or conversation memory yourself.

    Prompts for input with "You: ", prints each reply prefixed with
    "AI: ", and keeps going until the user types "exit", "quit", "stop",
    or "bye" (at which point it prints a goodbye message and returns).
    Each turn is appended to an internal history list of HumanMessage/
    AIMessage objects, and the full history is sent to the model on
    every call, so the model has memory of the whole conversation for
    as long as the loop runs. The history is local to this call and is
    not preserved once the loop exits. Errors from `ask_ai()` are
    caught and printed instead of raising, so a single bad call
    doesn't end the session.

    Args:
        ai_model (BaseChatModel): A LangChain chat model instance,
            such as one returned by `get_model()`.

    Returns:
        None. Runs until the user exits the loop.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_model, ai_chat

            model = get_model("anthropic", "claude-sonnet-4-6")
            ai_chat(model)
            ```

        === "The Traditional Way"
            ```python
            from langchain_anthropic import ChatAnthropic
            from langchain_core.messages import HumanMessage, AIMessage

            model = ChatAnthropic(model_name="claude-sonnet-4-6")

            history = []
            while True:
                user_input = input("You: ")
                if user_input.lower() in ("exit", "quit", "stop", "bye"):
                    print("AI: Talk to you later!")
                    break
                history.append(HumanMessage(content=user_input))
                response = model.invoke(history).content
                history.append(AIMessage(content=response))
                print(f"AI: {response}")
            ```
    """

    from langchain_core.messages import AIMessage, HumanMessage

    history = []

    while True:
        try:
            user_input = input("You: ")

            if _is_exit_command(user_input):
                print("AI: Talk to you later!")
                break

            history.append(HumanMessage(content=user_input))
            response = ask_ai(ai_model, history)
            history.append(AIMessage(content=response))
            print(f"AI: {response}")

        except Exception as e:
            print(f"AI: {e}")


def summarize_text(ai_model: BaseChatModel, text: str) -> str:
    """
    Sends a request to summarize the provided text using the given
    LangChain chat model, without you having to format messages manually.

    Args:
        ai_model (BaseChatModel): A LangChain chat model instance,
            such as one returned by `get_model()`.
        text (str): The raw text string to be summarized.

    Returns:
        str: A concise summary of the input text.

    Raises:
        EasyAIError: If the underlying model call fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_model, summarize_text

            model = get_model("anthropic", "claude-sonnet-4-6")
            summary = summarize_text(model, "Long article text here...")
            ```

        === "The Traditional Way"
            ```python
            from langchain_anthropic import ChatAnthropic
            from langchain_core.messages import HumanMessage

            model = ChatAnthropic(model_name="claude-sonnet-4-6")
            summary = model.invoke(
                [HumanMessage(content="Please summarize:\n\nLong article text here...")]
            ).content
            ```
    """

    try:
        prompt = f"Please summarize:\n\n{text}"
        return ask_ai(ai_model, prompt)
    except Exception as e:
        raise EasyAIError(f"\n\n\nERROR: {e}") from None


def translate_text(
    ai_model: BaseChatModel,
    text: str,
    target_lang: str = "English",
) -> str:
    """
    Sends a request to translate the provided text into the target
    language using the given LangChain chat model, without you having
    to format messages manually.

    Args:
        ai_model (BaseChatModel): A LangChain chat model instance,
            such as one returned by `get_model()`.
        text (str): The raw text string to be translated.
        target_lang (str): The name of the language to translate
            into (e.g. "French", "Spanish", "German").
            Defaults to "English".

    Returns:
        str: The translated text.

    Raises:
        EasyAIError: If the underlying model call fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_model, translate_text

            model = get_model("anthropic", "claude-sonnet-4-6")
            translation = translate_text(
                model,
                "Hola mundo",
                target_lang="English",
            )
            ```

        === "The Traditional Way"
            ```python
            from langchain_anthropic import ChatAnthropic
            from langchain_core.messages import HumanMessage

            model = ChatAnthropic(model_name="claude-sonnet-4-6")
            translation = model.invoke([
                HumanMessage(content="Translate to English: Hola mundo")
            ]).content
            ```
    """

    try:
        prompt = f"Translate to {target_lang}:\n\n{text}"
        return ask_ai(ai_model, prompt)
    except Exception as e:
        raise EasyAIError(f"\n\n\nERROR: {e}") from None


def rewrite_text(
    ai_model: BaseChatModel,
    text: str,
    tone: str = "calm",
) -> str:
    """
    Sends a request to change the tone of the provided text,
    without you having to change it manually.

    Args:
        ai_model (BaseChatModel): A LangChain chat model instance,
            such as one returned by `get_model()`.
        text (str): Text whose tone will be changed.
        tone (str): Used to decide the tone for the text that the user
            wants (e.g. calm, angry, nervous, supportive, etc.).
            Defaults to "calm".

    Returns:
        str: The text with its tone changed.

    Raises:
        EasyAIError: If the underlying model call fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_model, rewrite_text

            model = get_model("anthropic", "claude-sonnet-4-6")
            tone = rewrite_text(
                model,
                "hello py-simple-wrap devs",
                "excited",
            )
            ```

        === "The Traditional Way"
            ```python
            from langchain_anthropic import ChatAnthropic
            from langchain_core.messages import HumanMessage

            model = ChatAnthropic(model_name="claude-sonnet-4-6")
            tone = model.invoke([
                HumanMessage(
                    content="Change tone to excited: hello py-simple-wrap devs"
                )
            ]).content
            ```
    """

    try:
        prompt = f"Change tone to {tone}:\n\n{text}"
        return ask_ai(ai_model, prompt)
    except Exception as e:
        raise EasyAIError(f"\n\n\nERROR: {e}") from None


def detect_language(text: str) -> str:
    """
    Guesses which language a piece of text is written in, using
    simple keyword scoring rules, without installing a language-detection
    library or calling an external API.

    Args:
        text (str): The raw text to analyze.

    Returns:
        str: The detected language name (e.g., "English"), or
        "Unknown" if nothing could be confidently identified.

    Raises:
        EasyAIError: If `text` is not a string or is empty/whitespace.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import detect_language

            language = detect_language("Hello, how are you?")
            # "English"
            ```
    """

    if not isinstance(text, str) or not text.strip():
        raise EasyAIError(
            "ERROR: detect_language() requires a non-empty string."
        )

    words = set(re.findall(r"[a-zà-öø-ÿ]+", text.lower()))

    scores = {
        "English": sum(
            word in words
            for word in ["the", "and", "is", "you", "are", "hello"]
        ),
        "Italian": sum(
            word in words
            for word in ["il", "la", "che", "di", "sono", "ciao"]
        ),
        "Spanish": sum(
            word in words
            for word in ["el", "la", "que", "de", "es", "hola"]
        ),
        "French": sum(
            word in words
            for word in ["le", "la", "et", "est", "vous", "bonjour"]
        ),
        "German": sum(
            word in words
            for word in ["der", "die", "und", "ist", "du", "hallo", "wie", "geht", "dir"]
        ),
    }

    best_lang = max(scores, key=scores.get)

    if scores[best_lang] == 0:
        return "Unknown"

    return best_lang


def analyze_sentiment(ai_model: BaseChatModel, text: str) -> str:
    """
    Sends a request to analyze the sentiment of the provided text using the
    given LangChain chat model, returning a brief classification (e.g. Positive,
    Negative, or Neutral).

    Args:
        ai_model (BaseChatModel): A LangChain chat model instance,
            such as one returned by `get_model()`.
        text (str): The raw text string to analyze.

    Returns:
        str: The sentiment classification of the text.

    Raises:
        EasyAIError: If the underlying model call fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_model, analyze_sentiment

            model = get_model("anthropic", "claude-sonnet-4-6")
            sentiment = analyze_sentiment(
                model,
                "I absolutely love this new tool!",
            )
            ```

        === "The Traditional Way"
            ```python
            from langchain_anthropic import ChatAnthropic
            from langchain_core.messages import HumanMessage

            model = ChatAnthropic(model_name="claude-sonnet-4-6")
            sentiment = model.invoke([
                HumanMessage(
                    content=(
                        "Analyze the sentiment of the following text and "
                        "respond with a single word "
                        "(e.g., Positive, Negative, Neutral):\n\n"
                        "I absolutely love this new tool!"
                    )
                )
            ]).content
            ```
    """

    try:
        prompt = (
            "Analyze the sentiment of the following text and respond with "
            "a single word (e.g., Positive, Negative, Neutral):\n\n"
            f"{text}"
        )
        return ask_ai(ai_model, prompt)
    except Exception as e:
        raise EasyAIError(f"\n\n\nERROR: {e}") from None


def chunk_text(text: str, max_chars: int = 500) -> list[str]:
    """
    Split text into pieces that fit inside a character limit.

    Useful before sending a long note to an AI model that only accepts
    a short prompt. Words stay whole when they fit. A single word longer
    than the limit is split so nothing is dropped.

    Args:
        text (str): The text to split.
        max_chars (int, optional): Maximum characters in each piece.
            Defaults to `500`.

    Returns:
        list[str]: The pieces, in order. An empty string returns an
            empty list.

    Raises:
        EasyAIError: If `text` is not a string or `max_chars` is less
            than 1.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import chunk_text

            pieces = chunk_text("Pack a lunch and a notebook", max_chars=16)
            ```

        === "The Traditional Way"
            ```python
            text = "Pack a lunch and a notebook"
            words = text.split()
            pieces = []
            current = ""
            for word in words:
                candidate = word if not current else f"{current} {word}"
                if len(candidate) <= 16:
                    current = candidate
                else:
                    pieces.append(current)
                    current = word
            if current:
                pieces.append(current)
            ```
    """
    if not isinstance(text, str):
        raise EasyAIError("\n\n\nERROR: text must be a string.") from None
    if not isinstance(max_chars, int) or isinstance(max_chars, bool) or max_chars < 1:
        raise EasyAIError(
            "\n\n\nERROR: max_chars must be an integer of at least 1."
        ) from None
    if text == "":
        return []

    pieces: list[str] = []
    current = ""
    for word in text.split():
        if len(word) > max_chars:
            if current:
                pieces.append(current)
                current = ""
            for start in range(0, len(word), max_chars):
                pieces.append(word[start : start + max_chars])
            continue

        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            pieces.append(current)
            current = word

    if current:
        pieces.append(current)
    return pieces


class EasyAgent:
    def __init__(
        self,
        prompt_path: str,
        toolbox: list | None = None,
        history: list | None = None,
    ):
        self.toolbox = toolbox
        self.history = history

        self.master_prompt = None
        self.init_prompt(prompt_path)

    def init_prompt(self, path):
        if path.split(".")[-1].lower() == "txt":
            try:
                with open(path, "r", encoding="utf-8") as f:
                    prompt = f.read().rstrip()

                self.master_prompt = prompt

            except (
                FileNotFoundError,
                PermissionError,
                UnicodeDecodeError,
            ) as e:
                raise EasyAIError(f"\n\n\nERROR: {e}") from None
        else:
            raise EasyAIError(
                f"\n\n\nERROR: {path} not supported. "
                "Only `.txt` files are supported."
            ) from None

def summarize_text(ai_model, text: str, max_words: int = 50) -> str:
    """
    Sends a request to summarize the provided text in a specified number of words
    using the given LangChain chat model.

    Args:
        ai_model (BaseChatModel): A LangChain chat model instance,
            such as one returned by `get_model()`.
        text (str): The raw text string to summarize.
        max_words (int): The maximum number of words for the summary. Defaults to 50.

    Returns:
        str: The summarized text.

    Raises:
        EasyAIError: If the underlying model call fails.

    Example:
        === "The Py_simple Way"
            ```python
            from py_simple import get_model, summarize_text

            model = get_model("anthropic", "claude-sonnet-4-6")
            summary = summarize_text(
                model,
                "Long article text here...",
                max_words=20
            )
            ```

        === "The Traditional Way"
            ```python
            from langchain_anthropic import ChatAnthropic
            from langchain_core.messages import HumanMessage

            model = ChatAnthropic(model_name="claude-sonnet-4-6")
            summary = model.invoke([
                HumanMessage(
                    content=(
                        "Summarize the following text in under 20 words:\\n\\n"
                        "Long article text here..."
                    )
                )
            ]).content
            ```
    """
    try:
        prompt = (
            f"Summarize the following text in under {max_words} words:\n\n"
            f"{text}"
        )
        return ask_ai(ai_model, prompt)
    except Exception as e:
        raise EasyAIError(f"\n\n\nERROR: {e}") from None
