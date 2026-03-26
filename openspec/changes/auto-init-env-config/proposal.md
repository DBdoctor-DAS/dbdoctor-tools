## Why

当前 dbdoctor-tools Skill 要求用户手动创建 `.env` 文件并填入配置，增加了使用门槛。为了提升用户体验，实现**零配置上手**，需要在首次使用时自动检测配置缺失并引导用户完成初始化，自动生成 `.env` 文件。

## What Changes

- 修改 `common/config.py`，在配置缺失时自动触发交互式初始化流程
- 新增配置引导功能，提示用户输入 DBDoctor 连接信息
- 自动生成 `.env` 文件并保存用户配置
- 初始化完成后自动继续执行原脚本
- 更新 `SKILL.md` 文档，简化配置说明

## Capabilities

### New Capabilities
- `auto-env-init`: 自动检测并初始化环境变量配置，包括交互式引导、配置验证、文件生成

### Modified Capabilities
- 无（此变更为纯实现层优化，不改变现有功能行为）

## Impact

- `common/config.py`: 核心配置模块，添加自动初始化逻辑
- `SKILL.md`: 更新使用文档，移除手动创建 `.env` 的步骤
- 用户体验: 首次使用无需手动创建配置文件，降低使用门槛
