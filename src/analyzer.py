
"""
CodeLens AI - 代码分析器模块
负责代码解析和基础问题识别
"""

import os
import ast
import sys
from typing import List, Dict, Any
import os
import sys
import ast

class CodeAnalyzer:
    def __init__(self):
        self.language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
        }
        
    def scan_directory(self, path: str, target_language: str = None) -> List[str]:
        """
        扫描指定目录，找出符合条件的代码文件
        
        Args:
            path: 要扫描的目录路径
            target_language: 目标语言（可选）
            
        Returns:
            符合条件的文件路径列表
        """
        code_files = []
        
        if os.path.isfile(path):
            if self._is_code_file(path, target_language):
                code_files.append(path)
            return code_files
            
        for root, _, files in os.walk(path):
            # 忽略特定目录
            if '__pycache__' in root or '.git' in root or '.venv' in root:
                continue
                
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if self._is_code_file(file_path, target_language):
                    code_files.append(file_path)
                    
        return code_files
    
    def _is_code_file(self, file_path: str, language: str = None) -> bool:
        """
        判断文件是否是代码文件
        
        Args:
            file_path: 文件路径
            language: 目标语言（可选）
            
        Returns:
            是否是代码文件
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if language:
            target_ext = '.' + language.lower()
            return file_ext == target_ext
            
        return file_ext in self.language_map
    
    def analyze_file(self, file_path: str, code: str) -> Dict[str, Any]:
        """
        分析单个文件的代码质量
        
        Args:
            file_path: 文件路径
            code: 代码内容
            
        Returns:
            分析结果
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        language = self.language_map.get(file_ext, 'unknown')
        
        analysis = {
            'file_path': file_path,
            'language': language,
            'code': code,
            'issues': []
        }
        
        if language == 'python':
            self._analyze_python(analysis)
        elif language in ['javascript', 'typescript']:
            self._analyze_javascript(analysis)
            
        return analysis
    
    def _analyze_python(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析 Python 代码
        
        Args:
            analysis: 分析结果字典
            
        Returns:
            更新后的分析结果
        """
        try:
            tree = ast.parse(analysis['code'])
            
            # 基础代码质量检查
            issues = self._check_python_code_quality(tree)
            
            analysis['issues'].extend(issues)
            
        except SyntaxError as e:
            analysis['issues'].append({
                'type': 'syntax',
                'description': f"语法错误: {str(e)}",
                'line': e.lineno,
                'column': e.offset
            })
            
        except Exception as e:
            analysis['issues'].append({
                'type': 'parse',
                'description': f"解析错误: {str(e)}",
                'line': 0,
                'column': 0
            })
            
        return analysis
    
    def _check_python_code_quality(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """
        检查 Python 代码质量
        
        Args:
            tree: 抽象语法树
            
        Returns:
            问题列表
        """
        issues = []
        
        for node in ast.walk(tree):
            # 检查 print 语句（Python 3.x 中 print 是函数）
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and \
               hasattr(node.value.func, 'id') and node.value.func.id == 'print':
                issues.append({
                    'type': 'style',
                    'description': "使用 print 语句进行调试",
                    'line': node.lineno,
                    'column': node.col_offset
                })
            
            # 检查重复代码模式
            if isinstance(node, ast.For):
                if isinstance(node.iter, ast.Call) and hasattr(node.iter.func, 'id') and node.iter.func.id == 'range':
                    if len(node.iter.args) == 1:
                        issues.append({
                            'type': 'style',
                            'description': "使用范围循环，可以考虑使用 enumerate() 提高可读性",
                            'line': node.lineno,
                            'column': node.col_offset
                        })
            
            # 检查复杂条件
            if isinstance(node, ast.If):
                if self._is_complex_condition(node.test):
                    issues.append({
                        'type': 'complexity',
                        'description': "条件过于复杂，考虑重构为多个条件或提取到函数中",
                        'line': node.lineno,
                        'column': node.col_offset
                    })
            
            # 检查变量命名
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                if len(node.id) < 3 or node.id.startswith('_'):
                    issues.append({
                        'type': 'naming',
                        'description': f"变量名 '{node.id}' 过于简短或不符合命名规范",
                        'line': node.lineno,
                        'column': node.col_offset
                    })
        
        return issues
    
    def _is_complex_condition(self, node: ast.AST) -> bool:
        """
        判断条件是否复杂
        
        Args:
            node: 条件节点
            
        Returns:
            是否复杂
        """
        if isinstance(node, ast.BoolOp):
            # 如果有多个逻辑运算符，认为是复杂条件
            if len(node.values) > 2:
                return True
        
        # 检查嵌套条件
        if isinstance(node, ast.IfExp) or isinstance(node, ast.BoolOp) or \
           (isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not)):
            return True
            
        # 检查包含多个操作符的条件
        if hasattr(node, 'left') and hasattr(node, 'ops'):
            if len(node.ops) > 1:
                return True
                
        return False
    
    def _analyze_javascript(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析 JavaScript/TypeScript 代码
        
        Args:
            analysis: 分析结果字典
            
        Returns:
            更新后的分析结果
        """
        # 简单的 JavaScript/TypeScript 代码分析实现
        # 实际项目中可以使用 Babel 解析器
        try:
            # 逐行扫描代码以检测问题并获取行号
            lines = analysis['code'].split('\n')
            
            for line_number, line in enumerate(lines, 1):
                line = line.strip()
                
                # 检查 eval() 函数
                if 'eval(' in line:
                    analysis['issues'].append({
                        'type': 'security',
                        'description': "使用 eval() 存在安全风险",
                        'line': line_number,
                        'column': line.find('eval(')
                    })
                
                # 检查 alert() 函数
                if 'alert(' in line:
                    analysis['issues'].append({
                        'type': 'style',
                        'description': "使用 alert() 进行调试，可以考虑使用 console.log()",
                        'line': line_number,
                        'column': line.find('alert(')
                    })
                
                # 检查 console.log 函数
                if 'console.log(' in line:
                    analysis['issues'].append({
                        'type': 'style',
                        'description': "使用 console.log 进行调试",
                        'line': line_number,
                        'column': line.find('console.log(')
                    })
                
        except Exception as e:
            analysis['issues'].append({
                'type': 'parse',
                'description': f"解析错误: {str(e)}",
                'line': 0,
                'column': 0
            })
            
        return analysis
