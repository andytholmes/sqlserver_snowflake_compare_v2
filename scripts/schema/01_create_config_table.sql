-- ============================================
-- ConfigTable
-- Stores connection configurations for SQL Server and Snowflake
-- ============================================

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[ConfigTable]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[ConfigTable] (
        [connection_id] INT IDENTITY(1,1) NOT NULL,
        [platform] NVARCHAR(50) NOT NULL,  -- 'SQL Server' or 'Snowflake'
        [connection_string] NVARCHAR(MAX) NULL,
        [authentication_type] NVARCHAR(50) NULL,  -- 'username_password', 'key_pair', 'sso', etc.
        [created_date] DATETIME2 NOT NULL DEFAULT GETDATE(),
        [is_active] BIT NOT NULL DEFAULT 1,
        
        CONSTRAINT [PK_ConfigTable] PRIMARY KEY CLUSTERED ([connection_id] ASC),
        CONSTRAINT [CK_ConfigTable_Platform] CHECK ([platform] IN ('SQL Server', 'Snowflake'))
    );
    
    PRINT 'ConfigTable created successfully.';
END
ELSE
BEGIN
    PRINT 'ConfigTable already exists.';
END
GO

-- Create index on platform and is_active for common queries
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_ConfigTable_Platform_IsActive')
BEGIN
    CREATE NONCLUSTERED INDEX [IX_ConfigTable_Platform_IsActive]
    ON [dbo].[ConfigTable] ([platform], [is_active]);
    PRINT 'Index IX_ConfigTable_Platform_IsActive created.';
END
GO

