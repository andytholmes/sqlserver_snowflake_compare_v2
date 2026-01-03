# Development Guidelines

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git
- SQL Server (for test run database)
- Snowflake account (for testing)
- Virtual environment (venv)

### Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/andytholmes/sqlserver_snowflake_compare_v2.git
   cd sqlserver_snowflake_compare_v2
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

### Python Style Guide

- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Maximum line length: 100 characters (configured in black)
- Use descriptive variable and function names

### Code Formatting

We use `black` for code formatting:

```bash
black src/
```

### Linting

We use `flake8` for linting:

```bash
flake8 src/
```

### Type Checking

Consider using `mypy` for type checking (optional):

```bash
mypy src/
```

## Project Structure

```
sqlserver_snowflake_compare_v2/
├── src/                    # Source code
│   ├── database/          # Database modules
│   ├── translation/       # Translation engine
│   ├── execution/         # Execution engine
│   ├── analysis/          # Analysis modules
│   ├── ui/                # UI components
│   └── utils/             # Utilities
├── tests/                 # Test files
├── config/                # Configuration files
├── scripts/               # Utility scripts
├── docs/                  # Documentation
└── logs/                  # Log files (gitignored)
```

## Module Organization

### Module Naming

- Use lowercase with underscores: `query_executor.py`
- Match module name to primary class when possible
- Keep modules focused on a single responsibility

### Class Naming

- Use PascalCase: `QueryExecutor`
- Be descriptive and specific
- Avoid abbreviations unless widely understood

### Function Naming

- Use lowercase with underscores: `execute_query()`
- Use verbs for functions that perform actions
- Use nouns for functions that return values

## Testing

### Test Structure

- Mirror `src/` structure in `tests/`
- Test file naming: `test_<module_name>.py`
- Use pytest fixtures for common setup

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_translator.py

# Run specific test
pytest tests/test_translator.py::test_translate_getdate
```

### Writing Tests

```python
import pytest
from src.translation.translator import QueryTranslator

def test_translate_getdate():
    """Test GETDATE() translation to CURRENT_TIMESTAMP()."""
    translator = QueryTranslator()
    query = "SELECT GETDATE()"
    result = translator.translate(query)
    assert "CURRENT_TIMESTAMP()" in result
```

## Logging

### Using the Logger

```python
import logging

logger = logging.getLogger(__name__)

def my_function():
    logger.debug("Detailed debugging information")
    logger.info("General information")
    logger.warning("Warning message")
    logger.error("Error occurred")
```

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors that may stop execution

## Error Handling

### Exception Usage

Use specific exception types from `src.utils.exceptions`:

```python
from src.utils.exceptions import DatabaseConnectionError, QueryExecutionError

try:
    connection.connect()
except Exception as e:
    raise DatabaseConnectionError(f"Connection failed: {e}") from e
```

### Best Practices

- Always use specific exception types
- Include context in error messages
- Use `from e` when re-raising exceptions
- Log errors before raising

## Configuration Management

### Accessing Configuration

```python
from src.utils.config_loader import ConfigLoader

config = ConfigLoader()
parallel_workers = config.settings.get("execution.parallel_workers", 10)
```

### Adding New Configuration

1. Add to `config/config_template.json`
2. Document in `config/README.md`
3. Update configuration loader if needed

## Database Operations

### Connection Management

Always use context managers:

```python
from src.database.connections import SQLServerConnection

conn = SQLServerConnection(server="localhost", database="TestDB")
with conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table")
```

### Schema Operations

Use the SchemaManager for schema operations:

```python
from src.database.schema import SchemaManager
from src.database.connections import SQLServerConnection

conn = SQLServerConnection(...)
schema_mgr = SchemaManager(conn)
if schema_mgr.table_exists("TestRuns"):
    print("Table exists")
```

## Git Workflow

### Branch Naming

- `main`: Production-ready code
- `feature/<name>`: New features
- `bugfix/<name>`: Bug fixes
- `docs/<name>`: Documentation updates

### Commit Messages

Follow conventional commit format:

```
type(scope): subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Requests

- Create feature branch from `main`
- Write clear PR description
- Ensure all tests pass
- Request review before merging

## Documentation

### Code Documentation

- Use docstrings for all public functions and classes
- Follow Google-style docstrings
- Include parameter descriptions and return values
- Add examples for complex functions

### Example

```python
def translate(self, sqlserver_query: str) -> str:
    """
    Translate SQL Server query to Snowflake syntax.
    
    Args:
        sqlserver_query: Original SQL Server query
        
    Returns:
        Translated Snowflake query
        
    Raises:
        TranslationError: If translation fails
        
    Example:
        >>> translator = QueryTranslator()
        >>> translator.translate("SELECT GETDATE()")
        'SELECT CURRENT_TIMESTAMP()'
    """
```

## Performance Considerations

- Use connection pooling for database connections
- Implement caching for translations
- Use batch operations when possible
- Profile code to identify bottlenecks
- Consider async/await for I/O operations

## Security Best Practices

- Never commit credentials to version control
- Use environment variables for sensitive data
- Validate all user inputs
- Use parameterized queries to prevent SQL injection
- Keep dependencies up to date

## Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Dynaconf Documentation](https://www.dynaconf.com/)

