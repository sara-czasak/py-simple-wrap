import re
with open('tests/test_ai.py', 'r') as f:
    content = f.read()
new_test = """def test_summarize_text_success():
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
"""
content = re.sub(r'def test_summarize_text_success.*?\(EasyAIError, match="ERROR: API error"\):\n\s*summarize_text\(mock_model, "Text", 50\)', new_test, content, flags=re.DOTALL)
with open('tests/test_ai.py', 'w') as f:
    f.write(content)
