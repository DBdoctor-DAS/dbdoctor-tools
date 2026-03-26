# SKILL.md 改造及工具 Main 方法添加设计

## 1. 变更概述

将 SKILL.md 中所有工具的调用方式从 Bash/curl 完全替换为 Python CLI 调用，同时为 tools/ 目录下每个工具文件添加 main() 入口函数，使其支持命令行直接调用。

## 2. 涉及变更的文件清单

| 类别 | 文件 | 变更类型 |
|---|---|---|
| 文档 | SKILL.md | 环境配置、工具 API 参考、Notes、快速参考表全面重写 |
| 工具 | tools/get_instance.py | 添加 main 方法 |
| 工具 | tools/get_instance_abnormal.py | 添加 main 方法 |
| 工具 | tools/get_instance_info.py | 添加 main 方法 |
| 工具 | tools/get_database_by_instance.py | 添加 main 方法 |
| 工具 | tools/manage_instance.py | 添加 main 方法（含密码加密逻辑） |
| 工具 | tools/get_slow_sql.py | 添加 main 方法 |
| 工具 | tools/get_slow_sql_by_time.py | 添加 main 方法 |
| 工具 | tools/get_table_ddl.py | 添加 main 方法 |
| 工具 | tools/execute_sql.py | 添加 main 方法 |
| 工具 | tools/sql_audit.py | 添加 main 方法 |
| 工具 | tools/get_sql_audit_rules.py | 添加 main 方法 |
| 工具 | tools/do_inspect_instance.py | 添加 main 方法 |
| 工具 | tools/get_recent_inspect_report.py | 添加 main 方法 |
| 工具 | tools/get_inspect_item.py | 添加 main 方法 |
| 工具 | tools/get_current_process.py | 添加 main 方法 |
| 工具 | tools/alert_message.py | 添加 main 方法 |
| 工具 | tools/get_basic_monitor_info.py | 添加 main 方法 |
| 工具 | tools/get_host_resource_info.py | 添加 main 方法 |
| 工具 | tools/get_db_parameter_info.py | 添加 main 方法 |
| 工具 | tools/get_aas_info.py | 添加 main 方法 |
| 工具 | tools/get_related_sql_info.py | 添加 main 方法 |
| 工具 | tools/ai_sql_rewrite.py | 添加 main 方法 |
| 工具 | tools/get_sql_rewrite_result.py | 添加 main 方法 |

## 3. 环境配置部分重写

### 3.1 替换范围

SKILL.md 第 17-56 行（"环境配置" 整节），替换为 Python 环境变量 + 依赖安装方式。

### 3.2 新环境配置内容

**环境变量**（替代原 .env 文件方案）：

| 环境变量 | 描述 | 示例 |
|---|---|---|
| dbdoctor_url | DBDoctor API 基础地址 | http://[host]:[port] |
| dbdoctor_user | 登录用户名（同时作为 UserId） | [username] |
| dbdoctor_password | 登录密码（明文，程序自动 RSA 加密） | [password] |

**SKILL.md 中应提供的设置指引**：

- Linux/Mac 设置方式：通过 export 命令设置三个环境变量
- Windows 设置方式：通过 set 命令设置三个环境变量
- 依赖安装：pip install -r requirements.txt（包含 requests 和 pycryptodome）
- 认证机制说明：程序自动完成密码 RSA 加密、登录获取 Token、Token 文件缓存（.token_cache）与自动刷新，无需手动管理 auth_token

### 3.3 移除内容

- 移除 .env 文件内容示例
- 移除 bash 加载环境变量的脚本
- 移除 AUTH_TOKEN、ROLE、TENANT、PROJECT 等手动配置项（这些由程序内部管理或作为工具参数传入）

## 4. 工具 Main 方法设计

### 4.1 通用设计模式

每个工具文件统一按以下模式添加 main 方法：

**新增导入**：argparse、json、sys

