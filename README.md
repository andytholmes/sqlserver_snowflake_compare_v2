# SQL Server to Snowflake Query Performance Comparison Tool

A Python-based tool to compare query performance between SQL Server and Snowflake databases by translating SQL Server queries to Snowflake syntax, executing them on both platforms, and analyzing performance metrics with a graphical user interface.

## Project Overview

This tool enables automated comparison of query performance between SQL Server and Snowflake by:

- **Translating** SQL Server queries to Snowflake-compatible syntax
- **Executing** queries on both platforms with configurable parallelism and repetition
- **Comparing** performance metrics and validating data consistency
- **Providing** visual insights through an interactive UI
- **Storing** all test configurations, translations, and results in a centralized SQL Server database

## Features

- 🔄 **Query Translation**: Automatic translation of SQL Server queries to Snowflake syntax
- ⚡ **Parallel Execution**: Configurable parallel execution (1-50 concurrent queries)
- 🔁 **Repeat Testing**: Configurable repeat count per query (1-100 iterations)
- 📊 **Performance Analysis**: Comprehensive comparison metrics and statistical analysis
- 💾 **Centralized Storage**: All results stored in SQL Server database
- 🎨 **Interactive UI**: Graphical interface for configuration and visualization
- 📝 **Detailed Logging**: Comprehensive logging with file rotation

## Requirements

- Python 3.8 or higher
- SQL Server (for test run database and test target database)
- Snowflake account
- ODBC Driver for SQL Server (for pyodbc)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/andytholmes/sqlserver_snowflake_compare_v2.git
cd sqlserver_snowflake_compare_v2
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install as an editable package (recommended for development):

```bash
pip install -e ".[dev]"
```

### 4. Set Up Database Schema

Execute the SQL schema scripts in `scripts/schema/` on your SQL Server test run database:

```bash
# Option 1: Run master script (in SQL Server Management Studio)
sqlcmd -S server_name -d database_name -i scripts/schema/00_create_all_tables.sql

# Option 2: Run individual scripts in order
sqlcmd -S server_name -d database_name -i scripts/schema/01_create_config_table.sql
sqlcmd -S server_name -d database_name -i scripts/schema/02_create_query_repository.sql
# ... and so on
```

### 5. Configure the Application

1. Copy the configuration template:
   ```bash
   cp config/config_template.json config/config.json
   ```

2. Edit `config/config.json` with your settings (non-sensitive values)

3. Create `.env` file from template:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` with your database credentials

## Quick Start

### 1. Start the Application

```bash
python -m src.ui.main
```

Or if installed as a package:

```bash
sqlserver-snowflake-compare
```

### 2. Configure Connections

- Set up SQL Server test run database connection
- Set up SQL Server test target database connection
- Set up Snowflake connection

### 3. Load Queries

- Import SQL Server queries into the QueryRepository
- Review and validate translations

### 4. Run Tests

- Configure test parameters (parallel workers, repeat count)
- Start test execution
- Monitor progress in real-time

### 5. View Results

- Review performance comparisons
- Analyze statistical metrics
- Export results as needed

## Development Setup

### Project Structure

```
sqlserver_snowflake_compare_v2/
├── src/                    # Main application code
│   ├── database/          # Database connection & schema modules
│   ├── translation/       # Query translation engine
│   ├── execution/         # Query execution engine
│   ├── analysis/          # Comparison & analysis logic
│   ├── ui/                # User interface components
│   └── utils/             # Utility functions & helpers
├── config/                # Configuration files
├── scripts/               # Database schema scripts
│   └── schema/           # SQL schema creation scripts
├── tests/                 # Unit & integration tests
├── docs/                  # Documentation
└── logs/                  # Log files
```

### Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=src --cov-report=html
```

### Code Formatting

```bash
black src/
```

### Linting

```bash
flake8 src/
```

## Configuration

The application uses JSON configuration files and environment variables. See:

- `config/config_template.json` - Configuration template
- `.env.example` - Environment variables template
- `config/README.md` - Configuration documentation

## Documentation

- [Architecture Documentation](docs/architecture.md) - System architecture overview
- [Development Guidelines](docs/development.md) - Development best practices
- [API Documentation](docs/api.md) - API reference (coming soon)
- [Dependencies](DEPENDENCIES.md) - Dependency documentation
- [Setup Guide](SETUP.md) - Detailed setup instructions

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Status

**Current Phase**: Phase 0 - Project Initialization (Steps 1-7 completed)

See [implementation.md](implementation.md) for detailed progress tracking.
