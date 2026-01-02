-- ============================================
-- Master Script: Create All Tables
-- ============================================
-- This script creates all database tables in the correct order
-- Run this script to set up the entire database schema
-- ============================================

PRINT '========================================';
PRINT 'Creating SQL Server to Snowflake Compare Database Schema';
PRINT '========================================';
PRINT '';

-- Create ConfigTable
:r 01_create_config_table.sql

-- Create QueryRepository
:r 02_create_query_repository.sql

-- Create TestRuns
:r 03_create_test_runs.sql

-- Create TestResults (depends on TestRuns and QueryRepository)
:r 04_create_test_results.sql

-- Create ComparisonResults (depends on TestRuns and QueryRepository)
:r 05_create_comparison_results.sql

PRINT '';
PRINT '========================================';
PRINT 'Database schema creation complete!';
PRINT '========================================';
GO