**main() 函数行为**：
1. 创建 ArgumentParser，description 为该工具的中文功能描述
2. 通过 add_argument 定义 CLI 参数（必需参数使用 required=True，可选参数使用 default 值）
3. 解析参数后调用该文件已有的核心工具函数
4. 成功时：json.dumps(result, ensure_ascii=False, indent=2) 输出到 stdout
5. 异常时：错误信息输出到 stderr，sys.exit(1)

**入口守卫**：文件末尾添加 if \_\_name\_\_ == "\_\_main\_\_": main()

**调用方式**：从项目根目录执行 python tools/\<file\_name\>.py [参数]

### 4.2 各工具 CLI 参数详表

以下表格列出每个工具的 CLI 参数设计。所有参数均使用 --name 格式。

#### 实例管理类

| 工具文件 | CLI 参数 |
|---|---|
| get\_instance.py | --tenant（必需，租户名称）, --project（必需，项目名称） |
| get\_instance\_abnormal.py | --instance-id（必需，实例ID） |
| get\_instance\_info.py | --instance-id（必需，实例ID） |
| get\_database\_by\_instance.py | --instance-id（必需，实例ID） |
| manage\_instance.py | --ip（必需）, --port（必需，int 类型）, --engine（必需，choices: mysql/oracle/postgresql/dm/sqlserver/oracle-rac）, --db-user（必需）, --db-password（必需，明文密码）, --db-version（必需）, --tenant（必需）, --project（必需）, --description（可选，默认空） |

#### SQL 分析类

| 工具文件 | CLI 参数 |
|---|---|
| get\_slow\_sql.py | --instance-id（必需）, --start-time（必需，Unix 时间戳）, --end-time（必需，Unix 时间戳） |
| get\_slow\_sql\_by\_time.py | --instance-id（必需）, --start-time（必需）, --end-time（必需） |
| get\_table\_ddl.py | --instance-id（必需）, --database（必需）, --schema（必需）, --table（必需） |
| execute\_sql.py | --instance-id（必需）, --database（必需）, --schema（必需）, --sql（必需）, --engine（必需）, --tenant（必需）, --project（必需） |
| sql\_audit.py | --instance-id（必需）, --database（必需）, --schema（必需）, --sql（必需） |
| get\_sql\_audit\_rules.py | --engine（可选）, --rule-name（可选）, --priority（可选，choices: ERROR/WARNING/DANGER） |

#### 巡检类

| 工具文件 | CLI 参数 |
|---|---|
| do\_inspect\_instance.py | --instance-id（必需） |
| get\_recent\_inspect\_report.py | --instance-id（必需）, --start-time（必需）, --end-time（必需）, --tenant（必需）, --project（必需） |
| get\_inspect\_item.py | 无参数 |

#### 会话与告警类

| 工具文件 | CLI 参数 |
|---|---|
| get\_current\_process.py | --instance-id（必需）, --database（可选）, --sql-keyword（可选） |
| alert\_message.py | --status（可选，choices: alarming/recovered）, --priority（可选，choices: serious/warning/info）, --event-name（可选）, --instance-ip（可选）, --instance-desc（可选）, --create-time（可选）, --modified-time（可选） |

#### 性能诊断类

| 工具文件 | CLI 参数 |
|---|---|
| get\_basic\_monitor\_info.py | --instance-id（必需）, --start-time（必需）, --end-time（必需） |
| get\_host\_resource\_info.py | --instance-id（必需）, --start-time（必需）, --end-time（必需） |
| get\_db\_parameter\_info.py | --instance-id（必需） |
| get\_aas\_info.py | --instance-id（必需）, --start-time（必需）, --end-time（必需） |
| get\_related\_sql\_info.py | --instance-id（必需）, --start-time（必需）, --end-time（必需） |

#### SQL 改写类

| 工具文件 | CLI 参数 |
|---|---|
| ai\_sql\_rewrite.py | --instance-id（必需）, --database（必需）, --schema（必需）, --sql（必需） |
| get\_sql\_rewrite\_result.py | --task-id（必需） |

