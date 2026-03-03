
"""
CodeLens AI - 优化器测试
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch, MagicMock
from src.optimizer import AIOptimizer
from src.config import Config

class TestAIOptimizer(unittest.TestCase):
    """测试 AIOptimizer 类"""
    
    def setUp(self):
        """在每个测试方法前创建优化器实例"""
        self.config = Config()
        self.optimizer = AIOptimizer(self.config)
    
    @patch('src.optimizer.AIOptimizer._optimize_with_openai')
    def test_optimize_python_file(self, mock_openai):
        """测试优化 Python 文件"""
        # 设置模拟返回值
        mock_openai.return_value = [
            {
                "issue": "使用 print 语句进行调试",
                "suggestion": "import logging\nlogging.info('Debug message')",
                "reason": "使用 logging 模块代替 print 语句，便于控制日志级别",
                "category": "readability"
            }
        ]
        
        analysis_results = [
            {
                "file_path": "/tmp/test.py",
                "language": "python",
                "issues": ["使用 print 语句进行调试"],
                "metrics": {"lines": 10, "complexity": 1, "functions": 1}
            }
        ]
        
        optimization_results = self.optimizer.optimize(analysis_results)
        
        # 验证返回的结果
        self.assertEqual(1, len(optimization_results))
        self.assertEqual("/tmp/test.py", optimization_results[0]["file_path"])
        self.assertEqual("python", optimization_results[0]["language"])
        self.assertEqual(1, len(optimization_results[0]["suggestions"]))
        
        suggestion = optimization_results[0]["suggestions"][0]
        self.assertEqual("使用 print 语句进行调试", suggestion["issue"])
        self.assertIn("logging", suggestion["suggestion"])
        self.assertIn("print", suggestion["reason"])
    
    @patch('src.optimizer.AIOptimizer._optimize_with_gemini')
    def test_optimize_js_file(self, mock_gemini):
        """测试优化 JavaScript 文件"""
        mock_gemini.return_value = [
            {
                "issue": "使用 console.log 进行调试",
                "suggestion": "import logger from 'logger';\nlogger.debug('Debug message');",
                "reason": "使用专业的日志库代替 console.log",
                "category": "maintainability"
            }
        ]
        
        analysis_results = [
            {
                "file_path": "/tmp/test.js",
                "language": "javascript",
                "issues": ["使用 console.log 进行调试"],
                "metrics": {"lines": 10, "complexity": 1, "functions": 1}
            }
        ]
        
        optimization_results = self.optimizer.optimize(analysis_results)
        
        self.assertEqual(1, len(optimization_results))
        self.assertEqual("/tmp/test.js", optimization_results[0]["file_path"])
        self.assertEqual("javascript", optimization_results[0]["language"])
        
        suggestion = optimization_results[0]["suggestions"][0]
        self.assertEqual("使用 console.log 进行调试", suggestion["issue"])
        self.assertIn("logger", suggestion["suggestion"])
    
    def test_validate_suggestions(self):
        """测试验证优化建议"""
        # 无效的建议（缺少 issue 和 suggestion）
        invalid_suggestions = [
            {"reason": "缺少问题描述"},
            {"issue": "缺少建议内容"}
        ]
        
        validated = self.optimizer._validate_suggestions(invalid_suggestions, "python")
        self.assertEqual(0, len(validated))
        
        # 有效的建议
        valid_suggestions = [
            {
                "issue": "问题描述",
                "suggestion": "优化后的代码",
                "reason": "优化原因",
                "category": "readability"
            }
        ]
        
        validated = self.optimizer._validate_suggestions(valid_suggestions, "python")
        self.assertEqual(1, len(validated))
        
        # 检查补充的默认字段
        self.assertIn("category", validated[0])
        self.assertIn("reason", validated[0])
    
    def test_apply_suggestion(self):
        """测试应用优化建议"""
        import tempfile
        import os
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write("print('test')")
            temp_file = f.name
        
        try:
            # 创建优化建议
            suggestion = {
                "issue": "使用 print 语句",
                "suggestion": "import logging\nlogging.info('test')",
                "reason": "使用 logging 模块",
                "category": "readability"
            }
            
            result = self.optimizer.apply_suggestion(temp_file, suggestion)
            self.assertTrue(result)
            
            # 验证文件内容已更改
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("logging", content)
                self.assertNotIn("print", content)
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_build_prompt(self):
        """测试构建优化提示词"""
        code = "print('test')"
        language = "python"
        issues = ["使用 print 语句"]
        
        prompt = self.optimizer._build_prompt(code, language, issues)
        
        self.assertIn(code, prompt)
        self.assertIn(language, prompt)
        self.assertIn("print", prompt)

if __name__ == "__main__":
    unittest.main()
