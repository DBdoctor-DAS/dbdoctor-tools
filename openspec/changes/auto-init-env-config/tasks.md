## 1. Core Implementation

- [ ] 1.1 修改 `common/config.py`，添加 `is_interactive()` 函数检测 TTY 环境
- [ ] 1.2 在 `common/config.py` 中添加 `interactive_init()` 函数实现交互式配置引导
- [ ] 1.3 在 `common/config.py` 中添加 `generate_env_file()` 函数生成 `.env` 文件
- [ ] 1.4 修改 `Config.__init__()` 方法，集成自动初始化逻辑
- [ ] 1.5 添加输入验证逻辑（URL 格式、非空检查）

## 2. Testing & Verification

- [ ] 2.1 在无 `.env` 文件环境下测试自动初始化流程
- [ ] 2.2 验证已有 `.env` 文件时不会触发交互
- [ ] 2.3 验证系统环境变量优先级高于 `.env` 文件
- [ ] 2.4 在非 TTY 环境（如重定向输入）测试错误提示
- [ ] 2.5 测试生成的 `.env` 文件格式正确且能被正确加载

## 3. Documentation Update

- [ ] 3.1 更新 `SKILL.md` 中 "Environment Configuration" 章节，说明自动初始化功能
- [ ] 3.2 移除 SKILL.md 中手动创建 `.env` 的复杂步骤，简化为"首次使用自动引导"
- [ ] 3.3 更新 `scripts/test_env.py`，添加对自动初始化功能的检测提示

## 4. Edge Cases & Polish

- [ ] 4.1 处理用户在中途取消输入的情况（Ctrl+C）
- [ ] 4.2 确保 Windows PowerShell 和 CMD 环境下密码输入隐藏正常
- [ ] 4.3 添加友好的欢迎信息和配置完成提示
