
# CodeLens AI 贡献指南

我们欢迎任何形式的贡献！如果你想要为 CodeLens AI 项目做出贡献，请遵循以下指南。

## 如何开始

### 1. 提出问题
如果你发现了问题或有改进建议，请先查看 [Issues](../../issues) 页面，确认问题是否已经存在。

### 2. 创建分支
从 `main` 分支创建一个新的分支：
```bash
git checkout -b feature/your-feature-name
```

### 3. 开发
根据我们的 [开发指南](./DEVELOPMENT.md) 进行开发。

### 4. 测试
确保你的代码通过了所有测试：
```bash
pytest
```

### 5. 提交代码
使用语义化提交信息：
```bash
git add .
git commit -m "feat: 添加新功能"
git push origin feature/your-feature-name
```

### 6. 提交 PR
在 GitHub 上提交 Pull Request，描述你的修改内容和原因。

## 代码风格

### Python
- 使用 4 空格缩进
- 使用 PEP 8 风格
- 使用类型提示（Type Hints）
- 使用绝对导入

### JavaScript/TypeScript
- 使用 2 空格缩进
- 使用 ES6+ 语法
- 使用 TypeScript 类型注解

## 提交规范

我们使用以下提交前缀：
- `feat`: 添加新功能
- `fix`: 修复 bug
- `docs`: 文档修改
- `style`: 代码风格修改（不影响代码运行）
- `refactor`: 重构代码
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

## 问题报告

### Bug 报告
当你发现 Bug 时，请提供以下信息：
1. 操作系统和版本
2. Python 版本
3. CodeLens AI 版本
4. 复现步骤
5. 预期行为
6. 实际行为

### 功能请求
请描述：
1. 功能的概述
2. 功能的详细说明
3. 使用场景
4. 预期的实现方式

## 社区准则

我们遵循以下行为准则：
- 尊重他人
- 保持友好
- 提供有价值的反馈
- 帮助他人

## 联系我们

如果你有任何问题，可以通过以下方式联系我们：
- 打开 [Issue](../../issues)
- 发送邮件到 support@codelens-ai.com

## 许可证

通过贡献代码，你同意将你的贡献发布在 MIT 许可证下。
