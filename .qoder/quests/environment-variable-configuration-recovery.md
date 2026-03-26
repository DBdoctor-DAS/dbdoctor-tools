# 配置方式回退：从 .dbdoctor 配置文件恢复为环境变量

## 背景

当前项目通过项目根目录下的 `.dbdoctor` JSON 配置文件读取 DBDoctor 连接信息（`dbdoctor_url`、`dbdoctor_user`、`dbdoctor_password`）。现需将配置方式回退为通过系统环境变量读取，环境变量名沿用原有字段名的大写形式。

## 环境变量定义

| 环境变量名 | 描述 | 示例值 |
|---|---|---|
| DBDOCTOR_URL | DBDoctor API 基础地址 | http://[host]:[port] |
| DBDOCTOR_USER | 登录用户名（同时作为 UserId） | [username] |
| DBDOCTOR_PASSWORD | 登录密码（明文，程序自动 AES 加密） | [password] |

## 变更范围

### 1. common/config.py

**变更内容**：将配置读取方式从 JSON 文件改为 `os.environ` 环境变量。

- 移除 `_CONFIG_FILE` 路径常量和 `_REQUIRED_FIELDS` 元组
- 移除 `_load_config_file()` 静态方法（含文件读取、JSON 解析逻辑）
- 移除 `json` 模块导入
- `Config.__init__` 改为从 `os.environ` 读取三个环境变量（`DBDOCTOR_URL`、`DBDOCTOR_USER`、`DBDOCTOR_PASSWORD`）
- 任一环境变量缺失时抛出 `ConfigError`，错误信息中提示需要设置的环境变量名
- 模块顶部文档注释更新为描述环境变量配置方式
- `ConfigError` 类和全局单例 `config = Config()` 保持不变
- `Config` 对外暴露的属性（`base_url`、`username`、`password`、`user_id`、`role`）保持不变，确保 `auth.py`、`client.py` 等下游模块无需任何修改

### 2. SKILL.md

**变更内容**：将所有关于 `.dbdoctor` 配置文件的说明替换为环境变量方式。

具体涉及以下段落：

- "使用技能前 > 1. 配置文件检查" 段落：改为"环境变量检查"，说明检查 `DBDOCTOR_URL`、`DBDOCTOR_USER`、`DBDOCTOR_PASSWORD` 是否已设置，未设置时提示用户配置
- "环境配置" 段落中的配置文件表格和 JSON 示例：替换为环境变量设置方式说明
- "认证机制" 描述：将"从配置文件读取"改为"从环境变量读取"

### 3. 删除 .dbdoctor 配置文件

如果项目根目录下存在 `.dbdoctor` 文件，将其删除。根据项目规范（.env 文件仅在需要时保留），回退到环境变量后该文件不再需要。

## 不变更的部分

- common/auth.py：通过 `from common.config import config` 引用，`config` 对外接口不变，无需改动
- common/client.py：同上，无需改动
- scripts/ 目录下所有脚本：间接依赖 config，无需改动
- Token 缓存机制（`.token_cache`）：与配置读取方式无关，保持不变
- requirements.txt：无新增或移除依赖
