
"""
CodeLens AI - 报告生成器模块
负责生成代码质量分析报告
"""

import os
import sys
import json
from typing import List, Dict, Any
from datetime import datetime
import webbrowser
from rich.console import Console

console = Console()

class ReportGenerator:
    def __init__(self):
        self.report_dir = "reports"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
    
    def generate_html_report(self, analysis_results: List[Dict[str, Any]], optimization_results: List[Dict[str, Any]], output_path: str = None) -> str:
        """
        生成HTML报告
        
        Args:
            analysis_results: 分析结果
            optimization_results: 优化结果
            output_path: 输出路径（可选）
            
        Returns:
            报告文件路径
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(self.report_dir, f"codelens_report_{timestamp}.html")
        
        try:
            html_content = self._generate_html_content(analysis_results, optimization_results)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            console.print(f"[bold green]✅ 报告已生成: {output_path}[/bold green]")
            return output_path
            
        except Exception as e:
            console.print(f"[bold red]❌ 报告生成失败: {e}[/bold red]")
            return None
    
    def _generate_html_content(self, analysis_results: List[Dict[str, Any]], optimization_results: List[Dict[str, Any]]) -> str:
        """
        生成HTML内容
        
        Args:
            analysis_results: 分析结果
            optimization_results: 优化结果
            
        Returns:
            HTML内容
        """
        # 统计信息
        total_files = len(analysis_results)
        total_issues = sum(len(result.get("issues", [])) for result in analysis_results)
        total_suggestions = len(optimization_results)
        
        # 文件分析详情
        file_details = []
        for analysis, optimization in zip(analysis_results, optimization_results):
            file_details.append({
                "file_path": analysis.get("file_path"),
                "language": analysis.get("language"),
                "issues": analysis.get("issues", []),
                "optimization": optimization
            })
        
        return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeLens AI 报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f7fa;
            color: #333;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #4A90E2;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .stat-card h3 {{
            color: #4A90E2;
            margin-bottom: 10px;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
        .file-details {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }}
        .file-header {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
            border-left: 4px solid #4A90E2;
        }}
        .file-path {{
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 5px;
        }}
        .file-language {{
            color: #666;
            font-size: 14px;
        }}
        .issues {{
            margin-bottom: 15px;
        }}
        .issue {{
            background-color: #fff3cd;
            padding: 10px;
            border-radius: 3px;
            margin-bottom: 5px;
            border-left: 4px solid #ffc107;
        }}
        .issue-type {{
            font-weight: bold;
            color: #856404;
        }}
        .issue-desc {{
            color: #856404;
            margin-left: 10px;
        }}
        .code-section {{
            margin-bottom: 15px;
        }}
        .code-header {{
            font-weight: bold;
            margin-bottom: 10px;
            color: #4A90E2;
        }}
        .code {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: monospace;
            font-size: 14px;
        }}
        .optimization {{
            background-color: #d4edda;
            padding: 10px;
            border-radius: 3px;
            margin-bottom: 5px;
            border-left: 4px solid #28a745;
        }}
        .optimization-header {{
            font-weight: bold;
            color: #155724;
        }}
        .optimization-desc {{
            color: #155724;
            margin-left: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CodeLens AI 代码优化报告</h1>
            <p>生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>分析文件数</h3>
                <div class="stat-value">{total_files}</div>
            </div>
            <div class="stat-card">
                <h3>代码问题数</h3>
                <div class="stat-value">{total_issues}</div>
            </div>
            <div class="stat-card">
                <h3>优化建议数</h3>
                <div class="stat-value">{total_suggestions}</div>
            </div>
        </div>
        
        <div class="file-details">
            <h2>文件分析详情</h2>
            {self._generate_file_details(file_details)}
        </div>
        
        <div class="footer">
            <p>CodeLens AI - AI驱动的代码优化工具</p>
        </div>
    </div>
</body>
</html>
""".strip()
    
    def _generate_file_details(self, file_details: List[Dict[str, Any]]) -> str:
        """
        生成文件分析详情
        
        Args:
            file_details: 文件分析详情
            
        Returns:
            HTML内容
        """
        details_html = ""
        
        for detail in file_details:
            file_path = detail.get("file_path")
            language = detail.get("language")
            issues = detail.get("issues", [])
            optimization = detail.get("optimization")
            
            details_html += f"""
            <div class="file-header">
                <div class="file-path">{file_path}</div>
                <div class="file-language">语言: {language}</div>
            </div>
            """
            
            if issues:
                details_html += '<div class="issues">'
                details_html += '<div class="code-header">识别到的问题:</div>'
                
                for issue in issues:
                    issue_type = issue.get("type", "unknown")
                    issue_desc = issue.get("description", "未知问题")
                    
                    details_html += f"""
                    <div class="issue">
                        <span class="issue-type">{issue_type}</span>
                        <span class="issue-desc">{issue_desc}</span>
                    </div>
                    """
                
                details_html += "</div>"
            
            if optimization:
                suggestion = optimization.get("suggestion")
                reason = optimization.get("reason")
                
                if suggestion:
                    details_html += f"""
                    <div class="code-section">
                        <div class="code-header">AI优化建议:</div>
                        <div class="code">{suggestion}</div>
                    </div>
                    """
                
                if reason:
                    details_html += f"""
                    <div class="optimization">
                        <span class="optimization-header">优化原因:</span>
                        <span class="optimization-desc">{reason}</span>
                    </div>
                    """
        
        return details_html
    
    def generate_text_report(self, analysis_results: List[Dict[str, Any]], optimization_results: List[Dict[str, Any]]) -> str:
        """
        生成文本报告
        
        Args:
            analysis_results: 分析结果
            optimization_results: 优化结果
            
        Returns:
            文本报告
        """
        report = []
        report.append("CodeLens AI 代码优化报告")
        report.append("=" * 50)
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append()
        
        total_files = len(analysis_results)
        total_issues = sum(len(result.get("issues", [])) for result in analysis_results)
        total_suggestions = len(optimization_results)
        
        report.append(f"分析文件数: {total_files}")
        report.append(f"代码问题数: {total_issues}")
        report.append(f"优化建议数: {total_suggestions}")
        report.append()
        report.append("文件分析详情:")
        report.append("-" * 30)
        
        for analysis, optimization in zip(analysis_results, optimization_results):
            file_path = analysis.get("file_path")
            language = analysis.get("language")
            issues = analysis.get("issues", [])
            suggestion = optimization.get("suggestion")
            
            report.append(f"文件: {file_path}")
            report.append(f"语言: {language}")
            
            if issues:
                report.append("问题:")
                for issue in issues:
                    report.append(f"  - {issue.get('type')}: {issue.get('description')}")
            
            if suggestion:
                report.append("优化建议:")
                report.append(suggestion)
                report.append()
        
        return "\n".join(report)
    
    def open_report(self, report_path: str):
        """
        打开报告
        
        Args:
            report_path: 报告路径
        """
        try:
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
        except Exception as e:
            console.print(f"[bold red]❌ 无法打开报告: {e}[/bold red]")
