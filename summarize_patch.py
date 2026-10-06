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
