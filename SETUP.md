# Setup Guide

## Python Environment Setup

### Prerequisites
- Python 3.8 or higher (verified: Python 3.10.5)

### Virtual Environment

A virtual environment has been created in the `venv/` directory.

#### Activate the virtual environment:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

#### Deactivate:
```bash
deactivate
```

### Installing Dependencies

Once the virtual environment is activated:

#### Install Core Dependencies
```bash
pip install -r requirements.txt
```

#### Install with Development Tools
```bash
pip install -r requirements-dev.txt
```

#### Install as Editable Package (Recommended for Development)
```bash
pip install -e ".[dev]"
```

**Why editable install?** The `-e` flag creates an "editable" or "development" install:
- **Live code changes**: Changes to source code in `src/` are immediately available without reinstalling
- **No reinstall needed**: You can edit code and run it directly, making development faster
- **Proper imports**: The package is installed in a way that allows Python to import from `src/` correctly
- **Includes dev tools**: The `[dev]` extra installs pytest, black, flake8, etc.

This is the preferred method when actively developing the project.

### Verify Installation

Check that dependencies are installed:
```bash
pip list
```

You should see:
- pyodbc
- snowflake-connector-python
- pandas
- pyyaml
- pytest (if dev dependencies installed)
- black (if dev dependencies installed)
- flake8 (if dev dependencies installed)

### Next Steps

1. ✅ Virtual environment created
2. ✅ Dependencies defined (install with commands above)
3. Follow the implementation plan in `implementation.md`

For detailed dependency information, see `DEPENDENCIES.md`.

