---
name: dbdoctor-tools
description: >
  DBDoctor database performance diagnosis platform tools.
  Invoke when user needs to query database instances, slow SQL,
  inspection reports, performance metrics, or perform SQL audit/rewrite operations.
license: Apache-2.0
compatibility: Requires Python 3.9+ with requests, pycryptodome, python-dotenv packages. Network access to DBDoctor API server required.
allowed-tools: Bash Read
requires:
  env:
    - DBDOCTOR_URL
    - DBDOCTOR_USER
    - DBDOCTOR_PASSWORD
  commands:
    - python
    - pip
metadata:
  author: DBdoctor-DAS
  version: 1.0.1
  tags: [database, performance, diagnosis, slow-sql, sql-audit, monitoring, dbdoctor]
---

## Quick Start Examples

### Scenario 1: Diagnose Instance Performance Issues (Recommended)

```bash
# 1. Get tenant and project
python scripts/get_current_user.py --extract

# 2. Get instance list
python scripts/get_instance.py --tenant [tenant] --project [project]

# 3. Execute comprehensive performance diagnosis (last 1 hour)
python scripts/performance_diagnosis.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

### Scenario 2: Execute Instance Inspection

```bash
# 1. Get tenant and project of the instance
python scripts/get_instance.py

# 2. Execute inspection
python scripts/do_inspect_instance.py --instance-id [instance_id] --tenant [tenant] --project [project]

# 3. Get inspection report
python scripts/get_recent_inspect_report.py --instance-id [instance_id] --start-time [start] --end-time [end] --tenant [tenant] --project [project]
```

### Scenario 3: SQL Optimization

```bash
# 1. Get slow SQL list
python scripts/get_slow_sql.py --instance-id [instance_id] --start-time [start] --end-time [end]

# 2. Audit slow SQL
python scripts/sql_audit.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]"

# 3. Use AI to rewrite SQL (optional)
python scripts/ai_sql_rewrite.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]"
```

***

## Before Using Skills

### 1. Environment Configuration (Auto-Init)

**Zero-Configuration Quick Start**: The skill supports automatic configuration on first use. Simply run any script, and the system will guide you through the setup interactively.

**Required Configuration**:

| Variable Name | Description | Example |
| --- | --- | --- |
| DBDOCTOR\_URL | DBDoctor API base URL | http://\[host\]:\[port\] |
| DBDOCTOR\_USER | Login username (also used as UserId) | \[username\] |
| DBDOCTOR\_PASSWORD | Login password (plaintext, automatically AES encrypted) | \[password\] |

**First-Time Setup (Interactive)**:

On first use, the system will automatically prompt:
```
============================================================
Welcome to dbdoctor-tools!
First-time configuration required.
============================================================

