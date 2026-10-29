# Static Code Analysis – Issues and Fixes

## 1. Pylint

**Before:** 6.90/10  
**After:** 10.00/10

| Issue identified | Fix applied |
|---|---|
| Missing module and function docstrings | Added appropriate docstrings |
| Unused `os` import | Removed the unused import |
| Mutable default argument | Changed `batch_log=[]` to `batch_log=None` and initialized it inside the function |
| SQL query formatting | Replaced string interpolation with parameterized SQL |
| Bare exception handlers | Replaced them with specific exception types |
| File handling | Used context managers and specified UTF-8 encoding |
| Naming convention | Renamed `printStock()` to `print_stock()` |
| Long lines and formatting | Reformatted the code |

## 2. Bandit

**Before:** Security findings reported  
**After:** No issues identified

| Issue identified | Fix applied |
|---|---|
| B608 – Possible SQL injection | Used parameterized SQL queries |
| B110 – Try/except/pass | Replaced the silent exception handler with explicit exception handling |

## 3. Flake8

**Before:** Multiple style violations  
**After:** No violations reported

| Issue identified | Fix applied |
|---|---|
| F401 – Unused import | Removed the unused import |
| E302 and E305 – Incorrect blank lines | Corrected spacing around functions |
| E501 – Lines too long | Wrapped long lines |
| E722 – Bare except | Replaced bare exception handlers |
| E303 – Too many blank lines | Corrected excess blank lines |
