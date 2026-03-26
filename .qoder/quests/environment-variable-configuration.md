# 配置方式从环境变量迁移到本地配置文件

## 背景与问题

当前 `common/config.py` 通过 `os.environ.get()` 读取 `dbdoctor_url`、`dbdoctor_user`、`dbdoctor_password` 三个环境变量。环境变量是会话级别的（`set`/`export` 仅对当前终端窗口有效），每次新开终端或 IDE 重启后都需要重新配置，导致频繁出现"缺少必需的环境变量"错误。

## 目标

1. 将三项配置（`dbdoctor_url`、`dbdoctor_user`、`dbdoctor_password`）持久化到本地文件，一次写入、长期有效，仅在需要时手动更新。
2. Token 缓存机制保持不变（`auth.py` 已实现 `.token_cache` 文件缓存）。
3. 同步更新 `SKILL.md` 中的配置说明和检查方式。
4. 修正 `SKILL.md` 快速参考表中 `get_instance` 的参数描述，明确 tenant/project 为可选参数。

## 变更范围

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| common/config.py | 修改 | 从读取环境变量改为读取本地配置文件 |
| SKILL.md | 修改 | 配置说明从环境变量改为配置文件方式；修正 get_instance 参数描述 |

## 详细设计

### 1. 配置文件方案

**文件路径**：项目根目录下 `.dbdoctor` 文件（与 `.token_cache` 同级）。

**文件格式**：采用 JSON 格式，结构简单、Python 标准库原生支持，无需额外依赖。

**文件内容结构**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dbdoctor_url | string | 是 | API 基础地址，如 `http://host:port` |
| dbdoctor_user | string | 是 | 登录用户名（同时作为 UserId） |
| dbdoctor_password | string | 是 | 登录密码（明文，程序自动加密） |

### 2. config.py 改造

**当前行为**：`Config.__init__` 中通过 `os.environ.get()` 读取三个环境变量，缺失时抛出 `ConfigError`。

**目标行为**：

- 读取项目根目录下的 `.dbdoctor` 配置文件（JSON 格式）
- 文件不存在时，抛出 `ConfigError`，提示用户创建配置文件并给出文件路径和所需字段
- 文件存在但缺少必填字段时，抛出 `ConfigError`，提示缺少的具体字段
- 文件路径的定位方式：基于 `config.py` 自身位置向上一级（即项目根目录），与现有 `.token_cache` 的路径计算逻辑一致

**配置单例保持不变**：模块底部的 `config = Config()` 全局单例机制不变，其他模块的引用方式 `from common.config import config` 无需改动。

### 3. SKILL.md 更新

需要更新以下几处内容：

#### 3.1 "使用技能前 - 环境变量检查" 部分

将"环境变量检查"改为"配置文件检查"，说明：
- 检查项目根目录下是否存在 `.dbdoctor` 配置文件
- 如不存在，提示用户在项目根目录创建该文件，写入 `dbdoctor_url`、`dbdoctor_user`、`dbdoctor_password` 三个字段
- 如需更新配置，直接编辑该文件即可

#### 3.2 "环境配置" 部分

- 将"环境变量"表格改为"配置文件字段"表格（字段名、类型、描述不变）
- 将"设置环境变量"的 `export`/`set` 命令说明替换为：在项目根目录创建 `.dbdoctor` 文件并写入 JSON 内容的说明
- "认证机制"描述中移除"环境变量"相关措辞，改为"从配置文件读取"

#### 3.3 快速参考表中 get_instance 行

当前描述：`--tenant, --project`（显示为必需参数）

修正为：`--tenant（可选）, --project（可选）`，与 `get_instance.py` 代码实际行为一致（两个参数 `default=None`，已支持不传）。

### 4. Token 缓存

无需变更。`auth.py` 已将 Token 缓存到 `.token_cache` 文件中，支持自动读取和刷新。

### 5. .gitignore 建议

`.dbdoctor` 配置文件包含敏感信息（密码），应确认已被 `.gitignore` 忽略，避免意外提交到版本库。
