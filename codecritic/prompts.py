"""
Prompt templates for CodeCritic
"""

from .models import Language
from typing import Optional, Dict

class PromptTemplates:
    """A class to manage and generate prompt templates for CodeCritic."""

    def get_review_prompt(self, code: str, language: Language, modular: bool = False, block_name: Optional[str] = None) -> str:
        """Generate review prompt for the LLM"""
        
        language_guidance = self.get_language_specific_guidance(language)
        
        if modular and block_name:
            prompt = f"""You are CodeCritic, an expert code reviewer specializing in {language.value} development. Analyze the following {language.value} code block and provide comprehensive feedback.

Code Block: {block_name}
```{language.value}
{code}
```

{language_guidance}

Please analyze this code block and provide feedback in the following categories:

🐞 **Bug Detection**: Identify potential bugs, errors, or issues that could cause problems
💡 **Best Practices**: Suggest improvements based on {language.value} coding standards and conventions
⚡ **Performance**: Highlight opportunities for performance optimization
✅ **Style**: Provide style and formatting recommendations
🔒 **Security**: Identify potential security vulnerabilities and risks

Format your response as follows:
🐞 [BUG] - Description of the bug
- Specific issue details

💡 [BEST PRACTICE] - Description of best practice
- Specific recommendation

⚡ [PERFORMANCE] - Description of performance issue
- Specific optimization suggestion

✅ [STYLE] - Description of style issue
- Specific formatting recommendation

🔒 [SECURITY] - Description of security issue
- Specific security recommendation

Be specific, actionable, and constructive in your feedback. Include confidence levels and severity where appropriate."""
        else:
            prompt = f"""You are CodeCritic, an expert code reviewer specializing in {language.value} development. Analyze the following {language.value} code and provide comprehensive feedback.

```{language.value}
{code}
```

{language_guidance}

Please analyze this code and provide feedback in the following categories:

🐞 **Bug Detection**: Identify potential bugs, errors, or issues that could cause problems
💡 **Best Practices**: Suggest improvements based on {language.value} coding standards and conventions
⚡ **Performance**: Highlight opportunities for performance optimization
✅ **Style**: Provide style and formatting recommendations
🔒 **Security**: Identify potential security vulnerabilities and risks

Format your response as follows:
🐞 [BUG] - Description of the bug
- Specific issue details

💡 [BEST PRACTICE] - Description of best practice
- Specific recommendation

⚡ [PERFORMANCE] - Description of performance issue
- Specific optimization suggestion

✅ [STYLE] - Description of style issue
- Specific formatting recommendation

🔒 [SECURITY] - Description of security issue
- Specific security recommendation

Be specific, actionable, and constructive in your feedback. If no issues are found in a category, you can omit that section."""
        
        return prompt


    def get_language_specific_guidance(self, language: Language) -> str:
        """Get language-specific guidance for code review"""
        
        guidance_map = {
            Language.PYTHON: """
**Python-Specific Guidelines:**
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Consider using dataclasses for simple data structures
- Prefer list comprehensions over explicit loops when readable
- Use context managers for resource management
- Consider async/await for I/O operations
- Use f-strings for string formatting
- Follow the principle of least surprise
- Consider using mypy for static type checking
- Use virtual environments for dependency management""",

            Language.JAVASCRIPT: """
**JavaScript-Specific Guidelines:**
- Use const and let instead of var
- Prefer arrow functions for callbacks
- Use template literals for string interpolation
- Consider using TypeScript for type safety
- Use async/await instead of promises when possible
- Follow ESLint and Prettier configurations
- Use destructuring for cleaner code
- Consider using modern ES6+ features
- Use meaningful variable and function names
- Handle errors properly with try-catch""",

            Language.TYPESCRIPT: """
**TypeScript-Specific Guidelines:**
- Use strict type checking
- Define interfaces for object shapes
- Use enums for constants
- Prefer readonly properties when possible
- Use union types for flexible typing
- Consider using utility types
- Use generics for reusable components
- Follow naming conventions for types
- Use strict null checks
- Consider using branded types for type safety""",

            Language.CPP: """
**C++-Specific Guidelines:**
- Use RAII for resource management
- Prefer const correctness
- Use smart pointers over raw pointers
- Follow the Rule of Three/Five/Zero
- Use references when possible
- Consider using std::move for performance
- Use range-based for loops
- Prefer std::vector over C-style arrays
- Use nullptr instead of NULL
- Consider using auto for type deduction""",

            Language.JAVA: """
**Java-Specific Guidelines:**
- Use meaningful package names
- Follow Java naming conventions
- Use final for immutable variables
- Consider using Optional for nullable values
- Use try-with-resources for resource management
- Prefer interfaces over abstract classes
- Use StringBuilder for string concatenation
- Consider using streams for functional programming
- Use enums for constants
- Follow SOLID principles""",

            Language.GO: """
**Go-Specific Guidelines:**
- Follow Go naming conventions
- Use interfaces for abstraction
- Handle errors explicitly
- Use goroutines and channels appropriately
- Follow the Go formatting guidelines (gofmt)
- Use composition over inheritance
- Consider using context for cancellation
- Use defer for cleanup
- Prefer small, focused functions
- Use meaningful package names""",

            Language.RUST: """
**Rust-Specific Guidelines:**
- Follow Rust naming conventions
- Use ownership and borrowing effectively
- Handle errors with Result and Option
- Use match expressions for pattern matching
- Consider using iterators for performance
- Use traits for abstraction
- Follow the Rust formatting guidelines (rustfmt)
- Use meaningful variable names
- Consider using clippy for additional checks
- Use unsafe code sparingly and document why"""
        }
        
        return guidance_map.get(language, "")


    def get_security_prompt(self, code: str, language: Language) -> str:
        """Generate security-focused review prompt"""
        
        security_guidance = self.get_security_guidance(language)
        
        return f"""You are a security expert specializing in {language.value} code analysis. Analyze the following code for security vulnerabilities:

```{language.value}
{code}
```

{security_guidance}

Focus on identifying:
- Input validation issues
- Authentication and authorization problems
- Data exposure risks
- Injection vulnerabilities
- Cryptographic weaknesses
- Resource exhaustion risks
- Race conditions
- Memory safety issues (for applicable languages)

Provide specific, actionable security recommendations with severity levels."""


    def get_security_guidance(self, language: Language) -> str:
        """Get language-specific security guidance"""
        
        security_map = {
            Language.PYTHON: """
**Python Security Focus:**
- SQL injection in database queries
- Command injection in subprocess calls
- Path traversal in file operations
- Deserialization vulnerabilities
- Hardcoded secrets and credentials
- Insecure random number generation
- XSS in web applications
- CSRF vulnerabilities
- Insecure direct object references""",

            Language.JAVASCRIPT: """
**JavaScript Security Focus:**
- XSS vulnerabilities
- CSRF attacks
- Prototype pollution
- Insecure deserialization
- DOM-based vulnerabilities
- Insecure communication (HTTP vs HTTPS)
- Insecure storage of sensitive data
- Insecure random number generation
- Code injection vulnerabilities""",

            Language.TYPESCRIPT: """
**TypeScript Security Focus:**
- Same as JavaScript plus:
- Type safety bypasses
- Insecure type assertions
- Generic type vulnerabilities
- Interface pollution
- Unsafe type casting""",

            Language.CPP: """
**C++ Security Focus:**
- Buffer overflows
- Memory leaks
- Use-after-free vulnerabilities
- Integer overflow/underflow
- Format string vulnerabilities
- Race conditions
- Insecure memory management
- Type confusion vulnerabilities
- Stack corruption""",

            Language.JAVA: """
**Java Security Focus:**
- SQL injection
- Deserialization vulnerabilities
- Path traversal
- Insecure random number generation
- Hardcoded secrets
- Insecure communication
- Privilege escalation
- Memory leaks
- Insecure reflection usage""",

            Language.GO: """
**Go Security Focus:**
- SQL injection
- Command injection
- Path traversal
- Insecure random number generation
- Goroutine leaks
- Race conditions
- Insecure deserialization
- Hardcoded secrets
- Insecure communication""",

            Language.RUST: """
**Rust Security Focus:**
- Unsafe code usage
- Panic handling
- Resource leaks
- Integer overflow
- Insecure random number generation
- Hardcoded secrets
- Insecure communication
- Memory safety bypasses
- Concurrency issues"""
        }
        
        return security_map.get(language, "")


    def get_performance_prompt(self, code: str, language: Language) -> str:
        """Generate performance-focused review prompt"""
        
        performance_guidance = self.get_performance_guidance(language)
        
        return f"""You are a performance optimization expert specializing in {language.value}. Analyze the following code for performance issues:

```{language.value}
{code}
```

{performance_guidance}

Focus on identifying:
- Algorithmic inefficiencies
- Memory usage optimization
- I/O performance issues
- Concurrency opportunities
- Caching strategies
- Resource management
- Bottlenecks and hotspots
- Scalability concerns

Provide specific, measurable performance recommendations."""


    def get_performance_guidance(self, language: Language) -> str:
        """Get language-specific performance guidance"""
        
        performance_map = {
            Language.PYTHON: """
**Python Performance Focus:**
- Use list comprehensions over loops
- Leverage NumPy for numerical operations
- Use generators for large datasets
- Profile with cProfile
- Use __slots__ for memory optimization
- Consider Cython for critical paths
- Use multiprocessing for CPU-bound tasks
- Optimize string operations
- Use appropriate data structures""",

            Language.JAVASCRIPT: """
**JavaScript Performance Focus:**
- Use efficient DOM manipulation
- Leverage Web Workers for heavy computation
- Optimize event handling
- Use efficient data structures
- Minimize reflows and repaints
- Use requestAnimationFrame for animations
- Optimize network requests
- Use efficient loops and iterations
- Consider WebAssembly for critical paths""",

            Language.TYPESCRIPT: """
**TypeScript Performance Focus:**
- Same as JavaScript plus:
- Use efficient type checking
- Optimize generic usage
- Minimize type assertion overhead
- Use const assertions where appropriate""",

            Language.CPP: """
**C++ Performance Focus:**
- Use move semantics
- Optimize memory allocation
- Use efficient containers
- Leverage compiler optimizations
- Profile with tools like gprof
- Use const correctness
- Optimize loops and algorithms
- Use appropriate data structures
- Consider SIMD optimizations""",

            Language.JAVA: """
**Java Performance Focus:**
- Use appropriate collections
- Optimize garbage collection
- Use StringBuilder for string operations
- Profile with JProfiler or similar
- Use efficient I/O operations
- Optimize loops and algorithms
- Use appropriate data structures
- Consider JIT optimizations
- Use concurrency effectively""",

            Language.GO: """
**Go Performance Focus:**
- Use efficient goroutines
- Optimize memory allocation
- Use appropriate data structures
- Profile with pprof
- Use efficient I/O operations
- Optimize loops and algorithms
- Use channels effectively
- Consider garbage collection tuning
- Use sync.Pool for object reuse""",

            Language.RUST: """
**Rust Performance Focus:**
- Use efficient ownership patterns
- Optimize memory layout
- Use appropriate data structures
- Profile with cargo bench
- Use efficient I/O operations
- Optimize loops and algorithms
- Use zero-cost abstractions
- Consider unsafe optimizations
- Use efficient error handling"""
        }
        
        return performance_map.get(language, "") 