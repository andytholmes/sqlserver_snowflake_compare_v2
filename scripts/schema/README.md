# Database Schema Scripts

This directory contains SQL Server scripts to create the database schema for the SQL Server to Snowflake Query Performance Comparison Tool.

## Schema Overview

The database schema consists of 5 main tables:

1. **ConfigTable** - Stores connection configurations
2. **QueryRepository** - Stores SQL Server queries and their Snowflake translations
3. **TestRuns** - Stores test run metadata and configuration
4. **TestResults** - Stores individual query execution results
5. **ComparisonResults** - Stores aggregated comparison results

## Scripts

### Individual Table Scripts

- `01_create_config_table.sql` - Creates ConfigTable
- `02_create_query_repository.sql` - Creates QueryRepository
- `03_create_test_runs.sql` - Creates TestRuns
- `04_create_test_results.sql` - Creates TestResults (with foreign keys)
- `05_create_comparison_results.sql` - Creates ComparisonResults (with foreign keys)

### Master Script

- `00_create_all_tables.sql` - Master script that runs all table creation scripts in order

## Usage

### Option 1: Run Individual Scripts

Run each script in order (01 through 05) using SQL Server Management Studio or sqlcmd:

```bash
sqlcmd -S server_name -d database_name -i 01_create_config_table.sql
sqlcmd -S server_name -d database_name -i 02_create_query_repository.sql
# ... and so on
```

### Option 2: Run Master Script

Run the master script which includes all table creation scripts:

```bash
sqlcmd -S server_name -d database_name -i 00_create_all_tables.sql
```

**Note:** The master script uses `:r` commands which work in SQL Server Management Studio. For sqlcmd, you may need to run scripts individually.

## Table Relationships

```
TestRuns (1) ──< (many) TestResults
QueryRepository (1) ──< (many) TestResults
QueryRepository (1) ──< (many) ComparisonResults
TestRuns (1) ──< (many) ComparisonResults
```

## Indexes

Each table includes appropriate indexes for:
- Foreign key lookups
- Common query patterns
- Performance optimization

## Constraints

- Primary keys on all tables
- Foreign key relationships with CASCADE delete
- Check constraints for data validation
- Unique constraints where appropriate

## Notes

- All scripts are idempotent (can be run multiple times safely)
- Scripts check for table existence before creating
- Indexes are created conditionally to avoid errors on re-runs
- Default values are set for common fields
- Timestamps use DATETIME2 for better precision