## 5. SKILL.md 工具 API 参考部分重写

### 5.1 替换范围

SKILL.md 第 341-1005 行（"工具 API 参考" 各小节），将每个工具的 "Bash 调用" 代码块替换为 "Python 调用" 代码块。

### 5.2 各工具节统一文档模板

每个工具节的新格式如下（替换原有的 "Bash 调用" + curl 命令）：

```
### N. tool_name - 工具中文名

功能描述。

**Python 调用**：

（此处给出 python tools/xxx.py --param value 的调用示例）

**参数**：

（参数表，包含 CLI 选项、类型、是否必需、描述）
```

### 5.3 各工具具体调用示例

以下按序号列出每个工具在 SKILL.md 中应展示的 Python 调用示例。

#### 时间戳工具（原第 0 节）

原来使用 bash date 命令获取时间戳，替换为 Python 时间计算方式。提供 Python 内联计算时间戳的说明：

- 获取当前 Unix 时间戳（秒）：使用 Python 的 time.time()
- 常用时间范围计算表保留（最近1小时=3600秒，最近2小时=7200秒等）
- 完整示例：获取最近2小时慢SQL，先用 Python 算出 start/end 时间戳，再调用 python tools/get\_slow\_sql.py

#### 1. get\_instance - 获取实例基本信息

调用示例：python tools/get\_instance.py --tenant [tenant] --project [project]

#### 2. get\_instance\_abnormal - 获取实例异常信息

调用示例：python tools/get\_instance\_abnormal.py --instance-id [instance\_id]

#### 3. get\_database\_by\_instance - 获取实例下的数据库

调用示例：python tools/get\_database\_by\_instance.py --instance-id [instance\_id]

#### 4. manage\_instance - 纳管数据库实例

调用示例：python tools/manage\_instance.py --ip [ip] --port [port] --engine mysql --db-user [user] --db-password [password] --db-version [version] --tenant [tenant] --project [project]

说明：--db-password 接受明文密码，程序内部自动完成 RSA 加密。

#### 5. get\_slow\_sql - 获取慢SQL列表

调用示例：python tools/get\_slow\_sql.py --instance-id [instance\_id] --start-time [start\_ts] --end-time [end\_ts]

#### 6. get\_table\_ddl - 获取表DDL

调用示例：python tools/get\_table\_ddl.py --instance-id [instance\_id] --database [db] --schema [schema] --table [table]

#### 7. execute\_sql - 执行SQL语句

调用示例：python tools/execute\_sql.py --instance-id [instance\_id] --database [db] --schema [schema] --sql "[sql]" --engine mysql --tenant [tenant] --project [project]

#### 8. sql\_audit - SQL审核

调用示例：python tools/sql\_audit.py --instance-id [instance\_id] --database [db] --schema [schema] --sql "[sql]"

说明：内部自动完成提交审核+轮询结果的两步流程，无需手动分步调用。

#### 9. get\_sql\_audit\_rules - 获取SQL审核规则

调用示例：python tools/get\_sql\_audit\_rules.py --engine mysql --priority ERROR

#### 10. do\_inspect\_instance - 执行实例巡检

调用示例：python tools/do\_inspect\_instance.py --instance-id [instance\_id]

说明：内部自动完成获取巡检模板+执行巡检的两步流程。

#### 11. get\_recent\_inspect\_report - 获取最近巡检报告

调用示例：python tools/get\_recent\_inspect\_report.py --instance-id [instance\_id] --start-time [start\_ts] --end-time [end\_ts] --tenant [tenant] --project [project]

#### 12. get\_inspect\_item - 获取巡检项

调用示例：python tools/get\_inspect\_item.py

#### 13. get\_current\_process - 获取当前会话

调用示例：python tools/get\_current\_process.py --instance-id [instance\_id] --database [db] --sql-keyword [keyword]

#### 14. alert\_message - 获取告警概览

调用示例：python tools/alert\_message.py --status alarming --priority serious

#### 15. get\_basic\_monitor\_info - 获取数据库监控指标

