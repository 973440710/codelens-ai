
# CodeLens AI - AI驱动的代码优化工具 🚀

[![GitHub stars](https://img.shields.io/github/stars/973440710/codelens-ai.svg?style=social&label=Stars)](https://github.com/973440710/codelens-ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/973440710/codelens-ai/blob/main/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/codelens-ai.svg)](https://pypi.org/project/codelens-ai/)
[![Python version](https://img.shields.io/pypi/pyversions/codelens-ai.svg)](https://pypi.org/project/codelens-ai/)

**CodeLens AI** 是一个由人工智能驱动的代码优化工具，通过分析代码结构和语义，提供智能的代码优化建议，帮助开发者提高代码质量和开发效率。

## 🎯 核心功能

### ✨ 智能代码优化
- **AI驱动分析**：使用 GPT-4o 和 Gemini 1.5 Pro 进行代码理解和优化
- **多语言支持**：支持 Python、JavaScript、TypeScript
- **一键优化**：自动应用优化建议
- **上下文感知**：理解代码的语义和上下文，提供精准的优化建议

### 📊 详细报告
- **HTML报告**：生成美观的优化报告，显示优化前后对比
- **代码质量分析**：识别代码质量问题和改进建议
- **优化统计**：显示优化效果的详细数据

### 🚀 易用的CLI工具
- **简单命令**：`codelens analyze` 快速分析代码
- **配置管理**：`codelens config` 管理API密钥和设置
- **彩色输出**：使用 Rich 库提供美观的彩色界面

## 📦 安装

### 快速安装
```bash
pip install codelens-ai
```

### 从源码安装
```bash
git clone https://github.com/973440710/codelens-ai.git
cd codelens-ai
pip install -r requirements.txt
pip install -e .
```

## 🔧 使用

### 1. 配置API密钥
在第一次使用前，需要配置 OpenAI 和 Google Gemini 的 API 密钥：
```bash
codelens config
```

### 2. 分析代码
分析单个文件或目录：
```bash
# 分析单个文件
codelens analyze my_code.py

# 分析目录
codelens analyze /path/to/my/project

# 指定语言
codelens analyze /path/to/my/project --language python

# 自动修复
codelens analyze /path/to/my/project --auto-fix
```

### 3. 查看优化报告
```bash
codelens analyze /path/to/my/project --report my_report.html
```

## 📈 优化效果示例

### 原始代码（Python）
```python
def calculate_total(items):
    total = 0
    for i in range(len(items)):
        total += items[i]
    return total
```

### 优化后代码
```python
def calculate_total(items):
    return sum(items)
```

## 🎮 支持的语言

| 语言 | 状态 | 版本 |
|------|------|------|
| Python | ✅ 支持 | 3.8+ |
| JavaScript | ✅ 支持 | ES6+ |
| TypeScript | ✅ 支持 | 4.0+ |
| Java | 🚧 开发中 | - |
| Go | 🚧 开发中 | - |
| C++ | 🚧 开发中 | - |

## 🔌 技术架构

```
┌───────────────────────────────────────────────────────────────────────────┐
│                              CodeLens AI                                 │
├───────────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ CLI工具  │ │ 代码分析器│ │ AI优化器 │ │ 报告生成器│ │ 配置管理 │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│                                                                           │
│  ┌───────────────────────────────────────────────────────────────────────┐
│  │                            核心依赖                                    │
│  ├───────────────────────────────────────────────────────────────────────┤
│  │ OpenAI GPT-4o     │ Google Gemini 1.5 Pro │ Python AST解析            │
│  ├───────────────────────────────────────────────────────────────────────┤
│  │ Click (CLI)       │ Rich (彩色输出)      │ PyYAML (配置)             │
│  └───────────────────────────────────────────────────────────────────────┘
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

## 🤝 贡献

欢迎贡献！请阅读我们的 [CONTRIBUTING.md](./CONTRIBUTING.md) 来了解如何参与项目开发。

### 开发流程
1. Fork 项目
2. 创建分支 (`git checkout -b feature/AmazingFeature`)
3. 提交修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](./LICENSE) 文件了解详情。

## 📞 支持

如果您有任何问题或建议，请：
1. 查看我们的 [文档](https://github.com/973440710/codelens-ai/wiki)
2. 查看 [问题列表](https://github.com/973440710/codelens-ai/issues)
3. 提交新的 [问题](https://github.com/973440710/codelens-ai/issues/new)

## 🌟 社区

加入我们的社区，与其他开发者一起学习和成长！

- **GitHub Issues**: https://github.com/973440710/codelens-ai/issues
- **Discord**: https://discord.gg/codelens-ai
- **Twitter**: https://twitter.com/codelens_ai

---

**CodeLens AI - 让代码优化变得简单！** 🚀
