
# CodeLens AI - Makefile
# 自动化构建和测试工具

.PHONY: all install test coverage lint clean build run help

# 变量
VENV := .venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
FLAKE8 := $(VENV)/bin/flake8

# 默认目标
all: install test

# 创建虚拟环境
$(VENV):
	@echo "🔧 创建虚拟环境..."
	@python3 -m venv $(VENV)

# 安装依赖
install: $(VENV)
	@echo "📦 安装依赖包..."
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@$(PIP) install -e .

# 运行测试
test: install
	@echo "🧪 运行测试..."
	@$(PYTEST) tests/ -v -x

# 运行覆盖率分析
coverage: install
	@echo "📊 运行覆盖率分析..."
	@$(PYTEST) tests/ -v --tb=short --cov=src --cov-report=term --cov-report=html:coverage_report

# 代码检查
lint: install
	@echo "🔍 运行代码检查..."
	@$(FLAKE8) src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	@$(FLAKE8) src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# 清理项目
clean:
	@echo "🗑️  清理项目..."
	@rm -rf $(VENV)
	@rm -rf __pycache__
	@rm -rf *.pyc
	@rm -rf .pytest_cache
	@rm -rf coverage_report
	@rm -rf dist
	@rm -rf build
	@rm -rf *.egg-info
	@find . -name "__pycache__" -type d -exec rm -rf {} +

# 构建项目
build: install clean
	@echo "🚀 构建项目..."
	@$(PYTHON) -m pip install --upgrade build
	@$(PYTHON) -m build

# 运行工具
run: install
	@echo "▶️  运行 CodeLens AI..."
	@$(PYTHON) cli.py --help

# 帮助信息
help:
	@echo "CodeLens AI - 自动化构建和测试工具"
	@echo
	@echo "可用命令:"
	@echo "  make install    - 安装依赖包"
	@echo "  make test       - 运行所有测试"
	@echo "  make coverage   - 运行测试并生成覆盖率报告"
	@echo "  make lint       - 运行代码检查"
	@echo "  make clean      - 清理项目"
	@echo "  make build      - 构建项目"
	@echo "  make run        - 运行 CodeLens AI 工具"
	@echo "  make help       - 显示此帮助信息"
