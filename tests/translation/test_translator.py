"""
Unit tests for query translation engine.
"""

import pytest
from src.translation.translator import QueryTranslator
from src.utils.exceptions import TranslationError


class TestQueryTranslator:
    """Test QueryTranslator functionality."""
    
    @pytest.fixture
    def translator(self):
        """Create a QueryTranslator instance."""
        return QueryTranslator()
    
    def test_translate_getdate(self, translator):
        """Test GETDATE() translation to CURRENT_TIMESTAMP()."""
        query = "SELECT GETDATE()"
        result = translator.translate(query)
        assert "CURRENT_TIMESTAMP()" in result
        assert "GETDATE()" not in result
    
    def test_translate_len(self, translator):
        """Test LEN() translation to LENGTH()."""
        query = "SELECT LEN(name) FROM users"
        result = translator.translate(query)
        assert "LENGTH(" in result
        assert "LEN(" not in result
    
    def test_translate_isnull(self, translator):
        """Test ISNULL() translation to IFNULL()."""
        query = "SELECT ISNULL(value, 0) FROM table"
        result = translator.translate(query)
        assert "IFNULL(" in result
        assert "ISNULL(" not in result
    
    def test_translate_top(self, translator):
        """Test TOP clause translation to LIMIT."""
        query = "SELECT TOP 10 * FROM users"
        result = translator.translate(query)
        assert "LIMIT 10" in result.upper() or "LIMIT" in result.upper()
    
    def test_translate_multiple_replacements(self, translator):
        """Test query with multiple translation rules."""
        query = "SELECT TOP 5 * FROM users WHERE LEN(name) > 5 AND GETDATE() > created_date"
        result = translator.translate(query)
        assert "LIMIT" in result.upper() or "LIMIT 5" in result.upper()
        assert "LENGTH(" in result
        assert "CURRENT_TIMESTAMP()" in result
    
    def test_translate_preserves_original_structure(self, translator):
        """Test that translation preserves query structure."""
        query = "SELECT column1, column2 FROM table WHERE condition = 'value'"
        result = translator.translate(query)
        assert "SELECT" in result
        assert "FROM" in result
        assert "WHERE" in result
    
    def test_validate_translation_placeholder(self, translator):
        """Test validation method exists (placeholder implementation)."""
        query = "SELECT * FROM table"
        result = translator.validate_translation(query)
        # Currently returns True as placeholder
        assert isinstance(result, bool)

