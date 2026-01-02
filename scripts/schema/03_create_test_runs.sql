-- ============================================
-- TestRuns
-- Stores test run metadata and configuration
-- ============================================

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[TestRuns]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[TestRuns] (
        [test_run_id] INT IDENTITY(1,1) NOT NULL,
        [run_name] NVARCHAR(255) NOT NULL,
        [start_time] DATETIME2 NULL,
        [end_time] DATETIME2 NULL,
        [status] NVARCHAR(20) NOT NULL DEFAULT 'pending',  -- 'pending', 'running', 'completed', 'failed'
        [parallel_workers] INT NOT NULL DEFAULT 1,
        [repeat_count] INT NOT NULL DEFAULT 1,
        [queries_executed] INT NULL DEFAULT 0,
        [created_by] NVARCHAR(100) NULL,
        
        CONSTRAINT [PK_TestRuns] PRIMARY KEY CLUSTERED ([test_run_id] ASC),
        CONSTRAINT [CK_TestRuns_Status] CHECK ([status] IN ('pending', 'running', 'completed', 'failed')),
        CONSTRAINT [CK_TestRuns_ParallelWorkers] CHECK ([parallel_workers] > 0),
        CONSTRAINT [CK_TestRuns_RepeatCount] CHECK ([repeat_count] > 0)
    );
    
    PRINT 'TestRuns created successfully.';
END
ELSE
BEGIN
    PRINT 'TestRuns already exists.';
END
GO

-- Create indexes for common queries
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_TestRuns_Status')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_TestRuns_Status]
    ON [dbo].[TestRuns] ([status]);
    PRINT 'Index IX_TestRuns_Status created.';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_TestRuns_StartTime')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_TestRuns_StartTime]
    ON [dbo].[TestRuns] ([start_time] DESC);
    PRINT 'Index IX_TestRuns_StartTime created.';
END
GO