调用示例：python tools/get\_basic\_monitor\_info.py --instance-id [instance\_id] --start-time [start\_ts] --end-time [end\_ts]

#### 16. get\_host\_resource\_info - 获取主机资源指标

调用示例：python tools/get\_host\_resource\_info.py --instance-id [instance\_id] --start-time [start\_ts] --end-time [end\_ts]

#### 17. get\_db\_parameter\_info - 获取数据库参数

调用示例：python tools/get\_db\_parameter\_info.py --instance-id [instance\_id]

#### 18. get\_aas\_info - 获取活跃会话统计(AAS)

调用示例：python tools/get\_aas\_info.py --instance-id [instance\_id] --start-time [start\_ts] --end-time [end\_ts]

#### 19. get\_related\_sql\_info - 获取根因SQL

调用示例：python tools/get\_related\_sql\_info.py --instance-id [instance\_id] --start-time [start\_ts] --end-time [end\_ts]

#### 20. get\_instance\_info - 获取实例详细信息

调用示例：python tools/get\_instance\_info.py --instance-id [instance\_id]

#### 21. get\_slow\_sql\_by\_time - 按时间获取慢SQL

调用示例：python tools/get\_slow\_sql\_by\_time.py --instance-id [instance\_id] --start-time [start\_ts] --end-time [end\_ts]

#### 22. ai\_sql\_rewrite - AI SQL改写

调用示例：python tools/ai\_sql\_rewrite.py --instance-id [instance\_id] --database [db] --schema [schema] --sql "[sql]"

#### 23. get\_sql\_rewrite\_result - 获取SQL改写结果

调用示例：python tools/get\_sql\_rewrite\_result.py --task-id [task\_id]

## 6. SKILL.md 其他部分变更

### 6.1 Notes 部分更新（原第 1007-1016 行）

需要更新的条目：

| 原内容 | 新内容 |
|---|---|
| 认证：所有请求都需要 auth_token 请求头进行认证 | 认证：程序自动处理登录、Token 获取、缓存与刷新，无需手动管理 |
| JSON 处理：可以使用 jq 工具美化 JSON 输出 | 输出格式：所有工具默认以格式化 JSON 输出结果 |

其余条目（时间戳、Schema、引擎类型、错误处理、时间范围默认值）保持不变。

### 6.2 快速参考表更新（原第 1019-1048 行）

保留表格结构，将 "必需参数" 列的参数名更新为 CLI 选项格式（如 INSTANCE\_ID 改为 --instance-id）。

### 6.3 不变的部分

以下 SKILL.md 内容保持不变，无需修改：

- 第 1-15 行：文档头部和角色描述
- 第 60-73 行：严格禁止的行为
- 第 77-88 行：信息收集矩阵
- 第 91-303 行：详细处理策略和决策树
- 第 307-338 行：重要规则和快速判断指南

## 7. 特殊处理说明

### 7.1 manage\_instance 密码处理

当前 manage\_instance() 函数接受 encrypted\_password（已 RSA 加密的密码）。CLI 模式下 main 方法应：
- 通过 --db-password 接受明文密码
- 在 main 方法内调用 common.auth 模块的 encrypt\_password() 函数完成加密
- 将加密后的密码传递给 manage\_instance() 函数

### 7.2 SQL 参数中的特殊字符

--sql 参数可能包含空格、引号等特殊字符。SKILL.md 中应提示用户使用引号包裹 SQL 内容。

### 7.3 时间戳参数类型

所有 --start-time 和 --end-time 参数在 argparse 中定义为 string 类型（与当前函数签名一致），值为 Unix 秒级时间戳。get\_recent\_inspect\_report 的时间戳参数为 int 类型，需在 argparse 中指定 type=int。

### 7.4 工具编号调整

当前 SKILL.md 工具编号从 0（时间戳工具）到 23。改造后时间戳部分不再是独立工具（改为说明性文本），其余工具编号从 1 开始顺序排列，与上文第 5.3 节一致。
