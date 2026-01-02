# Dependencies Documentation

## Core Dependencies

### Database Connectivity

#### pyodbc (SQL Server)
- **Version**: >=4.0.39, <5.0.0
- **Purpose**: SQL Server database connectivity
- **Alternative**: `pymssql` (not used, pyodbc is more widely supported)
- **System Requirements**: 
  - Windows: ODBC Driver for SQL Server (usually pre-installed)
  - macOS: `brew install unixodbc` and Microsoft ODBC Driver
  - Linux: Install unixODBC and Microsoft ODBC Driver
- **Documentation**: https://github.com/mkleehammer/pyodbc

#### snowflake-connector-python
- **Version**: >=3.0.0, <4.0.0
- **Purpose**: Snowflake database connectivity
- **Authentication Methods Supported**:
  - Username/password
  - Key-pair authentication
  - SSO (Single Sign-On)
- **Documentation**: https://docs.snowflake.com/en/developer-guide/python-connector

### Data Manipulation

#### pandas
- **Version**: >=1.5.0, <3.0.0
- **Purpose**: Data manipulation and comparison for query results
- **Compatibility**: Works with Python 3.8+
- **Documentation**: https://pandas.pydata.org/

### Configuration

#### dynaconf
- **Version**: >=3.2.0, <4.0.0
- **Purpose**: Advanced configuration management with multiple sources, environment variable support, and validation
- **Features**:
  - Multiple config file formats (JSON, YAML, TOML, Python)
  - Environment variable overrides
  - Built-in validation
  - Dot-notation access
  - .env file support
- **Documentation**: https://www.dynaconf.com/

#### pyyaml
- **Version**: >=6.0, <7.0
- **Purpose**: YAML configuration file parsing (used by dynaconf)
- **Documentation**: https://pyyaml.org/

## Standard Library Modules (No Installation Required)

The following modules are part of Python's standard library and do not require installation:

- **tkinter**: GUI framework (built-in with Python, though may need separate installation on Linux)
- **configparser**: Configuration file parsing (built-in)
- **concurrent.futures**: Parallel execution support (built-in)
- **logging**: Logging infrastructure (built-in)
- **json**: JSON file handling (built-in)
- **sqlite3**: SQLite database (built-in, if needed for local storage)

## Development Dependencies

### Testing
- **pytest**: >=7.0.0, <8.0.0 - Testing framework
- **pytest-cov**: >=4.0.0, <5.0.0 - Coverage reporting

### Code Quality
- **black**: >=23.0.0, <24.0.0 - Code formatter
- **flake8**: >=6.0.0, <7.0.0 - Linting tool

## Installation

### Install Core Dependencies
```bash
pip install -r requirements.txt
```

### Install with Development Dependencies
```bash
pip install -e ".[dev]"
```

Or using requirements.txt (includes dev dependencies):
```bash
pip install -r requirements.txt
```

## Version Compatibility

- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Operating Systems**: Windows, macOS, Linux
- **Database Versions**:
  - SQL Server: 2012 and later
  - Snowflake: All supported versions

## Known Issues and Workarounds

### pyodbc on macOS
If you encounter issues with pyodbc on macOS, you may need to:
```bash
brew install unixodbc
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql17
```

### tkinter on Linux
On some Linux distributions, tkinter may need to be installed separately:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

## Dependency Updates

To update dependencies, review compatibility and test thoroughly:
1. Check for security updates: `pip list --outdated`
2. Review changelogs for breaking changes
3. Update version constraints in `requirements.txt` and `pyproject.toml`
4. Run tests to verify compatibility

