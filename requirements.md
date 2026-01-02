# SQL Server to Snowflake Query Performance Comparison Tool

## Project Overview

A Python-based tool to compare query performance between SQL Server and Snowflake databases by translating SQL Server queries to Snowflake syntax, executing them on both platforms, and analyzing performance metrics with a graphical user interface.

## Core Objectives

- Translate SQL Server queries to Snowflake-compatible syntax
- Execute queries on both platforms with configurable parallelism and repetition
- Compare performance metrics and validate data consistency
- Provide visual insights through an interactive UI
- Store all test configurations, translations, and results in a centralized SQL Server database

## Technical Requirements

### 1. Python Environment

- **Python Version**: 3.8+ (keep dependencies minimal)
- **Core Libraries**:
  - `pyodbc` or `pymssql` for SQL Server connectivity
  - `snowflake-connector-python` for Snowflake connectivity
  - Lightweight UI framework (e.g., `tkinter` for simplicity, or `streamlit` for richer visualization)
  - `pandas` for data manipulation and comparison
  - Standard library modules for concurrency (`concurrent.futures`)

### 2. Database Connectivity

#### SQL Server Connections

- **Test Run Database**: Separate connection to store test metadata, configurations, and results
- **Test Target Database**: Connection to the actual SQL Server database being tested
- **Authentication**: Username/password
- **Connection Parameters**: Configurable via UI

#### Snowflake Connection

- **Authentication Methods**: Support multiple options
  - Username/password
  - Key-pair authentication
  - SSO (Single Sign-On)
- **Connection Parameters**: Configurable via UI
- **Account Details**: Account identifier, warehouse, database, schema, role

### 3. Query Management System

#### Test Run Database Schema

Design tables in SQL Server to store:

**ConfigTable**:

- connection_id (PK)
- platform (SQL Server/Snowflake)
- connection_string
- authentication_type
- created_date
- is_active

**QueryRepository**:

- query_id (PK)
- query_name
- sqlserver_query (original SQL)
- snowflake_query (translated SQL)
- query_complexity (simple/medium/complex)
- translation_validated (boolean)
- translation_date
- description
- is_active

**TestRuns**:

- test_run_id (PK)
- run_name
- start_time
- end_time
- status (pending/running/completed/failed)
- parallel_workers
- repeat_count
- queries_executed
- created_by

**TestResults**:

- result_id (PK)
- test_run_id (FK)
- query_id (FK)
- platform (SQL Server/Snowflake)
- execution_number (for repeats)
- execution_time_ms
- row_count
- status (success/error)
- error_message
- execution_plan (optional)
- timestamp

**ComparisonResults**:

- comparison_id (PK)
- test_run_id (FK)
- query_id (FK)
- sqlserver_avg_time_ms
- snowflake_avg_time_ms
- time_difference_ms
- time_difference_percent
- row_count_match (boolean)
- sqlserver_row_count
- snowflake_row_count
- performance_winner (SQL Server/Snowflake/Tie)

### 4. Query Translation Engine

#### Translation Rules

Focus on common SQL Server to Snowflake syntax conversions:

- **CASE statements**: Generally compatible, minimal changes
- **CTEs (Common Table Expressions)**: Compatible syntax
- **LAG/LEAD functions**: Compatible with minor syntax adjustments
- **PARTITION BY clauses**: Compatible
- **Date/Time functions**: Convert SQL Server functions to Snowflake equivalents
  - `GETDATE()` → `CURRENT_TIMESTAMP()`
  - `DATEADD()` → `DATEADD()`
  - `DATEDIFF()` → `DATEDIFF()`
- **String functions**: Convert as needed
  - `LEN()` → `LENGTH()`
  - `ISNULL()` → `IFNULL()` or `COALESCE()`
- **Temp tables**: Convert `#temp` to Snowflake temporary table syntax
- **TOP clause**: Convert to `LIMIT`
- **Schema qualification**: Adjust for Snowflake’s database.schema.table format

#### Translation Process

1. **Pre-execution Phase**: Translate all queries before any tests run
1. **Validation Steps**:
- Syntax validation against Snowflake
- Store both original and translated queries in QueryRepository
- Flag translation_validated = TRUE when successful
- Manual review option for complex translations
1. **Translation Storage**: Persist translations for reuse across test runs

### 5. Query Execution Engine

#### Execution Configuration

- **Parallel Execution**: Configurable worker threads (1-50 concurrent queries)
- **Repeat Execution**: Configurable repeat count per query (1-100 iterations)
- **Execution Order**: Process queries from QueryRepository where is_active = TRUE

#### Execution Flow

1. Load active queries from QueryRepository
1. For each query, for each repeat iteration:
- Execute SQL Server query on test target database
- Execute Snowflake translated query on Snowflake
- Capture metrics for both executions
1. Handle parallel execution based on configured worker count
1. Store individual results in TestResults table

#### Metrics Collection

- **Row Count**: Total rows returned by query
- **Execution Duration**: Time in milliseconds from query start to completion
- **Additional Diagnostics** (if available):
  - Query compilation time
  - Execution plan details
  - Bytes scanned (Snowflake)
  - Wait statistics (SQL Server)
  - Error messages and stack traces

### 6. Comparison and Analysis

#### Data Validation

- Compare row counts between SQL Server and Snowflake results
- Flag mismatches in ComparisonResults table
- Optionally sample actual data to verify content matches

#### Performance Analysis

- Calculate average execution time across all repeats
- Compute time differences (absolute and percentage)
- Identify performance winner for each query
- Aggregate statistics across all queries in test run

