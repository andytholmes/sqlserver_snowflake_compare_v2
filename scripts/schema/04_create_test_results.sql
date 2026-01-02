-- ============================================
-- TestResults
-- Stores individual query execution results
-- ============================================

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[TestResults]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[TestResults] (
        [result_id] BIGINT IDENTITY(1,1) NOT NULL,
        [test_run_id] INT NOT NULL,
        [query_id] INT NOT NULL,
        [platform] NVARCHAR(50) NOT NULL,  -- 'SQL Server' or 'Snowflake'
        [execution_number] INT NOT NULL,  -- For repeat executions (1, 2, 3, ...)
        [execution_time_ms] BIGINT NULL,
        [row_count] BIGINT NULL,
        [status] NVARCHAR(20) NOT NULL,  -- 'success' or 'error'
        [error_message] NVARCHAR(MAX) NULL,
        [execution_plan] NVARCHAR(MAX) NULL,  -- Optional execution plan XML/text
        [timestamp] DATETIME2 NOT NULL DEFAULT GETDATE(),
        
        CONSTRAINT [PK_TestResults] PRIMARY KEY CLUSTERED ([result_id] ASC),
        CONSTRAINT [FK_TestResults_TestRuns] FOREIGN KEY ([test_run_id])
            REFERENCES [dbo].[TestRuns] ([test_run_id])
            ON DELETE CASCADE,
        CONSTRAINT [FK_TestResults_QueryRepository] FOREIGN KEY ([query_id])
            REFERENCES [dbo].[QueryRepository] ([query_id])
            ON DELETE CASCADE,
        CONSTRAINT [CK_TestResults_Platform] CHECK ([platform] IN ('SQL Server', 'Snowflake')),
        CONSTRAINT [CK_TestResults_Status] CHECK ([status] IN ('success', 'error')),
        CONSTRAINT [CK_TestResults_ExecutionNumber] CHECK ([execution_number] > 0)
    );
    
    PRINT 'TestResults created successfully.';
END
ELSE
BEGIN
    PRINT 'TestResults already exists.';
END
GO

-- Create indexes for performance
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_TestResults_TestRunId')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_TestResults_TestRunId]
    ON [dbo].[TestResults] ([test_run_id]);
    PRINT 'Index IX_TestResults_TestRunId created.';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_TestResults_QueryId')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_TestResults_QueryId]
    ON [dbo].[TestResults] ([query_id]);
    PRINT 'Index IX_TestResults_QueryId created.';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_TestResults_TestRunId_QueryId_Platform')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_TestResults_TestRunId_QueryId_Platform]
    ON [dbo].[TestResults] ([test_run_id], [query_id], [platform]);
    PRINT 'Index IX_TestResults_TestRunId_QueryId_Platform created.';
END
GO

