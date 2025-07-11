"""
Code parsing utilities for different programming languages
"""

import ast
import re
from typing import List, Optional, Dict, Any
from .models import CodeBlock, Language


class CodeParser:
    """Parser for different programming languages"""
    
    def __init__(self):
        self.language_parsers = {
            Language.PYTHON: self._parse_python,
            Language.JAVASCRIPT: self._parse_javascript,
            Language.TYPESCRIPT: self._parse_typescript,
            Language.CPP: self._parse_cpp,
            Language.JAVA: self._parse_java,
            Language.GO: self._parse_go,
            Language.RUST: self._parse_rust,
        }
    
    def parse_code(self, code: str, language: Language) -> List[CodeBlock]:
        """Parse code based on language"""
        parser = self.language_parsers.get(language)
        if parser:
            return parser(code)
        else:
            # Fallback to treating entire code as one block
            return [CodeBlock(
                name="main",
                type="module",
                code=code,
                line_start=1,
                line_end=len(code.split('\n')),
                language=language,
                lines_of_code=len(code.split('\n'))
            )]
    
    def _parse_python(self, code: str) -> List[CodeBlock]:
        """Parse Python code into functions and classes"""
        try:
            tree = ast.parse(code)
            blocks = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self._calculate_python_complexity(node)
                    blocks.append(CodeBlock(
                        name=node.name,
                        type="function",
                        code=ast.unparse(node),
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        language=Language.PYTHON,
                        complexity_score=complexity,
                        lines_of_code=node.end_lineno - node.lineno + 1 if node.end_lineno else 1
                    ))
                elif isinstance(node, ast.ClassDef):
                    complexity = self._calculate_python_complexity(node)
                    blocks.append(CodeBlock(
                        name=node.name,
                        type="class",
                        code=ast.unparse(node),
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        language=Language.PYTHON,
                        complexity_score=complexity,
                        lines_of_code=node.end_lineno - node.lineno + 1 if node.end_lineno else 1
                    ))
            
            return blocks
        except SyntaxError:
            return []
    
    def _calculate_python_complexity(self, node) -> float:
        """Calculate cyclomatic complexity for Python AST node"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _parse_javascript(self, code: str) -> List[CodeBlock]:
        """Parse JavaScript code into functions and classes"""
        blocks = []
        lines = code.split('\n')
        
        # Function patterns
        function_patterns = [
            r'function\s+(\w+)\s*\([^)]*\)\s*{',  # function name() {}
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',  # const name = () => {}
            r'let\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',  # let name = () => {}
            r'var\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*{',  # var name = () => {}
            r'(\w+)\s*:\s*function\s*\([^)]*\)\s*{',  # name: function() {}
        ]
        
        # Class patterns
        class_patterns = [
            r'class\s+(\w+)',  # class Name
        ]
        
        for i, line in enumerate(lines, 1):
            # Check for functions
            for pattern in function_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1)
                    block_code, end_line = self._extract_block(lines, i)
                    complexity = self._calculate_js_complexity(block_code)
                    blocks.append(CodeBlock(
                        name=name,
                        type="function",
                        code=block_code,
                        line_start=i,
                        line_end=end_line,
                        language=Language.JAVASCRIPT,
                        complexity_score=complexity,
                        lines_of_code=end_line - i + 1
                    ))
                    break
            
            # Check for classes
            for pattern in class_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1)
                    block_code, end_line = self._extract_block(lines, i)
                    complexity = self._calculate_js_complexity(block_code)
                    blocks.append(CodeBlock(
                        name=name,
                        type="class",
                        code=block_code,
                        line_start=i,
                        line_end=end_line,
                        language=Language.JAVASCRIPT,
                        complexity_score=complexity,
                        lines_of_code=end_line - i + 1
                    ))
                    break
        
        return blocks
    
    def _parse_typescript(self, code: str) -> List[CodeBlock]:
        """Parse TypeScript code (similar to JavaScript but with type annotations)"""
        # For now, use JavaScript parser as TypeScript is a superset
        blocks = self._parse_javascript(code)
        # Update language for all blocks
        for block in blocks:
            block.language = Language.TYPESCRIPT
        return blocks
    
    def _parse_cpp(self, code: str) -> List[CodeBlock]:
        """Parse C++ code into functions and classes"""
        blocks = []
        lines = code.split('\n')
        
        # Function patterns
        function_patterns = [
            r'(\w+(?:::\w+)*)\s+(\w+)\s*\([^)]*\)\s*{',  # return_type function_name()
            r'(\w+)\s+(\w+)\s*\([^)]*\)\s*{',  # type name()
        ]
        
        # Class patterns
        class_patterns = [
            r'class\s+(\w+)',  # class Name
            r'struct\s+(\w+)',  # struct Name
        ]
        
        for i, line in enumerate(lines, 1):
            # Check for functions
            for pattern in function_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(2) if len(match.groups()) > 1 else match.group(1)
                    block_code, end_line = self._extract_block(lines, i)
                    complexity = self._calculate_cpp_complexity(block_code)
                    blocks.append(CodeBlock(
                        name=name,
                        type="function",
                        code=block_code,
                        line_start=i,
                        line_end=end_line,
                        language=Language.CPP,
                        complexity_score=complexity,
                        lines_of_code=end_line - i + 1
                    ))
                    break
            
            # Check for classes/structs
            for pattern in class_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1)
                    block_code, end_line = self._extract_block(lines, i)
                    complexity = self._calculate_cpp_complexity(block_code)
                    blocks.append(CodeBlock(
                        name=name,
                        type="class",
                        code=block_code,
                        line_start=i,
                        line_end=end_line,
                        language=Language.CPP,
                        complexity_score=complexity,
                        lines_of_code=end_line - i + 1
                    ))
                    break
        
        return blocks
    
    def _parse_java(self, code: str) -> List[CodeBlock]:
        """Parse Java code into methods and classes"""
        blocks = []
        lines = code.split('\n')
        
        # Method patterns
        method_patterns = [
            r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:\w+(?:<[^>]+>)?)\s+(\w+)\s*\([^)]*\)\s*{',  # Java methods
        ]
        
        # Class patterns
        class_patterns = [
            r'(?:public\s+)?(?:abstract\s+)?(?:final\s+)?class\s+(\w+)',  # class Name
            r'(?:public\s+)?interface\s+(\w+)',  # interface Name
        ]
        
        for i, line in enumerate(lines, 1):
            # Check for methods
            for pattern in method_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1)
                    block_code, end_line = self._extract_block(lines, i)
                    complexity = self._calculate_java_complexity(block_code)
                    blocks.append(CodeBlock(
                        name=name,
                        type="method",
                        code=block_code,
                        line_start=i,
                        line_end=end_line,
                        language=Language.JAVA,
                        complexity_score=complexity,
                        lines_of_code=end_line - i + 1
                    ))
                    break
            
            # Check for classes/interfaces
            for pattern in class_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1)
                    block_code, end_line = self._extract_block(lines, i)
                    complexity = self._calculate_java_complexity(block_code)
                    blocks.append(CodeBlock(
                        name=name,
                        type="class",
                        code=block_code,
                        line_start=i,
                        line_end=end_line,
                        language=Language.JAVA,
                        complexity_score=complexity,
                        lines_of_code=end_line - i + 1
                    ))
                    break
        
        return blocks
    
    def _parse_go(self, code: str) -> List[CodeBlock]:
        """Parse Go code into functions and structs"""
        blocks = []
        lines = code.split('\n')
        
        # Function patterns
        function_patterns = [
            r'func\s+(\w+)\s*\([^)]*\)\s*{',  # func name()
            r'func\s*\([^)]*\)\s*(\w+)\s*\([^)]*\)\s*{',  # func (receiver) name()
        ]
        
        # Struct patterns
        struct_patterns = [
            r'type\s+(\w+)\s+struct\s*{',  # type Name struct
        ]
        
        for i, line in enumerate(lines, 1):
            # Check for functions
            for pattern in function_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1)
                    block_code, end_line = self._extract_block(lines, i)
                    complexity = self._calculate_go_complexity(block_code)
                    blocks.append(CodeBlock(
                        name=name,
                        type="function",
                        code=block_code,
                        line_start=i,
                        line_end=end_line,
                        language=Language.GO,
                        complexity_score=complexity,
                        lines_of_code=end_line - i + 1
                    ))
                    break
            
            # Check for structs
            for pattern in struct_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1)
                    block_code, end_line = self._extract_block(lines, i)
                    complexity = self._calculate_go_complexity(block_code)
                    blocks.append(CodeBlock(
                        name=name,
                        type="struct",
                        code=block_code,
                        line_start=i,
                        line_end=end_line,
                        language=Language.GO,
                        complexity_score=complexity,
                        lines_of_code=end_line - i + 1
                    ))
                    break
        
        return blocks
    
    def _parse_rust(self, code: str) -> List[CodeBlock]:
        """Parse Rust code into functions and structs"""
        blocks = []
        lines = code.split('\n')
        
        # Function patterns
        function_patterns = [
            r'fn\s+(\w+)\s*\([^)]*\)\s*{',  # fn name()
        ]
        
        # Struct patterns
        struct_patterns = [
            r'struct\s+(\w+)',  # struct Name
            r'impl\s+(\w+)',  # impl Name
        ]
        
        for i, line in enumerate(lines, 1):
            # Check for functions
            for pattern in function_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1)
                    block_code, end_line = self._extract_block(lines, i)
                    complexity = self._calculate_rust_complexity(block_code)
                    blocks.append(CodeBlock(
                        name=name,
                        type="function",
                        code=block_code,
                        line_start=i,
                        line_end=end_line,
                        language=Language.RUST,
                        complexity_score=complexity,
                        lines_of_code=end_line - i + 1
                    ))
                    break
            
            # Check for structs/impls
            for pattern in struct_patterns:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1)
                    block_code, end_line = self._extract_block(lines, i)
                    complexity = self._calculate_rust_complexity(block_code)
                    blocks.append(CodeBlock(
                        name=name,
                        type="struct" if "struct" in line else "impl",
                        code=block_code,
                        line_start=i,
                        line_end=end_line,
                        language=Language.RUST,
                        complexity_score=complexity,
                        lines_of_code=end_line - i + 1
                    ))
                    break
        
        return blocks
    
    def _extract_block(self, lines: List[str], start_line: int) -> tuple[str, int]:
        """Extract a code block from start_line to its closing brace"""
        code_lines = []
        brace_count = 0
        started = False
        
        for i, line in enumerate(lines[start_line - 1:], start_line):
            if '{' in line:
                started = True
                brace_count += line.count('{')
            
            if started:
                code_lines.append(line)
            
            if '}' in line:
                brace_count -= line.count('}')
                if brace_count <= 0:
                    return '\n'.join(code_lines), i
        
        # If we can't find proper closing, return what we have
        return '\n'.join(code_lines), start_line + len(code_lines) - 1
    
    def _calculate_js_complexity(self, code: str) -> float:
        """Calculate cyclomatic complexity for JavaScript code"""
        complexity = 1
        complexity_patterns = [
            r'\bif\b', r'\belse\b', r'\bwhile\b', r'\bfor\b', 
            r'\bcase\b', r'\bcatch\b', r'\&\&', r'\|\|'
        ]
        
        for pattern in complexity_patterns:
            complexity += len(re.findall(pattern, code))
        
        return complexity
    
    def _calculate_cpp_complexity(self, code: str) -> float:
        """Calculate cyclomatic complexity for C++ code"""
        complexity = 1
        complexity_patterns = [
            r'\bif\b', r'\belse\b', r'\bwhile\b', r'\bfor\b', 
            r'\bcase\b', r'\bcatch\b', r'\&\&', r'\|\|'
        ]
        
        for pattern in complexity_patterns:
            complexity += len(re.findall(pattern, code))
        
        return complexity
    
    def _calculate_java_complexity(self, code: str) -> float:
        """Calculate cyclomatic complexity for Java code"""
        complexity = 1
        complexity_patterns = [
            r'\bif\b', r'\belse\b', r'\bwhile\b', r'\bfor\b', 
            r'\bcase\b', r'\bcatch\b', r'\&\&', r'\|\|'
        ]
        
        for pattern in complexity_patterns:
            complexity += len(re.findall(pattern, code))
        
        return complexity
    
    def _calculate_go_complexity(self, code: str) -> float:
        """Calculate cyclomatic complexity for Go code"""
        complexity = 1
        complexity_patterns = [
            r'\bif\b', r'\belse\b', r'\bfor\b', r'\bcase\b', 
            r'\&\&', r'\|\|'
        ]
        
        for pattern in complexity_patterns:
            complexity += len(re.findall(pattern, code))
        
        return complexity
    
    def _calculate_rust_complexity(self, code: str) -> float:
        """Calculate cyclomatic complexity for Rust code"""
        complexity = 1
        complexity_patterns = [
            r'\bif\b', r'\belse\b', r'\bwhile\b', r'\bfor\b', 
            r'\bmatch\b', r'\&\&', r'\|\|'
        ]
        
        for pattern in complexity_patterns:
            complexity += len(re.findall(pattern, code))
        
        return complexity 