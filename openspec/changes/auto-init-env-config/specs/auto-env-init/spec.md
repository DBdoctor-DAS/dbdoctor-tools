## ADDED Requirements

### Requirement: 自动检测配置缺失
当系统检测到必需的环境变量未设置时，SHALL 触发自动初始化流程。

#### Scenario: 首次使用无配置
- **GIVEN** 用户首次使用 dbdoctor-tools，无 `.env` 文件且无系统环境变量
- **WHEN** 任意脚本导入 `common.config` 模块
- **THEN** 系统自动触发交互式配置引导

#### Scenario: 已有系统环境变量
- **GIVEN** 用户已设置系统环境变量 DBDOCTOR_URL, DBDOCTOR_USER, DBDOCTOR_PASSWORD
- **WHEN** 任意脚本导入 `common.config` 模块
- **THEN** 系统直接加载环境变量，不触发交互式配置

#### Scenario: 已有 .env 文件
- **GIVEN** 用户已有完整的 `.env` 配置文件
- **WHEN** 任意脚本导入 `common.config` 模块
- **THEN** 系统自动加载 `.env` 文件，不触发交互式配置

### Requirement: 交互式配置引导
系统 SHALL 提供交互式命令行界面，引导用户输入必需的配置信息。

#### Scenario: 引导输入 URL
- **WHEN** 系统触发初始化流程
- **THEN** 提示用户输入 "请输入 DBDoctor URL (例如: http://localhost:8080):"
- **AND** 验证输入不为空

#### Scenario: 引导输入用户名
- **WHEN** 用户完成 URL 输入
- **THEN** 提示用户输入 "请输入 DBDoctor 用户名:"
- **AND** 验证输入不为空

#### Scenario: 隐藏密码输入
- **WHEN** 用户完成用户名输入
- **THEN** 提示用户输入 "请输入 DBDoctor 密码:"
- **AND** 输入时不在终端显示字符（使用 getpass）
- **AND** 验证输入不为空

### Requirement: 自动生成 .env 文件
系统 SHALL 根据用户输入自动生成 `.env` 配置文件。

#### Scenario: 成功生成配置文件
- **GIVEN** 用户已完成所有配置项输入
- **WHEN** 系统验证输入有效
- **THEN** 在项目根目录创建 `.env` 文件
- **AND** 文件内容格式与 `.env.example` 模板一致
- **AND** 文件权限设置为仅所有者可读写（Unix 系统）

#### Scenario: 配置立即生效
- **GIVEN** 系统已生成 `.env` 文件
- **WHEN** 初始化流程完成
- **THEN** 新配置立即加载到当前进程环境变量
- **AND** 脚本正常继续执行

### Requirement: 非交互式环境处理
系统 SHALL 检测运行环境，在非交互式环境中提供明确的错误信息。

#### Scenario: CI/CD 环境检测
- **GIVEN** 脚本运行在非 TTY 环境（如 CI/CD 管道）
- **WHEN** 配置缺失需要交互输入
- **THEN** 抛出 ConfigError 异常
- **AND** 错误信息明确提示 "请在系统环境变量或 .env 文件中配置"
