
"""
CodeLens AI - 项目设置文件
用于打包和分发工具
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = [line.strip() for line in f if line.strip()]

setup(
    name="codelens-ai",
    version="1.0.0",
    description="CodeLens AI - AI驱动的代码优化工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="小T & 小A",
    author_email="support@codelens-ai.com",
    url="https://github.com/yourusername/codelens-ai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "codelens = cli:main",
        ],
    },
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    keywords=[
        "AI",
        "code-optimization",
        "refactoring",
        "code-quality",
        "developer-tools"
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/codelens-ai/issues",
        "Source": "https://github.com/yourusername/codelens-ai",
        "Documentation": "https://github.com/yourusername/codelens-ai/wiki",
    },
    include_package_data=True,
    zip_safe=False,
)
