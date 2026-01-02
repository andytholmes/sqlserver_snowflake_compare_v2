# Configuration Directory

This directory contains configuration files for the SQL Server to Snowflake Query Performance Comparison Tool.

## Files

### `config_template.json`
Template configuration file with all available settings and default values. Copy this to `config.json` and customize for your environment.

**Note**: Do not commit `config.json` if it contains sensitive credentials. Use environment variables (via `.env` file) for credentials instead.

### Creating Your Config File

1. Copy the template:
   ```bash
   cp config/config_template.json config/config.json
   ```

2. Edit `config.json` with your settings (non-sensitive values only)

3. Use `.env` file for sensitive credentials (see `.env.example` in project root)

## Configuration Sections

- **connections**: Database connection parameters (use placeholders, real credentials in .env)
- **execution**: Parallel workers, repeat counts, timeouts
- **ui**: UI framework and display preferences
- **logging**: Log levels, file settings, rotation
- **translation**: Query translation settings
- **analysis**: Analysis and export settings

## Environment Variables

See `.env.example` in the project root for environment variable configuration.

