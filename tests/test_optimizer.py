
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
        # 避免在测试中调用实际的API
        self.config.set_model("openai")
        self.config.openai_api_key = "test_key"
        # 使用 mock 避免调用实际的API
        with patch.object(self.config, 'validate_config', return_value=None), \
             patch.object(self.config, 'get_api_key', return_value="test_key"):
            self.optimizer = AIOptimizer(self.config)

    @patch('src.optimizer.AIOptimizer._call_openai')
    def test_optimize_python_file(self, mock_openai):
        """测试优化 Python 文件"""
        # 设置模拟返回值
        mock_openai.return_value = "import logging\nlogging.info('Debug message')"

        analysis_results = [
            {
                "file_path": "/tmp/test.py",
                "language": "python",
                "code": "print('Debug message')",
                "issues": [
                    {
                        "type": "style",
                        "description": "使用 print 语句进行调试"
                    }
                ]
            }
        ]

        optimization_results = self.optimizer.optimize(analysis_results)

        # 验证返回的结果
        self.assertEqual(1, len(optimization_results))
        self.assertEqual("/tmp/test.py", optimization_results[0]["file_path"])
        self.assertEqual("python", optimization_results[0]["language"])
        self.assertIn("logging", optimization_results[0]["suggestion"])
        self.assertIn("Debug message", optimization_results[0]["suggestion"])

    @patch('src.optimizer.AIOptimizer._call_openai')
    def test_optimize_js_file(self, mock_openai):
        """测试优化 JavaScript 文件"""
        # 设置模拟返回值
        mock_openai.return_value = "import logger from 'logger';\nlogger.debug('Debug message');"
    
        analysis_results = [
            {
                "file_path": "/tmp/test.js",
                "language": "javascript",
                "code": "console.log('Debug message');",
                "issues": [
                    {
                        "type": "style",
                        "description": "使用 console.log 进行调试"
                    }
                ]
            }
        ]
    
        optimization_results = self.optimizer.optimize(analysis_results)
    
        self.assertEqual(1, len(optimization_results))
        self.assertEqual("/tmp/test.js", optimization_results[0]["file_path"])
        self.assertEqual("javascript", optimization_results[0]["language"])
        self.assertIn("logger", optimization_results[0]["suggestion"])

    def test_generate_optimization_prompt(self):
        """测试生成优化提示词"""
        code = "print('test')"
        language = "python"
        issues = [
            {
                "type": "style",
                "description": "使用 print 语句"
            }
        ]

        # 直接调用 _generate_optimization_prompt 方法
        prompt = self.optimizer._generate_optimization_prompt(language, code, issues)

        self.assertIn(code, prompt)
        self.assertIn(language, prompt)
        self.assertIn("print", prompt)

if __name__ == "__main__":
    unittest.main()
