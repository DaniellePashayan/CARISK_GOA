# CARISK GoAnywhere Medical Records Processing

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An automated system for processing and consolidating medical records PDFs from the Sutherland RPA system. This tool extracts daily medical records, combines files by invoice number, performs quality checks, and prepares them for GoAnywhere automated distribution.

## 📋 Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Architecture](#architecture)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Configuration](#configuration)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Automated Scheduling](#automated-scheduling)
* [Logging and Monitoring](#logging-and-monitoring)
* [Error Handling](#error-handling)
* [Archive Management](#archive-management)
* [Testing](#testing)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)

## 🎯 Overview

This automation system processes medical records from the OC WCNF (Orlin & Cohen Workers' Compensation and No Fault) system. It combines multiple PDF files associated with the same invoice into a single consolidated document, validates page counts, generates audit logs, and prepares files for downstream GoAnywhere processing.

### Key Workflow

1. **Extract**: Identifies and extracts PDFs from dated folders organized by year/month/day
2. **Combine**: Merges multiple PDF files with the same invoice number into a single document
3. **Validate**: Verifies page counts match between original and combined PDFs
4. **Audit**: Generates Excel audit logs with processing statistics
5. **Notify**: Sends error notifications via Pushbullet for critical issues
6. **Archive**: Organizes processed files into a structured archive system

## Features

* **Smart Business Day Detection**: Automatically processes records from the last business day, accounting for weekends and holidays
* **Intelligent PDF Merging**: Combines multiple PDF files per invoice while maintaining document integrity
* **Page Count Validation**: Cross-verifies that no pages are lost during the merge process
* **Corrupted File Detection**: Identifies and skips zero-byte or corrupted PDF files
* **Comprehensive Audit Logging**: Generates detailed Excel reports for each processing run
* **Real-time Notifications**: Pushbullet integration for immediate error alerts
* **Status Tracking**: JSON-based status updates for dashboard monitoring
* **Automated Scheduling**: Windows Task Scheduler integration via batch scripts
* **Archive Management**: Automated cleanup and organization of processed files
* **Network Path Support**: Works with UNC network paths for enterprise file sharing

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Source Directory Structure                 │
│  \\NT2KWB972SRV03\SHAREDATA\CPP-Data\Sutherland RPA\...     │
│                                                             │
│  └── OC WCNF Records/                                       │
│      ├── YYYY/                                              │
│      │   └── MM YYYY/                                       │
│      │       └── MM_DD_YY/  ← Daily PDFs                    │
│      └── GOA/  ← Output destination                         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    Processing Pipeline                      │
│                                                             │
│  1. RootFolder.__init__()                                   │
│     ├── Get last business day                               │
│     ├── Navigate to daily folder                            │
│     └── Extract file names and invoice lists                │
│                                                             │
│  2. get_records_per_invoice()                               │
│     └── Group files by invoice number                       │
│                                                             │
│  3. combine_pdfs()                                          │
│     ├── Merge PDFs with PyMuPDF                             │
│     ├── Validate file integrity                             │
│     └── Save to GOA folder                                  │
│                                                             │
│  4. update_audit_log()                                      │
│     ├── Generate Excel report                               │
│     └── Update JSON status                                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  Output & Monitoring                        │
│                                                             │
│  ├── Combined PDFs → GOA/ folder                            │
│  ├── Audit Logs → script logs/MM_DD_YY.xlsx                 │
│  ├── Daily Logs → logs/log_MM_DD_YY.log                     │
│  └── Status Updates → Automated Scripts Status.json         │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

* **Python**: 3.8 or higher
* **Operating System**: Windows (for batch scripts and Task Scheduler)
* **Network Access**: Access to `\\NT2KWB972SRV03\SHAREDATA\CPP-Data\` network share
* **Pushbullet API**: API key for error notifications (optional but recommended)

### Required Python Packages

```
pandas>=2.2.3
PyMuPDF>=1.25.3
loguru>=0.7.3
tqdm>=4.67.1
openpyxl>=3.1.5
python-dateutil>=2.9.0
pushbullet.py
```

See `requirements.txt` for complete dependency list.

## Installation

### 1\. Clone the Repository

``` bash
git clone https://github.com/DaniellePashayan/CARISK_GOA.git
cd CARISK_GOA
```

### 2\. Create Virtual Environment

``` bash
python -m venv .venv
```

### 3\. Activate Virtual Environment

**Windows (cmd.exe):**

``` cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**

``` powershell
.venv\Scripts\Activate.ps1
```

### 4\. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 5\. Set Environment Variables

Create a `.env` file or set system environment variable:

``` bash
set PUSHBULLET_API_KEY=your_pushbullet_api_key_here
```

To obtain a Pushbullet API key:

1. Visit https://www.pushbullet.com/#settings/account
2. Create an Access Token
3. Store securely in your environment

## Configuration

### Network Paths

The following network paths are configured in `main.py`:

``` python
# Source directory for daily records
source_directory = Path(r'\\NT2KWB972SRV03\SHAREDATA\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records')

# Output destination for combined PDFs
destination = Path(r'\\NT2KWB972SRV03\SHAREDATA\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records\GOA')

# Audit log location
audit_path = Path(r'\\NT2KWB972SRV03\SHAREDATA\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records\script logs')
```

**⚠️ Important**: Update these paths if your network configuration differs.

### Status Tracking

The script updates a shared JSON status file for dashboard monitoring:

``` python
status = JSONStatus(
    r"\\NT2KWB972SRV03\SHAREDATA\CPP-Data\CBO Westbury Managers\LEADERSHIP\Bot Folder\Automated Scripts Status.json",
    "Carisk GOA"
)
```

## Usage

### Manual Execution

#### Run Main Script

``` bash
python main.py
```

This will:

* Automatically determine the last business day
* Process all PDFs from that date
* Generate audit logs and status updates

#### Run with Custom Date

Modify `manual.py` to specify a custom date:

``` python
year = '2024'
month = '02'
day = '27'
```

Then run:

``` bash
python manual.py
```

#### I

### Batch Execution

Execute via batch script (useful for Task Scheduler):

``` cmd
batch_script.bat
```

This script:

1. Navigates to project directory
2. Activates virtual environment
3. Runs `main.py`
4. Redirects output to `logs\TS_log.txt`

## 📁 Project Structure

```
│
├── main.py                      # Core processing logic
├── manual.py                    # Manual execution with custom dates
├── main.ipynb                   # Jupyter notebook for interactive use
│
├── batch_script.bat             # Windows batch file for automation
├── cleanup_archive_folder.py    # Archive organization script
├── cleanup_archive.bat          # Batch file for archive cleanup
│
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── logs/                        # Log files directory
│   ├── log_MM_DD_YY.log        # Daily processing logs
│   └── TS_log.txt              # Task Scheduler output
│
└── tests/                       # Unit tests
    ├── test.py                  # Test cases
    └── generate_tests.py        # Test generation utilities
```

### Key Files Description

| File | Purpose |
| ---- | ------- |
| `main.py` | Main processing script with `RootFolder` class and PDF combining logic |
| `manual.py` | Allows manual execution with user-specified dates |
| `batch_script.bat` | Windows Task Scheduler integration |
| `cleanup_archive_folder.py` | Organizes archived files into year/month/day structure |
| `requirements.txt` | Python package dependencies |

## Automated Scheduling

### Setting Up Windows Task Scheduler

1. **Open Task Scheduler**
    * Press `Win + R`, type `taskschd.msc`, press Enter
2. **Create Basic Task**
    * Click "Create Basic Task" in the Actions pane
    * Name: `CARISK GOA Processing`
    * Description: `Daily medical records PDF processing`
3. **Set Trigger**
    * Frequency: Daily
    * Start time: After business hours (e.g., 6:00 PM)
    * Recur every: 1 day
4. **Set Action**
    * Action: Start a program
    * Program/script: `C:\Users\pa_dpashayan\Desktop\PyProjects\CARISK_GOA\batch_script.bat`
    * Start in: `C:\Users\pa_dpashayan\Desktop\PyProjects\CARISK_GOA`
5. **Configure Settings**
    * ✅ Run whether user is logged on or not
    * ✅ Run with highest privileges
    * ✅ If the task fails, restart every: 10 minutes
    * ✅ Attempt to restart up to: 3 times
6. **Save and Test**
    * Right-click task → Run
    * Verify log files in `logs/` directory

## 📊 Logging and Monitoring

### Log Files

#### Daily Processing Logs (`logs/log_MM_DD_YY.log`)

Captures detailed processing information:

```
2025-12-10 18:00:01 | INFO     | Found 45 files in \\NT2KWB972SRV03\...\05_01_23
2025-12-10 18:00:02 | SUCCESS  | Found 12 unique invoices in \\NT2KWB972SRV03\...\05_01_23
2025-12-10 18:00:15 | SUCCESS  | PDFs combined and saved to \\NT2KWB972SRV03\...\GOA
2025-12-10 18:00:16 | SUCCESS  | Audit log updated: \\NT2KWB972SRV03\...\05_01_23.xlsx
2025-12-10 18:00:16 | INFO     | Script completed successfully for 05_01_23
```

**Log Rotation**: Logs are automatically rotated daily and retained for 7 days.

#### Task Scheduler Logs (`logs/TS_log.txt`)

Captures stdout/stderr when run via batch script.

### Audit Reports

Excel audit logs are generated at:

```
\\NT2KWB972SRV03\SHAREDATA\CPP-Data\Sutherland RPA\MedicalRecords\OC WCNF Records\script logs\MM_DD_YY.xlsx
```

**Columns**:

* `Invoice`: Invoice number
* `Files`: List of source files
* `File Count`: Number of files merged
* `Original Page Count`: Total pages in source files
* `New Page Count`: Pages in combined PDF
* `Saved`: Whether file was successfully saved
* `Page Count Match`: Boolean indicating if page counts match

### Status Dashboard

Updates a shared JSON file for real-time monitoring:

``` json
{
  "Carisk GOA": {
    "status": "Completed",
    "last_run": "2025-12-10 18:00:16",
    "errors": null
  }
}
```

**Status Values**:

* `Running`: Processing in progress
* `Completed`: Successful completion
* `Failed`: Error occurred (details in `errors` field)

## Error Handling

### Automatic Error Detection

The script handles various error scenarios:

1. **Corrupted Files**: Zero-byte files are skipped with warnings
2. **Page Count Mismatch**: Triggers critical log and Pushbullet notification
3. **Missing Folders**: Graceful failure with detailed error message
4. **Network Issues**: Logged with full exception details

### Pushbullet Notifications

Critical errors trigger immediate notifications:

``` python
send_error_notification("PDF is missing pages for invoice ABC123. Original: 10, New: 8")
```

You'll receive a push notification on all connected devices with:

* **Title**: "UHC API Input Generator Error"
* **Message**: Detailed error description

### Error Recovery

1. **Check Logs**: Review `logs/log_MM_DD_YY.log` for details
2. **Verify Status**: Check JSON status file for error message
3. **Manual Rerun**: Use `manual.py` to reprocess specific dates
4. **Archive Cleanup**: Run `cleanup_archive_folder.py` if needed

## Archive Management

### Cleanup Script

The `cleanup_archive_folder.py` script organizes archived files:

**Purpose**: Moves files from flat archive folder into organized year/month/day structure

**Usage**:

``` bash
python cleanup_archive_folder.py
```

Or via batch file:

``` cmd
cleanup_archive.bat
```

**Behavior**:

* Reads file modification date
* Creates folder structure: `YYYY/MM YYYY/MM_DD_YY/`
* Moves files to appropriate dated folder
* Removes duplicates if they exist

**Target Directory**:

```
M:/CPP-Data/Sutherland RPA/MedicalRecords/OC WCNF Records/GOA Archive
```

## Testing

### Run Unit Tests

``` bash
cd tests
python test.py
```

### Test Coverage

Current tests include:

* Business day calculation (Monday through Sunday scenarios)
* Weekend handling
* Month/year transitions

### Adding Tests

Use `tests/generate_tests.py` to scaffold new test cases.

## Troubleshooting

### Common Issues

#### 1\. "NOT CONNECTED TO M DRIVE"

**Cause**: Network drive not mapped

**Solution**:

``` cmd
net use M: \\NT2KWB972SRV03\SHAREDATA
```

#### 2\. "No files found in daily folder"

**Cause**: Incorrect date or missing data

**Solution**:

* Verify date calculation with `get_last_business_day()`
* Check source directory manually and reach out to Sutherland to save the folder
* Use `manual.py` to specify exact date

#### 3\. "Page Count Mismatch"

**Cause**: Corrupted PDF or incomplete merge

**Solution**:

* Check log for specific invoice
* Manually inspect source PDFs
* Rerun processing for that date

#### 4\. "Permission Denied" errors

**Cause**: Insufficient network permissions

**Solution**:

* Ensure you have read/write access to network shares
* Run Task Scheduler with appropriate service account

#### 5\. Pushbullet notifications not working

**Cause**: Missing or invalid API key

**Solution**:

``` cmd
set PUSHBULLET_API_KEY=your_api_key
```

### Debug Mode

Enable verbose logging by modifying logger level:

``` python
logger.add('debug.log', level='DEBUG')
```

## License

This project is proprietary software for internal use within the organization.

- - -

## Support

For issues, questions, or contributions:

* **Repository**: https://github.com/DaniellePashayan/CARISK\_GOA
* **Email**: DPashayan@northwell.edu
* **Owner**: DaniellePashayan
* **Branch**: main

**Last Updated**: December 10, 2025