Please enter DBDoctor URL (e.g., http://localhost:8080): 
Please enter DBDoctor username: 
Please enter DBDoctor password: 

============================================================
✅ Configuration saved to: .../.env
============================================================
```

The configuration will be saved to `.env` file and automatically loaded in subsequent sessions.

**Configuration Priority**:

System environment variables > `.env` file > Interactive input

**Alternative: Manual .env File Creation**

If you prefer manual configuration, create `.env` file in project root with the following content:
```
DBDOCTOR_URL=http://[host]:[port]
DBDOCTOR_USER=[username]
DBDOCTOR_PASSWORD=[password]
```

> **Security Note**: Passwords written in plaintext will be automatically AES-encrypted (prefixed with `ENC:`) on first load. After that, the `.env` file will contain only the encrypted value.

**Alternative: System Environment Variables (Temporary)**
```bash
# Linux / Mac
export DBDOCTOR_URL="http://[host]:[port]"
export DBDOCTOR_USER="[username]"
export DBDOCTOR_PASSWORD="[password]"

# Windows PowerShell
$env:DBDOCTOR_URL="http://[host]:[port]"
$env:DBDOCTOR_USER="[username]"
$env:DBDOCTOR_PASSWORD="[password]"
```

### 2. Instance Information Retrieval Guidelines

**Important**: When tenant and project information is needed, **it must be dynamically retrieved through tools**, and is prohibited from being extracted directly from user input or other sources.

**⚠️ Strictly prohibited from fabricating tenant and project information**

**Method 1: Retrieve via get_current_user (Recommended)**
```
1. Call get_current_user --extract to get all tenants and projects for the current user
2. Select target tenant and project
3. Call get_instance --tenant xxx --project yyy to get instance list under this tenant/project
4. Select target instance and execute other operations
```

**Method 2: Retrieve via get_instance (Recommended)**
```
1. Call get_instance to query all instance list (no parameters needed)
2. Find target instance from returned data
3. Extract tenant and project from instance data
4. Use extracted tenant and project to call other tools
```

**Example**:
```bash
# Method 1: Get tenant/project first, then get instances
python scripts/get_current_user.py --extract
python scripts/get_instance.py --tenant demo-tenant --project demo-project

# Method 2: Get all instances directly (Recommended)
python scripts/get_instance.py

# Use obtained tenant and project to execute other operations
python scripts/execute_sql.py --instance-id xxx --tenant [from_instance] --project [from_instance] ...
```

### 3. API Usage Constraints

**⚠️ Strictly prohibited from calling interfaces not defined in this document**

- Only use tools and interfaces listed in the "Tool API Reference" section
- Prohibited from fabricating or inferring interface paths
- Prohibited from calling interfaces of other systems or services
- For new features, please confirm if the interface exists first

***

## Tool Combination Patterns

### Pattern 1: Performance Diagnosis Workflow ⭐ (Most Common)

```
get_current_user --extract
        ↓
get_instance --tenant xxx --project yyy
        ↓
performance_diagnosis --instance-id xxx --start-time t1 --end-time t2
        ↓
[Based on diagnosis results]
    ├─ Many slow SQLs → sql_audit / ai_sql_rewrite
    ├─ Resource bottleneck → get_host_resource_info / get_basic_monitor_info
    └─ High active sessions → get_aas_info / get_current_process
```

### Pattern 2: Instance Inspection Workflow

```
get_instance
        ↓
do_inspect_instance --instance-id xxx --tenant xxx --project yyy
        ↓
get_recent_inspect_report --instance-id xxx --start-time t1 --end-time t2
```

### Pattern 3: SQL Optimization Workflow

```
get_slow_sql / get_related_sql_info
        ↓
sql_audit --sql "xxx"
        ↓
[Based on audit results]
    ├─ Need rewrite → ai_sql_rewrite
    └─ Need index suggestion → execute_sql "ALTER TABLE ... ADD INDEX ..."
```

### Pattern 4: New Instance Registration Workflow

```
get_current_user --extract
        ↓
manage_instance --tenant xxx --project yyy --ip xxx --port xxx ...
        ↓
get_instance --tenant xxx --project yyy [Confirm registration success]
```

***

## Environment Configuration

All tools are called through Python scripts. The skill supports **automatic configuration initialization** - simply run any script and follow the interactive prompts on first use.

### Automatic Configuration (Recommended)

On first use, the system will automatically detect missing configuration and guide you through setup:

```bash
# Just run any script
python scripts/get_instance.py

# The system will prompt:
# "Please enter DBDoctor URL (e.g., http://localhost:8080):"
# "Please enter DBDoctor username:"
# "Please enter DBDoctor password:"
```

Configuration is automatically saved to `.env` file and will be loaded in all subsequent sessions.

### Manual Configuration Options

**Option 1: Manual .env File Creation**

Create `.env` file in project root with the following content:
```
DBDOCTOR_URL=http://[host]:[port]
DBDOCTOR_USER=[username]
DBDOCTOR_PASSWORD=[password]
```

> **Security Note**: Passwords written in plaintext will be automatically AES-encrypted (prefixed with `ENC:`) on first load. After that, the `.env` file will contain only the encrypted value.

**Option 2: System Environment Variables (Temporary)**
```bash
# Linux / Mac
export DBDOCTOR_URL="http://[host]:[port]"
export DBDOCTOR_USER="[username]"
export DBDOCTOR_PASSWORD="[password]"

# Windows PowerShell
$env:DBDOCTOR_URL="http://[host]:[port]"
$env:DBDOCTOR_USER="[username]"
$env:DBDOCTOR_PASSWORD="[password]"
```

### Configuration Priority

System environment variables > `.env` file > Interactive input

### Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies include: requests, pycryptodome, python-dotenv

**Authentication Mechanism**: The program reads account information from environment variables, automatically completes password AES encryption, login to obtain Token, token file caching (.token\_cache) and automatic refresh, no need to manually manage auth\_token.

## Information Collection Matrix

| Task Type     | Required Information            | Collection Strategy            | Notes |
| -------- | --------------- | --------------- | ---- |
| Query Instance     | None               | Call tool directly          | Get instance list and tenant/project |
| Product Q&A     | None               | Call tool directly          | |
| Technical Q&A     | None               | Call tool directly          | |
| Platform Operation Guide   | None               | Call tool directly          | |
| **Instance Inspection** | **Instance ID**        | **Check → Ask → Call**   | tenant/project must be retrieved via get_instance |
| **Performance Diagnosis** | **Instance ID + Time Range** | **Check → Ask one by one → Call** | tenant/project must be retrieved via get_instance |
| **View Data** | **Instance ID**        | **Check → Ask → Call**   | tenant/project must be retrieved via get_instance |

**For detailed processing strategies, decision trees and rules, please refer to**: `reference/agent_guidelines.md`

***

# Tool API Reference

## Utility Tools

### 0. Get Current Timestamp

Get the current Unix timestamp (seconds) for time range queries.

**Python Timestamp Calculation**:

```python
import time

now = int(time.time())
print(f"Current timestamp: {now}")

# Get timestamps for specific time ranges
start = now - 3600   # Last 1 hour
start = now - 7200   # Last 2 hours
start = now - 86400  # Last 24 hours
```

**Common Time Range Calculations**:

| Time Range   | Calculation        | Seconds     |
| ------ | --------- | ------ |
| Last 1 hour  | now - 3600 | 3600   |
| Last 2 hours  | now - 7200 | 7200   |
| Last 6 hours  | now - 21600| 21600  |
| Last 12 hours | now - 43200| 43200  |
| Last 24 hours | now - 86400| 86400  |
| Last 3 days   | now - 259200| 259200 |
| Last 7 days   | now - 604800| 604800 |

**Complete Example - Get Slow SQL for Last 2 Hours**:

```bash
# Step 1: Calculate timestamps
now=$(python -c "import time; print(int(time.time()))")
start=$(python -c "import time; print(int(time.time()) - 7200)")

# Step 2: Call tool
python scripts/get_slow_sql.py --instance-id [instance_id] --start-time $start --end-time $now
```

**Important Notes**:

- Timestamps must be integers (seconds), not milliseconds
- Use `python -c "import time; print(int(time.time()))"` to get current timestamp

***

## Instance Management Tools

### 1. get\_instance - Get Instance Basic Information, Returns Instance List and Abnormal Instances

Get the list of database instances under a tenant/project. **This tool is the only way to obtain instance tenant and project information**.

**Python Call**:

```bash
# Get all instances (will return all instances across all tenants/projects)
python scripts/get_instance.py

# Filter by tenant and project
python scripts/get_instance.py --tenant [tenant] --project [project]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --tenant | string | No | Tenant name filter (optional) |
| --project | string | No | Project name filter (optional) |

```

**Important**: When other tools need `--tenant` and `--project` parameters, you must call this tool first to obtain them, and are prohibited from extracting directly from user input.

***

### 2. get\_current\_user - Get Current User Tenant and Project Information

Get the list of all tenants and projects for the currently logged-in user. The namespace format is `tenant-project`.

**Applicable Scenarios**:
- View all tenants and projects that the current user has permissions for
- As a prerequisite step for `get_instance`, determine tenant and project first

**Python Call**:

```bash
# Get complete user information
python scripts/get_current_user.py

# Get simplified tenant-project list
python scripts/get_current_user.py --extract
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --extract | flag | No | Only output simplified tenant-project list |

**Return Example (--extract mode)**:
```json
{
  "username": "tester",
  "userId": "472",
  "tenantProjects": [
    {
      "tenant": "demo-tenant",
      "project": "demo-project",
      "namespace": "demo-tenant-demo-project",
      "roles": ["dev", "admin", "tester"]
    },
    {
      "tenant": "ju-admin",
      "project": "admin",
      "namespace": "ju-admin-admin",
      "roles": ["admin"]
    }
  ]
}
```

**Usage Flow**:
```
1. Call get_current_user --extract to get tenant-project list
2. Select target tenant and project
3. Call get_instance --tenant xxx --project yyy to get instance list
4. Select target instance and execute other operations
```

***

### 3. get\_instance\_abnormal - Get Instance Abnormal Information

Get abnormal/alert information for a specified instance.

**Python Call**:

```bash
python scripts/get_instance_abnormal.py --instance-id [instance_id]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |

***

### 4. get\_database\_by\_instance - Get Databases Under Instance

Get the list of all databases under a specified instance.

**Python Call**:

```bash
python scripts/get_database_by_instance.py --instance-id [instance_id]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |

***

### 5. manage\_instance - Manage Database Instance

Register a new database instance to the DBDoctor platform.

**Python Call**:

```bash
python scripts/manage_instance.py --ip [ip] --port [port] --engine mysql --db-user [user] --db-password [password] --db-version [version] --tenant [tenant] --project [project]
```

Note: --db-password accepts plaintext password, the program automatically completes RSA encryption internally.

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --ip | string | Yes | Database server IP |
| --port | integer | Yes | Database port |
| --engine | string | Yes | Database engine (mysql/oracle/postgresql/dm/sqlserver/oracle-rac) |
| --db-user | string | Yes | Database username |
| --db-password | string | Yes | Database password (plaintext, automatically encrypted) |
| --db-version | string | Yes | Database version |
| --tenant | string | Yes | Tenant name |
| --project | string | Yes | Project name |
| --description | string | No | Instance description |

***

## SQL Analysis Tools

### 6. get\_slow\_sql - Get Slow SQL List

Get slow SQL queries within a specified time range.

**Python Call**:

```bash
python scripts/get_slow_sql.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start time (Unix timestamp, seconds) |
| --end-time | string | Yes | End time (Unix timestamp, seconds) |

**Related Page**: View slow SQL page (查看实例慢SQL页面)
```
{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-slow-sql-governance?cluster=idc
```

***

### 7. get\_table\_ddl - Get Table DDL

Get the structure definition of a specified table.

**Python Call**:

```bash
python scripts/get_table_ddl.py --instance-id [instance_id] --database [db] --schema [schema] --table [table]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --database | string | Yes | Database name |
| --schema | string | Yes | Schema name (same as database name for MySQL) |
| --table | string | Yes | Table name |

***

### 8. execute\_sql - Execute SQL Statement

Execute SQL statements on a specified database.

**Prerequisite**: If tenant and project information is needed, call `get_instance` first to get instance details.

**Python Call**:

```bash
python scripts/execute_sql.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]" --engine mysql --tenant [tenant] --project [project]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --database | string | Yes | Database name |
| --schema | string | Yes | Schema name |
| --sql | string | Yes | SQL statement to execute (wrapped in quotes) |
| --engine | string | Yes | Database engine (mysql/oracle/postgresql) |
| --tenant | string | Yes | Tenant name (can be obtained from get_instance) |
| --project | string | Yes | Project name (can be obtained from get_instance) |

***

### 9. sql\_audit - SQL Audit

Audit and analyze SQL statements. Automatically completes the two-step process of submitting audit + polling results internally.

**Prerequisites**: Instance ID, database name, schema name, SQL to be audited

**Python Call**:

```bash
python scripts/sql_audit.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]"
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --database | string | Yes | Database name |
| --schema | string | Yes | Schema name |
| --sql | string | Yes | SQL statement to audit (wrapped in quotes) |

**Follow-up Suggestions**:
- If issues are found during audit → `ai_sql_rewrite` for SQL rewriting
- If indexes need to be added → `execute_sql` to execute ALTER TABLE ADD INDEX
- To view audit rules → `get_sql_audit_rules`

***

### 10. get\_sql\_audit\_rules - Get SQL Audit Rules

Get SQL audit rule configurations.

**Python Call**:

```bash
python scripts/get_sql_audit_rules.py --engine mysql --priority ERROR
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --engine | string | No | Database engine filter |
| --rule-name | string | No | Rule name filter |
| --priority | string | No | Risk level (ERROR/WARNING/DANGER) |

***

## Inspection Tools

### 11. do\_inspect\_instance - Execute Instance Inspection

Trigger an inspection task for a database instance. Automatically completes the two-step process of getting inspection template + executing inspection internally.

**Prerequisites**: Instance ID; if you need to generate jump links, call `get_instance` first to get tenant and project

**Python Call**:

```bash
# Basic usage
python scripts/do_inspect_instance.py --instance-id [instance_id]

# With jump link (recommended), need to prompt user to view after completion
python scripts/do_inspect_instance.py --instance-id [instance_id] --tenant [tenant] --project [project]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --tenant | string | No | Tenant name (optional, used to generate jump link, can be obtained from get_instance) |
| --project | string | No | Project name (optional, used to generate jump link, can be obtained from get_instance) |

**Follow-up Suggestions**:
- View detailed report → `get_recent_inspect_report`
- View inspection items list → `get_inspect_item`

***

### 12. get\_recent\_inspect\_report - Get Recent Inspection Report

Get the recent inspection report for an instance.

**Prerequisite**: If tenant and project information is needed, call `get_instance` first to get instance details.

**Python Call**:

```bash
python scripts/get_recent_inspect_report.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts] --tenant [tenant] --project [project]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | integer | Yes | Start time (Unix timestamp, seconds) |
| --end-time | integer | Yes | End time (Unix timestamp, seconds) |
| --tenant | string | Yes | Tenant name (can be obtained from get_instance) |
| --project | string | Yes | Project name (can be obtained from get_instance) |

***

### 13. get\_inspect\_item - Get Inspection Items

Get the list of available inspection items.

**Python Call**:

```bash
python scripts/get_inspect_item.py
```

No parameters.

***

## Session & Process Tools

### 14. get\_current\_process - Get Current Sessions

Query the list of current database sessions/processes.

**Python Call**:

```bash
python scripts/get_current_process.py --instance-id [instance_id] --database [db] --sql-keyword [keyword]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --database | string | No | Database name filter |
| --sql-keyword | string | No | SQL keyword filter |

***

## Alert Tools

### 15. alert\_message - Get Alert Overview

Get an overview of alert messages.

**Python Call**:

```bash
python scripts/alert_message.py --status alarming --priority serious
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --status | string | No | Alert status (alarming/recovered) |
| --priority | string | No | Alert level (serious/warning/info) |
| --event-name | string | No | Event name filter |
| --instance-ip | string | No | Instance IP filter |
| --instance-desc | string | No | Instance description filter |
| --create-time | string | No | Creation time filter |
| --modified-time | string | No | Modification time filter |

***

## Performance Diagnosis Tools

### 16. performance\_diagnosis - Database Performance Comprehensive Diagnosis ⭐

**Recommended** - Perform comprehensive performance diagnosis on a database for a specified time period, integrating multiple diagnostic dimensions, and obtain a complete performance analysis report in one call.

**Prerequisites**: Instance ID, time range (can get instance ID via `get_instance`)

**Diagnostic Dimensions** (using actual existing API endpoints):
- Instance basic information (/drapi/ai/instance/info)
- Slow SQL analysis (/drapi/ai/getSlowSqlByTime)
- Abnormal SQL analysis (/drapi/ai/getAbnormalSqlByTime)
- AAS active session statistics (/drapi/ai/activeSession/statistics)
- Resource monitoring metrics (/drapi/ai/getResourceMetricsInNL)

**Python Call**:

```bash
python scripts/performance_diagnosis.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

**Return Report Structure**:
```json
{
  "diagnosisTime": {"startTime": xxx, "endTime": yyy},
  "instanceInfo": {...},
  "performanceMetrics": {
    "slowSql": [...],
    "abnormalSql": [...],
    "aasInfo": {...}
  },
  "resourceMetrics": {...}
}
```

**Follow-up Suggestions**:
- Many slow SQL → Use `sql_audit` or `ai_sql_rewrite` for optimization
- Resource bottleneck → Use `get_host_resource_info` to view detailed resource metrics
- High active sessions → Use `get_aas_info` to analyze session composition

***

### 17. get\_basic\_monitor\_info - Get Database Monitoring Metrics

Get database-level monitoring metrics.

**Python Call**:

```bash
python scripts/get_basic_monitor_info.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

**Related Page**: View basic monitor page (查看基础监控页面)
```
{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-basic-monitor?cluster=idc
```

***

### 18. get\_host\_resource\_info - Get Host Resource Metrics

Get host-level resource monitoring metrics.

**Python Call**:

```bash
python scripts/get_host_resource_info.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

**Related Page**: View host resource page (查看主机资源页面)
```
{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-basic-monitor?cluster=idc
```

***

### 19. get\_db\_parameter\_info - Get Database Parameters

Get database parameter configurations.

**Python Call**:

```bash
python scripts/get_db_parameter_info.py --instance-id [instance_id]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |

**Related Page**: View database parameter page (查看数据库参数相关页面)
```
{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-param-recommend?cluster=idc
```

***

### 20. get\_aas\_info - Get Active Session Statistics (AAS)

Get active session statistics summary.

**Python Call**:

```bash
python scripts/get_aas_info.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

**Related Page**: View performance insight page (查看性能洞察页面)
```
{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-performance-insight?cluster=idc
```

***

### 21. get\_related\_sql\_info - Get Root Cause SQL

Get root cause SQL that caused performance issues within a specified time range.

**Python Call**:

```bash
python scripts/get_related_sql_info.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

**Related Page**: View root cause SQL page (查看根因SQL页面)
```
{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/instance-diagnosis/{instance_id}/dbdoctor-root-cause-diagnosis?cluster=idc
```

***

### 22. get\_instance\_info - Get Instance Detailed Information

Get detailed instance information for diagnosis.

**Python Call**:

```bash
python scripts/get_instance_info.py --instance-id [instance_id]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |

**Related Page**: View instance list page (查看实例列表页面)
```
{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/doctor-instance-list?cluster=idc
```

***

### 23. get\_slow\_sql\_by\_time - Get Slow SQL by Time

Get slow SQL information within a specified time range (diagnosis version).

**Python Call**:

```bash
python scripts/get_slow_sql_by_time.py --instance-id [instance_id] --start-time [start_ts] --end-time [end_ts]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --start-time | string | Yes | Start timestamp (Unix seconds) |
| --end-time | string | Yes | End timestamp (Unix seconds) |

***

## SQL Rewrite Tools

### 24. ai\_sql\_rewrite - AI SQL Rewrite

Trigger AI-driven SQL rewrite optimization.

**Python Call**:

```bash
python scripts/ai_sql_rewrite.py --instance-id [instance_id] --database [db] --schema [schema] --sql "[sql]"
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --instance-id | string | Yes | Instance ID |
| --database | string | Yes | Database name |
| --schema | string | Yes | Schema name |
| --sql | string | Yes | SQL statement to rewrite (wrapped in quotes) |

***

### 25. get\_sql\_rewrite\_result - Get SQL Rewrite Result

Get the result of SQL rewrite task.

**Python Call**:

```bash
python scripts/get_sql_rewrite_result.py --task-id [task_id]
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --task-id | string | Yes | Task ID returned by ai\_sql\_rewrite |

***

---

### 26. get_sql_audit_rules - Get SQL Audit Rules

Get the list of SQL audit rules for a specified engine.

**Python Call**:

```bash
# Get all MySQL audit rules
python scripts/get_sql_audit_rules.py --engine mysql

# Get Oracle ERROR level rules
python scripts/get_sql_audit_rules.py --engine oracle --priority ERROR
```

**Parameters**:

| CLI Option | Type | Required | Description |
| --- | --- | --- | --- |
| --engine | string | No | Database engine (mysql/oracle/postgresql/dm/sqlserver etc.) |
| --rule-name | string | No | Rule name filter |
| --priority | string | No | Risk level (ERROR/WARNING/DANGER) |

**Rule Priority Description**:
- **ERROR**: Critical issues, must fix (e.g.: full table scan, poor indexing, foreign keys prohibited)
- **WARNING**: Warning issues, recommended to fix (e.g.: avoid using SELECT *, limit on number of indexed fields)
- **DANGER**: Dangerous operations, use with caution (e.g.: prohibit dropping tables, prohibit TRUNCATE)

**For detailed rule descriptions please refer to**: `reference/audit_and_inspection_rules.md`

---

## Notes

1. **Authentication**: The program automatically handles login, token acquisition, caching and refresh, no manual management required
2. **Timestamps**: Time range parameters use Unix timestamps (seconds)
3. **Schema**: For databases without schema concept (like MySQL), schema name is the same as database name
4. **Engine Types**: Supported engines include `mysql`, `oracle`, `postgresql`, `dm` (Dameng), `sqlserver`, `oracle-rac`
5. **Error Handling**: Check the `Code` or `Success` field in the response to determine if the request was successful
6. **Time Range Default**: If user doesn't provide time range, alert query defaults to last 2 hours
7. **Output Format**: All tools output formatted JSON by default
8. **SQL Parameter**: When --sql parameter contains spaces or special characters, please wrap it in quotes
9. **tenant/project Acquisition Specification**:
   - **⚠️ Strictly prohibited to fabricate tenant and project information**
   - Must dynamically obtain through `get_instance` tool
   - **Recommended**: Call `get_instance` without parameters to get all instance list
   - Find target instance from returned data and extract tenant and project fields
   - Prohibited from extracting directly from user input, input_data or other sources

10. **Performance Diagnosis Best Practices**:
    - Recommend using `performance_diagnosis` for comprehensive diagnosis, get complete report in one call
    - Recommended diagnosis time ranges: last 1 hour, last 6 hours, last 24 hours
    - For detailed performance diagnosis knowledge base please refer to: `reference/performance_diagnosis_guide.md`

11. **Interface Usage Constraints**:
    - **⚠️ Strictly prohibited to call interfaces not defined in this document**
    - Can only use tools and interfaces listed in the "Tool API Reference" chapter
    - Prohibited from fabricating or speculating interface paths
    - Prohibited from calling interfaces of other systems or services
    - All available interfaces are listed in the "Quick Reference: Parameter Requirements Summary" table

12. **Reference Document Index**:
    - `reference/performance_diagnosis_guide.md` - Performance Diagnosis Knowledge Base
    - `reference/best_practices.md` - Best Practices Guide (diagnosis flow, SQL optimization, performance troubleshooting, information collection)
    - `reference/audit_and_inspection_rules.md` - SQL Audit Rules and Inspection Rules Description
    - `reference/troubleshooting.md` - Common Issues and Solutions
    - `reference/agent_guidelines.md` - Agent Processing Strategies and Decision Guidelines (information collection matrix, detailed processing strategies, decision tree)

13. **Page Jump Links (Related Page)**:
    - Some tools have a **Related Page** section with a URL template for the corresponding DBDoctor web console page
    - URL template format: `{base_url}/#/dbDoctor/{tenant}/{project}/{role}/index/...`
    - Placeholders:
      - `{base_url}`: DBDOCTOR_URL from environment configuration (e.g., `http://localhost:8080`)
      - `{tenant}`: Tenant name (obtained from `get_instance`)
      - `{project}`: Project name (obtained from `get_instance`)
      - `{role}`: User role (default: `dev`)
      - `{instance_id}`: Instance ID
    - When presenting tool results, construct and provide the page link so users can jump to the corresponding web console page for detailed viewing
    - Tenant and project information must be obtained via `get_instance` tool before constructing the URL

***

## Quick Reference: Parameter Requirements Summary

| Tool | Required Parameters |
| --- | --- |
| get\_instance | None (returns all instances) |
| get\_current\_user | None (get current user tenant-project information) |
| get\_instance\_abnormal | --instance-id |
| get\_database\_by\_instance | --instance-id |
| manage\_instance | --ip, --port, --engine, --db-user, --db-password, --db-version, --tenant, --project |
| get\_slow\_sql | --instance-id, --start-time, --end-time |
| get\_table\_ddl | --instance-id, --database, --schema, --table |
| execute\_sql | --instance-id, --database, --schema, --sql, --engine, --tenant, --project (tenant/project can be obtained from get_instance) |
| sql\_audit | --instance-id, --database, --schema, --sql |
| get\_sql\_audit\_rules | --engine (optional), --priority (optional) |
| do\_inspect\_instance | --instance-id, --tenant (optional), --project (optional, tenant/project can be obtained from get_instance) |
| get\_recent\_inspect\_report | --instance-id, --start-time, --end-time, --tenant, --project (tenant/project can be obtained from get_instance) |
| get\_inspect\_item | None |
| get\_current\_process | --instance-id |
| alert\_message | --status (optional), --priority (optional), --instance-ip (optional) |
| performance\_diagnosis ⭐ | --instance-id, --start-time, --end-time (comprehensive diagnosis, recommended) |
| get\_basic\_monitor\_info | --instance-id, --start-time, --end-time |
| get\_host\_resource\_info | --instance-id, --start-time, --end-time |
| get\_db\_parameter\_info | --instance-id |
| get\_aas\_info | --instance-id, --start-time, --end-time |
| get\_related\_sql\_info | --instance-id, --start-time, --end-time |
| get\_instance\_info | --instance-id |
| get\_slow\_sql\_by\_time | --instance-id, --start-time, --end-time |
| ai\_sql\_rewrite | --instance-id, --database, --schema, --sql |
| get\_sql\_rewrite\_result | --task-id |

