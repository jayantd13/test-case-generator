# Testcases Folder

This folder contains all generated test case Excel files from both the CLI and web interface.

## File Naming Convention

- **CLI Generated**: `JIRA-TICKET_testcases.xlsx`
- **Web UI Generated**: `JIRA-TICKET_testcases_YYYYMMDD_HHMMSS.xlsx`

## Example Files

- `BULK-001_testcases.xlsx` - CLI generated test cases
- `AUTH-123_testcases_20250713_150530.xlsx` - Web UI generated with timestamp
- `API-456_testcases.xlsx` - CLI generated API test cases

## File Management

- Files are automatically organized by timestamp
- Each generation creates a new file (no overwriting)
- Download files directly from the web interface
- Access files locally from this folder

## Git Tracking

- The folder structure is tracked in Git (via `.gitkeep`)
- Generated Excel files are ignored in `.gitignore`
- Only the folder structure is committed, not the test case files