#### Statistical Insights

- Min/max/median execution times
- Standard deviation to identify consistency
- Outlier detection for anomalous runs
- Query complexity correlation with performance difference

### 7. User Interface Requirements

#### UI Framework

- Use `tkinter` for simplicity or `streamlit` for richer visualization
- Responsive design for configuration and monitoring

#### UI Components

**Connection Configuration Panel**:

- SQL Server test run database connection
- SQL Server test target database connection
- Snowflake connection with authentication method selection
- Test connection buttons
- Save/load connection profiles

**Test Configuration Panel**:

- Test run name input
- Parallel workers slider/input (1-50)
- Repeat count slider/input (1-100)
- Query selection (all active or specific subset)
- Start/Stop/Pause buttons

**Translation Management Panel**:

- View original SQL Server queries
- View translated Snowflake queries side-by-side
- Translation validation status indicators
- Manual re-translation trigger
- Validation test button

**Execution Progress Panel**:

- Real-time progress bar
- Current query being executed
- Queries completed / total queries
- Elapsed time
- Estimated time remaining
- Live log of execution events

**Results Visualization Panel**:

- **Summary Dashboard**:
  - Total queries executed
  - Overall average performance comparison
  - Success/failure counts
  - Row count match percentage
- **Query-level Comparison Chart**:
  - Bar chart comparing SQL Server vs Snowflake execution times
  - Color-coded by performance winner
  - Sortable by various metrics
- **Detailed Results Table**:
  - Query name, complexity, execution times, row counts
  - Drill-down to see individual execution results
  - Export to CSV capability
- **Time Series Visualization**:
  - Line chart showing execution time trends across repeats
  - Identify performance consistency and outliers

**Historical Analysis Panel**:

- View past test runs
- Compare results across different test runs
- Trend analysis over time

### 8. Workflow and Process Flow

#### Phase 1: Setup and Translation

1. User configures connections via UI
1. Tool connects to test_run database
1. Loads queries from QueryRepository
1. Initiates translation process for untranslated queries
1. Validates translations against Snowflake
1. Updates QueryRepository with translated queries and validation status
1. User reviews translations (optional manual review)

#### Phase 2: Test Execution

1. User configures test parameters (parallel workers, repeat count)
1. User starts test run
1. Tool creates TestRun record
1. Executes queries according to configuration
1. Stores results in TestResults table
1. Updates progress in UI real-time
1. Handles errors gracefully and continues execution

#### Phase 3: Analysis and Reporting

1. Tool calculates comparison metrics
1. Populates ComparisonResults table
1. Updates TestRun record with completion status
1. Displays results in UI visualizations
1. User explores results and exports as needed

### 9. Error Handling and Logging

#### Error Scenarios

- Connection failures to SQL Server or Snowflake
- Query syntax errors post-translation
- Query timeout handling
- Data type mismatches
- Authentication failures

#### Logging Requirements

- Detailed execution logs stored in database or file
- Error stack traces for debugging
- Performance metrics logging
- User actions audit trail
- Log levels: DEBUG, INFO, WARNING, ERROR

### 10. Scale and Performance Considerations

#### Expected Scale

- **Query Volume**: ~500 queries per test run
- **Parallel Execution**: 1-50 concurrent queries
- **Repeat Iterations**: 1-100 per query
- **Total Executions**: Up to 50,000 individual query executions per test run

#### Performance Optimizations

- Connection pooling for database connections
- Async execution where possible
- Efficient data retrieval (fetch only necessary metrics)
- Batch inserts for results storage
- UI responsiveness with background threading
- Progress updates without UI blocking

### 11. Configuration and Extensibility

#### Configuration File

Store default settings in config file (JSON/YAML):

- Default connection parameters (without sensitive credentials)
- Default parallel worker count
- Default repeat count
- UI preferences
- Logging configuration

#### Extensibility Points

- Pluggable translation rules for additional SQL patterns
- Custom metric collectors
- Export formats (CSV, JSON, HTML, PDF)
- Additional database platform support (future: PostgreSQL, MySQL)

## Deliverables

### Phase 1: Foundation

1. Database schema scripts for test_run database
1. Connection management module
1. Basic UI shell with connection configuration
1. Query loader from QueryRepository

### Phase 2: Translation

1. SQL Server to Snowflake translation engine
1. Translation validation logic
1. Translation management UI panel
1. Updated QueryRepository with translated queries

### Phase 3: Execution

1. Query execution engine with parallel processing
1. Metrics collection framework
1. Results storage in TestResults table
1. Execution progress UI with real-time updates

### Phase 4: Analysis and Visualization

1. Comparison calculation logic
1. ComparisonResults population
1. Results visualization dashboard
1. Export functionality

### Phase 5: Polish

1. Error handling and logging
1. Documentation (user guide, technical documentation)
1. Testing and validation
1. Performance optimization

## Success Criteria

- Successfully translate 95%+ of queries automatically
- Execute 500 queries across both platforms within reasonable time
- Accurately compare performance metrics with <1% measurement error
- Identify and visualize performance differences clearly
- Provide actionable insights for query optimization
- Maintain stable UI with responsive progress tracking
- Handle errors gracefully without test interruption

## Future Enhancements (Out of Scope for Initial Release)

- Query result data comparison (beyond row counts)
- Cost comparison (Snowflake credits vs SQL Server compute)
- Automatic query optimization suggestions
- Machine learning-based translation improvement
- Support for stored procedures and functions
- Integration with CI/CD pipelines
- Multi-user support with role-based access