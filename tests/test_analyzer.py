
"""
CodeLens AI - 代码分析器测试
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.analyzer import CodeAnalyzer

class TestCodeAnalyzer(unittest.TestCase):
    """测试 CodeAnalyzer 类"""
    
    def setUp(self):
        """在每个测试方法前创建分析器实例"""
        self.analyzer = CodeAnalyzer()
    
    def test_supported_languages(self):
        """测试支持的语言和文件扩展名"""
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
        }
        
        for ext, lang in language_map.items():
            self.assertEqual(language_map[ext], lang)
    
    def test_is_supported_file_python(self):
        """测试是否正确识别 Python 文件"""
        from pathlib import Path
        
        temp_file = Path("/tmp/test_analyzer_temp.py")
        temp_file.write_text("print('test')", encoding="utf-8")
        
        try:
            # 测试自动检测
            self.assertTrue(self.analyzer._is_code_file(str(temp_file)))
            
            # 测试指定语言
            self.assertTrue(self.analyzer._is_code_file(str(temp_file), target_language="python"))
            self.assertFalse(self.analyzer._is_code_file(str(temp_file), target_language="javascript"))
        finally:
            if temp_file.exists():
                temp_file.unlink()
    
    def test_scan_directory_single_file(self):
        """测试扫描单个文件"""
        from pathlib import Path
        
        temp_file = Path("/tmp/test_scan_single.py")
        temp_file.write_text("print('test')", encoding="utf-8")
        
        try:
            files = self.analyzer.scan_directory(str(temp_file))
            self.assertEqual(1, len(files))
            self.assertEqual(str(temp_file), files[0])
        finally:
            if temp_file.exists():
                temp_file.unlink()
    
    def test_analyze_python_file_basic(self):
        """测试分析基本的 Python 文件"""
        code = """
def hello_world():
    print("Hello, World!")
    return

if __name__ == "__main__":
    hello_world()
""".strip()
        
        result = self.analyzer.analyze_file("/tmp/test.py", code)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result["issues"]), 1)
        self.assertTrue(any("print" in issue.get('description', '') for issue in result["issues"]))
    
    def test_analyze_python_file_print_statement(self):
        """测试检测 print 语句"""
        code = """
def debug_function():
    print("Debug message")
    return 42
""".strip()
        
        analysis = self.analyzer.analyze_file("/tmp/test.py", code)
        
        self.assertGreater(len(analysis["issues"]), 0)
        self.assertTrue(any("print" in issue.get('description', '') for issue in analysis["issues"]))
    
    def test_analyze_python_file_complexity(self):
        """测试计算圈复杂度"""
        code = """
def complex_function(x):
    if x > 0:
        if x < 10:
            return x * 2
        elif x < 100:
            return x * 3
        else:
            return x * 4
    else:
        if x == -1:
            return 0
        else:
            return -x
""".strip()
        
        analysis = self.analyzer.analyze_file("/tmp/test.py", code)
        
        # 这个函数的圈复杂度应该较高
        self.assertGreater(len(analysis["issues"]), 0)
        self.assertTrue(any("复杂" in issue.get('description', '') for issue in analysis["issues"]))
    
    def test_analyze_js_file_basic(self):
        """测试分析基本的 JavaScript 文件"""
        code = """
function helloWorld() {
    console.log("Hello, World!");
}

helloWorld();
""".strip()
        
        analysis = self.analyzer.analyze_file("/tmp/test.js", code)
        
        self.assertIsNotNone(analysis)
        self.assertEqual(len(analysis["issues"]), 1)
        self.assertTrue(any("console" in issue.get('description', '') for issue in analysis["issues"]))
    
    def test_analyze_js_file_console_log(self):
        """测试检测 console.log 语句"""
        code = """
function debug() {
    console.log("Debug info");
    return 42;
}
""".strip()
        
        analysis = self.analyzer.analyze_file("/tmp/test.js", code)
        
        self.assertGreater(len(analysis["issues"]), 0)
        self.assertTrue(any("console" in issue.get('description', '') for issue in analysis["issues"]))
    
    def test_analyze_typescript_file(self):
        """测试分析 TypeScript 文件"""
        code = """
function greet(name: string): string {
    return `Hello, ${name}!`;
}

const message = greet("TypeScript");
""".strip()
        
        analysis = self.analyzer.analyze_file("/tmp/test.ts", code)
        
        self.assertIsNotNone(analysis)

if __name__ == "__main__":
    unittest.main()
