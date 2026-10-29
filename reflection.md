# Reflection on Static Code Analysis

This lab helped me understand how static code analysis tools improve code quality, readability, and security.

Pylint identified code-quality issues such as missing docstrings, unused imports, mutable default arguments, and naming convention violations. After making corrections, the final score improved to 10.00/10.

Bandit identified a potential SQL injection risk and a silent exception-handling issue. I addressed these findings by using parameterized SQL queries and explicit exception handling. The final Bandit scan reported no issues.

Flake8 identified formatting and style violations, including incorrect blank lines, long lines, and bare exception handlers. I corrected these issues, and the final Flake8 scan produced no output.

I learned that running multiple static analysis tools provides complementary feedback. Pylint focuses on code quality, Bandit checks for common security problems, and Flake8 enforces Python style conventions.

Overall, the lab demonstrated the importance of analyzing code, fixing reported issues, rerunning the tools, and retaining before-and-after reports to demonstrate the improvements.
