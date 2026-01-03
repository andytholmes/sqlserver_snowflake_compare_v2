```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
│                      src/ui/main.py                         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────┐  │
│  │ Translation      │  │ Execution        │  │ Analysis  │  │
│  │ Engine           │  │ Engine           │  │ Comparator│  │
│  └──────────────────┘  └──────────────────┘  └───────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Access Layer                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────┐   │
│  │ SQL Server       │  │ Snowflake        │  │ Test Run │   │
│  │ Connection       │  │ Connection       │  │ DB Schema│   │
│  └──────────────────┘  └──────────────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────┐   │
│  │ Configuration    │  │ Logging          │  │ Exception│   │
│  │ Loader           │  │ Infrastructure   │  │ Handling │   │
│  └──────────────────┘  └──────────────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         └────────────────────┴────────────────────┘
                    (supports all layers)
```


## Component Overview

### 1. Configuration Layer (`src/utils/config_loader.py`)

- **Purpose**: Centralized configuration management
- **Technology**: Dynaconf
- **Features**:
  - JSON configuration file support
  - Environment variable overrides
  - Configuration validation
  - Multiple configuration sources

### 2. Logging Infrastructure (`src/utils/logger.py`)

- **Purpose**: Centralized logging with rotation
- **Features**:
  - File and console handlers
  - Log rotation (size-based)
  - Configurable log levels
  - Integration with configuration system

### 3. Database Layer

#### Connection Management (`src/database/connections.py`)
- **SQLServerConnection**: Manages SQL Server connections using pyodbc
- **SnowflakeConnection**: Manages Snowflake connections using snowflake-connector-python
- **Features**: Context manager support, connection pooling ready

#### Schema Operations (`src/database/schema.py`)
- **SchemaManager**: Database schema operations
- **Features**: Table existence checks, schema information retrieval

### 4. Translation Engine (`src/translation/translator.py`)

- **Purpose**: Convert SQL Server queries to Snowflake syntax
- **QueryTranslator**: Main translation class
- **Translation Rules**:
  - Date functions: `GETDATE()` → `CURRENT_TIMESTAMP()`
  - String functions: `LEN()` → `LENGTH()`
  - Null functions: `ISNULL()` → `IFNULL()`
  - TOP clause: `TOP N` → `LIMIT N`

### 5. Execution Engine (`src/execution/executor.py`)

- **Purpose**: Execute queries on both platforms
- **QueryExecutor**: Main execution class
- **Features**:
  - Parallel execution support
  - Metrics collection (execution time, row count)
  - Error handling
  - Timeout support

### 6. Analysis Module (`src/analysis/comparator.py`)

- **Purpose**: Compare and analyze performance results
- **PerformanceComparator**: Main comparison class
- **Features**:
  - Average execution time calculation
  - Performance winner determination
  - Row count validation
  - Statistical analysis (min, max, median, mean)

### 7. User Interface (`src/ui/main.py`)

- **Purpose**: Graphical user interface
- **Technology**: tkinter (built-in Python GUI framework)
- **Features**:
  - Connection configuration
  - Test configuration
  - Real-time progress monitoring
  - Results visualization

## Data Flow

### Query Execution Flow

```
1. Load queries from QueryRepository
   ↓
2. Translate SQL Server queries to Snowflake
   ↓
3. Create test run record in TestRuns table
   ↓
4. Execute queries in parallel (configurable workers)
   ├─→ SQL Server execution
   └─→ Snowflake execution
   ↓
5. Store results in TestResults table
   ↓
6. Calculate comparison metrics
   ↓
7. Store comparison results in ComparisonResults table
   ↓
8. Update test run status
```

### Configuration Flow

```
1. Load config.json (or config_template.json)
   ↓
2. Override with environment variables (.env file)
   ↓
3. Validate configuration
   ↓
4. Make available to all modules via ConfigLoader
```

## Database Schema

The application uses a SQL Server database to store:

- **ConfigTable**: Connection configurations
- **QueryRepository**: SQL queries and translations
- **TestRuns**: Test run metadata
- **TestResults**: Individual execution results
- **ComparisonResults**: Aggregated comparison metrics

See `scripts/schema/` for detailed schema definitions.

## Error Handling

The application uses a hierarchical exception structure:

- `SQLServerSnowflakeCompareError` (base exception)
  - `ConfigurationError`
  - `DatabaseConnectionError`
  - `QueryExecutionError`
  - `TranslationError`
  - `ValidationError`
  - `SchemaError`

## Concurrency

- **Parallel Execution**: Uses `concurrent.futures.ThreadPoolExecutor`
- **Configurable Workers**: 1-50 concurrent query executions
- **Thread Safety**: Each execution uses separate connections

## Scalability Considerations

- **Connection Pooling**: Ready for connection pooling implementation
- **Batch Processing**: Results can be stored in batches
- **Async Support**: Architecture allows for async implementation
- **Database Optimization**: Indexes on foreign keys and commonly queried columns

## Future Enhancements

- Async/await support for better concurrency
- Connection pooling for database connections
- Caching layer for translations
- Plugin system for custom translation rules
- REST API for remote access
- Web-based UI alternative

