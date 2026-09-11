"""
easy_ai wraps common LangChain functionality to make it easier to use.
"""

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import SecretStr


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

        api_key = SecretStr(api_key) if api_key is not None else None
        model = ChatAnthropic(
            model_name=model_name, api_key=api_key, timeout=timeout, stop=None
        )
        return model

    elif provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        model = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
        return model

    elif provider == "mistral":
        from langchain_mistralai import ChatMistralAI

        model = ChatMistralAI(api_key=api_key, model_name=model_name)
        return model

    else:
        raise EasyAIError(f"\n\n\nERROR: Provider '{provider}' is not supported yet!")


def ask_ai(
    ai_model: BaseChatModel, question: str | list
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
            summary = model.invoke([HumanMessage(content="Please summarize:\n\nLong article text here...")]).content
            ```
    """
    try:
        prompt = f"Please summarize:\n\n{text}"
        return ask_ai(ai_model, prompt)
    except Exception as e:
        raise EasyAIError(f"\n\n\nERROR: {e}") from None


def translate_text(
    ai_model: BaseChatModel, text: str, target_lang: str = "English"
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
            translation = translate_text(model, "Hola mundo", target_lang="English")
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


# ⚠️️ WORK IN PROGRESS ⚠️
# This class will eventually take the complexity of setting up an agent
# with LangChain and turning it into something simple.


class EasyAgent:
    def __init__(
        self, prompt_path: str, toolbox: list | None = None, history: list | None = None
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
            except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
                raise EasyAIError(f"\n\n\nERROR: {e}") from None
        else:
            raise EasyAIError(
                f"\n\n\nERROR: {path} not supported. Only `.txt` files are supported."
            ) from None
