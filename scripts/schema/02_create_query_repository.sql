-- ============================================
-- QueryRepository
-- Stores SQL Server queries and their Snowflake translations
-- ============================================

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[QueryRepository]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[QueryRepository] (
        [query_id] INT IDENTITY(1,1) NOT NULL,
        [query_name] NVARCHAR(255) NOT NULL,
        [sqlserver_query] NVARCHAR(MAX) NOT NULL,
        [snowflake_query] NVARCHAR(MAX) NULL,
        [query_complexity] NVARCHAR(20) NULL,  -- 'simple', 'medium', 'complex'
        [translation_validated] BIT NOT NULL DEFAULT 0,
        [translation_date] DATETIME2 NULL,
        [description] NVARCHAR(MAX) NULL,
        [is_active] BIT NOT NULL DEFAULT 1,
        
        CONSTRAINT [PK_QueryRepository] PRIMARY KEY CLUSTERED ([query_id] ASC),
        CONSTRAINT [CK_QueryRepository_Complexity] CHECK ([query_complexity] IN ('simple', 'medium', 'complex') OR [query_complexity] IS NULL)
    );
    
    PRINT 'QueryRepository created successfully.';
END
ELSE
BEGIN
    PRINT 'QueryRepository already exists.';
END
GO

-- Create indexes for common queries
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_QueryRepository_IsActive')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_QueryRepository_IsActive]
    ON [dbo].[QueryRepository] ([is_active]);
    PRINT 'Index IX_QueryRepository_IsActive created.';
END
GO

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_QueryRepository_TranslationValidated')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_QueryRepository_TranslationValidated]
    ON [dbo].[QueryRepository] ([translation_validated]);
    PRINT 'Index IX_QueryRepository_TranslationValidated created.';
END
GO

