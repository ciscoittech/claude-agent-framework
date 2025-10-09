# Tool Usage Guide: Engineer Agent

## Tool Philosophy

Engineers implement efficiently by reading existing code first, making precise changes with appropriate tools, and validating through testing. The goal is working, tested code—use tools to understand context, implement changes correctly, and verify functionality through automated testing.

---

## Recommended Tool Patterns

### Pattern 1: Implementation Workflow
**When to Use**: Implementing a new feature or fixing a bug
**Workflow**:
1. `Read` relevant existing files to understand context
2. `Edit` existing files or `Write` new files as appropriate
3. `Bash` to run tests and verify implementation
4. Fix any issues and re-test

**Example**:
```
1. Read "src/services/auth.py" → understand existing auth service
2. Edit "src/services/auth.py" → add new method for token refresh
3. Bash "pytest tests/test_auth.py -v" → run auth tests
4. Edit if needed → fix test failures
5. Bash "pytest tests/test_auth.py -v" → verify all pass
```
**Token Cost**: ~15K (Read: 5K, Edit: 3K, Bash: 2K, Fixes: 5K)

### Pattern 2: Multi-File Changes
**When to Use**: Changes that span multiple related files (feature + tests, model + migration)
**Workflow**:
1. `Read` all affected files in parallel
2. Plan changes across files
3. `Edit` multiple files in sequence (or parallel if independent)
4. `Bash` to validate all changes together

**Example**:
```
1. Read ["models/user.py", "services/user.py", "tests/test_user.py"] in parallel
2. Plan: Add email verification to model, service, and tests
3. Edit "models/user.py" → add email_verified field
4. Edit "services/user.py" → add verify_email method
5. Edit "tests/test_user.py" → add verification tests
6. Bash "pytest tests/test_user.py" → verify all work together
```
**Token Cost**: ~20K (Read: 9K, Edit: 6K, Bash: 2K, Validation: 3K)

### Pattern 3: Testing Integration
**When to Use**: Every implementation task (testing is mandatory)
**Workflow**:
1. Implement code changes
2. `Bash` to run relevant test suite
3. Analyze failures and `Edit` to fix
4. Re-run tests until passing
5. Run broader test suite to check for regressions

**Example**:
```
1. Edit "api/endpoints.py" → add new /health endpoint
2. Bash "pytest tests/test_endpoints.py::test_health -v" → test specific
3. Edit "api/endpoints.py" → fix status code issue
4. Bash "pytest tests/test_endpoints.py::test_health -v" → passes
5. Bash "pytest tests/test_endpoints.py" → all endpoint tests pass
```
**Token Cost**: ~12K (Implementation: 5K, Testing: 4K, Fixes: 3K)

### Pattern 4: Code Search Before Implementation
**When to Use**: Before implementing anything new
**Workflow**:
1. `Grep` to search for similar implementations
2. `Read` the most relevant matches
3. Implement following established patterns
4. Avoid reinventing existing utilities

**Example**:
```
1. Grep "def.*validate.*email" → finds existing email validator
2. Read "utils/validators.py" → see validate_email function
3. Edit "services/user.py" → import and use existing validator
4. Don't write new email validation logic
```
**Token Cost**: ~6K (Grep: 2K, Read: 3K, Edit: 1K)

### Pattern 5: Validation and Quality Checks
**When to Use**: After implementation, before marking complete
**Workflow**:
1. `Bash` to run tests
2. `Bash` to run linter (flake8, pylint, eslint)
3. `Bash` to run type checker (mypy, tsc)
4. Fix issues and re-validate

**Example**:
```
1. Bash "pytest tests/" → all tests pass
2. Bash "flake8 src/" → finds style issues
3. Edit files to fix style issues
4. Bash "mypy src/" → finds type issues
5. Edit to add type hints
6. Bash "flake8 src/ && mypy src/" → all clean
```
**Token Cost**: ~10K (Tests: 3K, Linting: 2K, Typing: 2K, Fixes: 3K)

---

## Anti-Patterns to Avoid

1. ❌ **Using Bash for file operations**: Running `cat`, `grep`, or `sed` commands wastes tokens and bypasses tool optimization → ✅ **Instead**: Use dedicated `Read`, `Grep`, and `Edit` tools which are optimized for Claude Code

2. ❌ **Using Write when Edit should be used**: Overwriting existing files with `Write` loses context and risks losing code → ✅ **Instead**: Use `Edit` with old_string/new_string for surgical changes to existing files

3. ❌ **Implementing without reading existing code first**: Writing code without understanding context leads to inconsistent patterns → ✅ **Instead**: Always `Read` relevant files first to understand conventions, patterns, and integration points

4. ❌ **Skipping testing after implementation**: Marking tasks complete without running tests risks broken code → ✅ **Instead**: Always `Bash` to run tests after every implementation, fix failures before completing

5. ❌ **Using cat/grep/sed in Bash**: Commands like `cat file.py | grep pattern` waste tokens on unnecessary output → ✅ **Instead**: Use `Grep` tool for searching, `Read` tool for viewing, `Edit` tool for modifications

---

## Token Budget Allocation

**Typical Budget**: 50-80K tokens (varies by task complexity)

**Allocation**:
- Context Phase: 30% (~15-24K tokens) - Reading existing code, searching patterns
- Implementation Phase: 50% (~25-40K tokens) - Writing/editing code, iterating on design
- Validation Phase: 20% (~10-16K tokens) - Testing, linting, fixing issues

**Budget Management**:
- Use `Grep` to find relevant files before reading everything
- Read only files you'll modify plus immediate dependencies
- Make targeted edits rather than rewriting entire functions
- Run specific tests first (`pytest test_file.py::test_name`) before full suite

---

## Efficiency Tips

1. **Parallel Reads**: When you know you'll need multiple files, read them in parallel rather than sequentially. Example: If implementing a feature touching model, service, and API layers, read all three files simultaneously.

2. **Grep Before Read**: Search for existing implementations with `Grep` before reading files. This helps you find the right files quickly and understand what patterns already exist. Example: `Grep "class.*Config"` before implementing new configuration.

3. **Targeted Testing**: Run specific tests first (`pytest path/to/test.py::test_name`) to get fast feedback, then run broader suites. This saves time and tokens on test output.

4. **Edit Over Write**: Always prefer `Edit` for existing files. It's more token-efficient and safer than reading entire file, modifying in memory, and using `Write`. Only use `Write` for genuinely new files.

5. **Bash Chaining**: Chain related Bash commands with `&&` to run sequences efficiently. Example: `pytest tests/ && flake8 src/ && mypy src/` runs all validations in one call, failing fast if any step fails.

---

*Tool Usage Guide v1.0 - Engineer Agent*
*Part of Claude Agent Framework - Best Practices Integration*
