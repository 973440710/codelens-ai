
#!/usr/bin/env python3
"""
CodeLens AI - AI驱动的代码优化工具
CLI 入口文件
"""

import click
import os
import sys
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.analyzer import CodeAnalyzer
from src.optimizer import AIOptimizer
from src.reporter import ReportGenerator
from src.config import Config

console = Console()

@click.group()
@click.version_option("1.0.0", prog_name="CodeLens AI")
def main():
    """
    CodeLens AI - AI驱动的代码优化工具
    自动分析代码质量，提供智能优化建议
    """
    pass

@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--language", "-l", help="指定代码语言（python/javascript/typescript）")
@click.option("--model", "-m", default="openai", help="使用的AI模型（openai/gemini）")
@click.option("--auto-fix", "-a", is_flag=True, help="自动应用优化建议")
@click.option("--report", "-r", help="生成HTML报告的路径")
def analyze(path, language, model, auto_fix, report):
    """
    分析指定路径的代码文件
    """
    try:
        console.print("[bold green]🚀 启动 CodeLens AI 代码分析器[/bold green]")
        
        # 加载配置
        config = Config()
        config.set_model(model)
        
        # 初始化分析器
        analyzer = CodeAnalyzer()
        
        # 扫描代码文件
        with Progress() as progress:
            task = progress.add_task("[cyan]扫描代码文件...", total=100)
            files = analyzer.scan_directory(path, language)
            progress.update(task, advance=30)
            
            # 分析代码
            progress.update(task, description="[cyan]分析代码质量...")
            analysis_results = []
            for file_path in files:
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
                analysis = analyzer.analyze_file(file_path, code)
                analysis_results.append(analysis)
            progress.update(task, advance=60)
            
            # 生成优化建议
            optimizer = AIOptimizer(config)
            progress.update(task, description="[cyan]生成AI优化建议...")
            optimization_results = optimizer.optimize(analysis_results)
            progress.update(task, advance=10)
        
        # 显示结果
        display_results(analysis_results, optimization_results)
        
        # 自动修复
        if auto_fix:
            console.print("\n[bold yellow]🔧 自动应用优化建议...[/bold yellow]")
            for result in optimization_results:
                if result.get("suggestion"):
                    file_path = result.get("file_path")
                    optimized_code = result.get("suggestion")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(optimized_code)
                    console.print(f"✅ 已优化: {file_path}")
        
        # 生成报告
        if report:
            console.print(f"\n📊 生成报告: {report}")
            report_generator = ReportGenerator()
            report_generator.generate_html_report(analysis_results, optimization_results, report)
        
        console.print("\n[bold green]🎉 代码分析完成！[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]❌ 错误: {str(e)}[/bold red]")
        sys.exit(1)

@main.command()
def config():
    """
    配置工具参数
    """
    console.print("[bold yellow]⚙️  配置工具参数[/bold yellow]")
    config = Config()
    
    # 获取API密钥
    openai_key = click.prompt("请输入 OpenAI API 密钥", hide_input=True)
    gemini_key = click.prompt("请输入 Google Gemini API 密钥", hide_input=True)
    
    config.set_api_keys(openai_key=openai_key, gemini_key=gemini_key)
    console.print("[bold green]✅ 配置已保存！[/bold green]")

def display_results(analysis_results, optimization_results):
    """
    显示分析结果
    """
    # 统计信息
    total_files = len(analysis_results)
    total_issues = sum(len(analysis.get("issues", [])) for analysis in analysis_results)
    total_suggestions = sum(len(result.get("suggestions", [])) for result in optimization_results)
    
    console.print(f"\n📈 [bold blue]统计信息[/bold blue]:")
    console.print(f"   总文件数: {total_files}")
    console.print(f"   代码质量问题: {total_issues}")
    console.print(f"   优化建议数: {total_suggestions}")
    
    # 详细结果
    if optimization_results:
        console.print("\n📋 [bold blue]优化建议[/bold blue]:")
        for result in optimization_results:
            file_path = result.get("file_path")
            suggestions = result.get("suggestions", [])
            
            if suggestions:
                console.print(f"\n[bold cyan]{file_path}[/bold cyan]:")
                for i, suggestion in enumerate(suggestions, 1):
                    console.print(f"  {i}. [yellow]{suggestion['issue']}[/yellow]")
                    console.print(f"     建议: [green]{suggestion['suggestion']}[/green]")
                    if suggestion.get("reason"):
                        console.print(f"     原因: [blue]{suggestion['reason']}[/blue]")

if __name__ == "__main__":
    main()
