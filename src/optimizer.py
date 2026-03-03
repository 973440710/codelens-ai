
"""
CodeLens AI - AI优化器模块
负责与AI模型交互，生成代码优化建议
"""

import os
import sys
import openai
import google.generativeai as genai
from typing import List, Dict, Any
from rich.console import Console

from src.config import Config

console = Console()

class AIOptimizer:
    def __init__(self, config: Config):
        self.config = config
        self._setup_api()
    
    def _setup_api(self):
        """设置AI API"""
        try:
            if self.config.model == "openai":
                openai.api_key = self.config.get_api_key()
            elif self.config.model == "gemini":
                genai.configure(api_key=self.config.get_api_key())
        except Exception as e:
            console.print(f"[bold red]❌ API配置错误: {e}[/bold red]")
            sys.exit(1)
    
    def optimize(self, analysis_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        对分析结果进行优化
        
        Args:
            analysis_results: 分析结果列表
            
        Returns:
            优化结果列表
        """
        optimization_results = []
        
        for analysis in analysis_results:
            result = self._optimize_single_file(analysis)
            optimization_results.append(result)
            
        return optimization_results
    
    def _optimize_single_file(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        优化单个文件
        
        Args:
            analysis: 分析结果
            
        Returns:
            优化结果
        """
        file_path = analysis.get("file_path")
        code = analysis.get("code")
        language = analysis.get("language")
        issues = analysis.get("issues", [])
        
        # 生成优化提示
        prompt = self._generate_optimization_prompt(language, code, issues)
        
        # 调用AI模型
        try:
            if self.config.model == "openai":
                optimized_code = self._call_openai(prompt)
            elif self.config.model == "gemini":
                optimized_code = self._call_gemini(prompt)
            else:
                raise ValueError("不支持的AI模型")
        except Exception as e:
            console.print(f"[bold red]❌ 优化失败: {file_path} - {e}[/bold red]")
            return {
                "file_path": file_path,
                "language": language,
                "original_code": code,
                "suggestion": None,
                "reason": f"AI调用失败: {e}"
            }
        
        # 解析优化结果
        return {
            "file_path": file_path,
            "language": language,
            "original_code": code,
            "suggestion": optimized_code,
            "reason": "AI优化建议"
        }
    
    def _generate_optimization_prompt(self, language: str, code: str, issues: List[Dict[str, Any]]) -> str:
        """
        生成优化提示
        
        Args:
            language: 代码语言
            code: 原始代码
            issues: 识别出的问题
            
        Returns:
            优化提示字符串
        """
        issue_list = "\n".join([f"- {issue.get('type')}: {issue.get('description')}" for issue in issues])
        
        prompt = f"""
你是一个专业的代码优化专家。请帮我优化以下{language}代码：

## 原始代码
```{language}
{code}
```

## 识别到的问题
{issue_list if issues else "未识别到具体问题，但请检查代码质量"}

## 优化要求
1. 修复识别到的问题
2. 提高代码的可读性和可维护性
3. 优化代码结构和逻辑
4. 保持功能不变
5. 遵循最佳实践
6. 使用{language}的标准风格

## 输出格式
只输出优化后的代码，不要包含任何其他文本。
"""
        
        return prompt
    
    def _call_openai(self, prompt: str) -> str:
        """
        调用 OpenAI API
        
        Args:
            prompt: 提示词
            
        Returns:
            优化后的代码
        """
        try:
            client = openai.OpenAI(api_key=self.config.get_api_key())
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的代码优化专家，只返回优化后的代码"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"OpenAI API调用失败: {e}")
    
    def _call_gemini(self, prompt: str) -> str:
        """
        调用 Google Gemini API
        
        Args:
            prompt: 提示词
            
        Returns:
            优化后的代码
        """
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.config.temperature,
                    max_output_tokens=self.config.max_tokens
                )
            )
            
            return response.text.strip()
            
        except Exception as e:
            raise Exception(f"Google Gemini API调用失败: {e}")
