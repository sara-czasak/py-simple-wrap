async def run_with_fallback(primary_func, fallback_func, *args) -> tuple:
    """
    Attempts to run the primary function asynchronously. If it fails, runs the
    fallback function instead.

    Raises EasyAsyncError if the fallback function also fails.

    Args:
        primary_func (callable): The main function to execute.
        fallback_func (callable): The function to execute if the primary fails.
        *args: Positional arguments to pass to both functions.

    Returns:
        tuple: A tuple containing `(successful_func.__name__, result)`.

    Example:
        === "The Py_simple Way"
            ```python
            import asyncio
            from py_simple import run_with_fallback

            def risky_add(a, b):
                raise ValueError("Oops")

            def safe_add(a, b):
                return a + b

            async def main():
                return await run_with_fallback(risky_add, safe_add, 3, 5)

            asyncio.run(main())  # -> ("safe_add", 8)
            ```

        === "The Traditional Way"
            ```python
            import asyncio

            def risky_add(a, b):
                raise ValueError("Oops")

            def safe_add(a, b):
                return a + b

            async def main():
                loop = asyncio.get_running_loop()
                try:
                    result = await loop.run_in_executor(None, risky_add, 3, 5)
                    return (risky_add.__name__, result)
                except Exception:
                    result = await loop.run_in_executor(None, safe_add, 3, 5)
                    return (safe_add.__name__, result)

            asyncio.run(main())
            ```
    """
    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(None, primary_func, *args)
        return (primary_func.__name__, result)
    except Exception:
        try:
            result = await loop.run_in_executor(None, fallback_func, *args)
            return (fallback_func.__name__, result)
        except Exception as e:
            raise EasyAsyncError(f"\n\n\nERROR: {e}") from None
