import re
with open('tests/test_async.py', 'r') as f:
    content = f.read()

new_test = """def test_run_with_fallback_success():
    def primary(a, b): return a + b
    def fallback(a, b): return a * b
    
    import asyncio
    name, result = asyncio.run(run_with_fallback(primary, fallback, 2, 3))
    assert name == "primary"
    assert result == 5

def test_run_with_fallback_uses_fallback():
    def primary(a, b): raise ValueError("Fail")
    def fallback(a, b): return a + b
    
    import asyncio
    name, result = asyncio.run(run_with_fallback(primary, fallback, 2, 3))
    assert name == "fallback"
    assert result == 5

def test_run_with_fallback_both_fail():
    def primary(a, b): raise ValueError("Fail 1")
    def fallback(a, b): raise ValueError("Fail 2")
    
    import asyncio
    with pytest.raises(EasyAsyncError, match="Fail 2"):
        asyncio.run(run_with_fallback(primary, fallback, 2, 3))
"""
content = re.sub(r'async def test_run_with_fallback_success.*?await run_with_fallback\(primary, fallback, 2, 3\)', new_test, content, flags=re.DOTALL)
with open('tests/test_async.py', 'w') as f:
    f.write(content)
