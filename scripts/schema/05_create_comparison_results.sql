-- ============================================
-- ComparisonResults
-- Stores aggregated comparison results between SQL Server and Snowflake
-- ============================================

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ComparisonResults]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ComparisonResults] (
        [comparison_id] INT IDENTITY(1,1) NOT NULL,
        [test_run_id] INT NOT NULL,
        [query_id] INT NOT NULL,
        [sqlserver_avg_time_ms] BIGINT NULL,
        [snowflake_avg_time_ms] BIGINT NULL,
        [time_difference_ms] BIGINT NULL,  -- snowflake_avg_time_ms - sqlserver_avg_time_ms
        [time_difference_percent] DECIMAL(10, 2) NULL,  -- Percentage difference
        [row_count_match] BIT NOT NULL DEFAULT 0,
        [sqlserver_row_count] BIGINT NULL,
        [snowflake_row_count] BIGINT NULL,
        [performance_winner] NVARCHAR(20) NULL,  -- 'SQL Server', 'Snowflake', or 'Tie'
        
        CONSTRAINT [PK_ComparisonResults] PRIMARY KEY CLUSTERED ([comparison_id] ASC),
        CONSTRAINT [FK_ComparisonResults_TestRuns] FOREIGN KEY ([test_run_id])
            REFERENCES [dbo].[TestRuns] ([test_run_id])
            ON DELETE CASCADE,
        CONSTRAINT [FK_ComparisonResults_QueryRepository] FOREIGN KEY ([query_id])
            REFERENCES [dbo].[QueryRepository] ([query_id])
            ON DELETE CASCADE,
        CONSTRAINT [CK_ComparisonResults_PerformanceWinner] CHECK ([performance_winner] IN ('SQL Server', 'Snowflake', 'Tie') OR [performance_winner] IS NULL),
        CONSTRAINT [UQ_ComparisonResults_TestRun_Query] UNIQUE ([test_run_id], [query_id])
    );
    
    PRINT 'ComparisonResults created successfully.';
END
ELSE
BEGIN
    PRINT 'ComparisonResults already exists.';
END
GO

-- Create indexes for performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ComparisonResults_TestRunId')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_ComparisonResults_TestRunId]
    ON [dbo].[ComparisonResults] ([test_run_id]);
    PRINT 'Index IX_ComparisonResults_TestRunId created.';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ComparisonResults_QueryId')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_ComparisonResults_QueryId]
    ON [dbo].[ComparisonResults] ([query_id]);
    PRINT 'Index IX_ComparisonResults_QueryId created.';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ComparisonResults_PerformanceWinner')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_ComparisonResults_PerformanceWinner]
    ON [dbo].[ComparisonResults] ([performance_winner]);
    PRINT 'Index IX_ComparisonResults_PerformanceWinner created.';
END
GO

