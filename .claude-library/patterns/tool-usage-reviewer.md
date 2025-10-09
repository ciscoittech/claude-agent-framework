# Tool Usage Guide: Reviewer Agent

## Tool Philosophy

Reviewers search strategically to find issues, read critically to assess quality, and report concisely with actionable feedback. The goal is quality assurance, not fixing—use tools to automate checks, target high-risk areas, and provide specific, file-and-line-referenced feedback that engineers can act on immediately.

---

## Recommended Tool Patterns

### Pattern 1: Automated Checks First
**When to Use**: Starting every code review
**Workflow**:
1. `Bash` to run test suite
2. `Bash` to run linter
3. `Bash` to run type checker
4. `Bash` to run security scanners if available
5. Only proceed to manual review if automated checks pass

**Example**:
```
1. Bash "pytest tests/ -v --cov" → check test coverage
2. Bash "flake8 src/ --count" → check style issues
3. Bash "mypy src/ --strict" → check type safety
4. Bash "bandit -r src/" → check security issues
5. Review report: "Automated checks found 3 issues before manual review"
```
**Token Cost**: ~8K (Tests: 3K, Linting: 2K, Types: 2K, Security: 1K)

### Pattern 2: Security Scanning
**When to Use**: Every code review (mandatory security check)
**Workflow**:
1. `Grep` for sensitive patterns (API keys, secrets, hardcoded passwords)
2. `Grep` for security anti-patterns (SQL injection, XSS vulnerabilities)
3. `Read` flagged files to assess severity
4. Document findings with specific line numbers

**Example**:
```
1. Grep "api[_-]?key|secret|password.*=.*['\"]" -i → finds 2 matches
2. Grep "execute.*\+|format.*\%" type:py → SQL injection patterns
3. Read "config/settings.py:45-50" → confirm API key in code
4. Report: "SECURITY: API key hardcoded in config/settings.py:47"
```
**Token Cost**: ~6K (Grep: 3K, Read: 2K, Analysis: 1K)

### Pattern 3: Targeted Review
**When to Use**: Reviewing specific changes or components
**Workflow**:
1. `Grep` for files containing the feature/change
2. `Grep` with `-C` context to see surrounding code
3. `Read` only the specific lines needing deep review
4. Avoid reading entire files unnecessarily

**Example**:
```
1. Grep "def.*authenticate" files_with_matches → 3 files found
2. Grep "def.*authenticate" content -C 10 → see function context
3. Read "auth/service.py:145-180" → deep dive on main auth function
4. Report: "auth/service.py:167 - Missing input validation"
```
**Token Cost**: ~7K (Grep: 3K, Read: 3K, Analysis: 1K)

### Pattern 4: Coverage Analysis
**When to Use**: Assessing test completeness
**Workflow**:
1. `Bash` to run coverage report
2. `Grep` for untested files or low-coverage areas
3. `Read` untested code to assess risk
4. Prioritize review feedback on untested critical paths

**Example**:
```
1. Bash "pytest --cov=src --cov-report=term-missing" → 78% coverage
2. Grep "0%|[0-9]%" coverage report → find untested files
3. Read "services/payment.py" → critical payment logic untested
4. Report: "CRITICAL: services/payment.py has 0% test coverage"
```
**Token Cost**: ~9K (Coverage: 4K, Analysis: 3K, Read: 2K)

### Pattern 5: Priority-Based Review
**When to Use**: Every code review (structured approach)
**Workflow**:
1. Security issues first (Pattern 2)
2. Test coverage second (Pattern 4)
3. Code quality third (automated checks)
4. Style last (lowest priority)

**Example**:
```
Priority 1 - Security:
- Grep for secrets, injection patterns → 1 issue found

Priority 2 - Tests:
- Bash coverage report → 85%, payment.py at 45%

Priority 3 - Quality:
- Bash "flake8 && mypy" → 5 type hints missing

Priority 4 - Style:
- Note: Minor formatting issues, defer to linter auto-fix
```
**Token Cost**: ~15K (Security: 5K, Coverage: 5K, Quality: 3K, Style: 2K)

---

## Anti-Patterns to Avoid

1. ❌ **Reading entire codebase**: Attempting to read every file wastes tokens and provides little value → ✅ **Instead**: Use `Grep` to target specific patterns, then `Read` only flagged areas with context

2. ❌ **Modifying code as reviewer**: Reviewers who fix issues blur responsibilities and skip proper review process → ✅ **Instead**: Document issues with file:line references and let engineers implement fixes

3. ❌ **Reviewing without running automated checks**: Manual-only reviews miss issues that tools catch instantly → ✅ **Instead**: Always run tests, linters, and type checkers first with `Bash` before manual review

4. ❌ **Skipping security scanning**: Assuming code is secure without checking for common vulnerabilities → ✅ **Instead**: Always `Grep` for secrets, injection patterns, and other security anti-patterns

5. ❌ **Providing vague feedback without references**: Comments like "fix the auth code" aren't actionable → ✅ **Instead**: Provide specific file:line references like "auth/service.py:167 - Missing input validation on email parameter"

---

## Token Budget Allocation

**Typical Budget**: 40K tokens

**Allocation**:
- Search Phase: 50% (~20K tokens) - Automated checks, Grep patterns, coverage analysis
- Analysis Phase: 40% (~16K tokens) - Reading flagged code, assessing severity, understanding context
- Reporting Phase: 10% (~4K tokens) - Writing structured feedback with specific references

**Budget Management**:
- Run all automated checks in parallel with `Bash` commands
- Use `Grep files_with_matches` before `content` mode to estimate scope
- Read specific line ranges (e.g., `Read "file.py:100-150"`) not entire files
- Focus manual review on high-risk areas: security, untested code, complex logic

---

## Efficiency Tips

1. **Parallel Automated Checks**: Run tests, linting, and type checking in parallel at the start of every review. Example: Launch `pytest`, `flake8`, and `mypy` simultaneously to get all automated feedback in one round trip.

2. **Security Patterns Library**: Maintain a list of security-related Grep patterns to search consistently. Example: Create `.claude-library/patterns/security-patterns.txt` with patterns for API keys, SQL injection, XSS, CSRF tokens, etc.

3. **Context Lines Strategy**: Use `Grep -C 5` to see surrounding code context without reading entire files. This helps assess whether flagged patterns are actually problematic or just false positives.

4. **Coverage-Driven Review**: Always check test coverage first and prioritize reviewing untested code. Untested critical paths (auth, payments, data validation) deserve deepest scrutiny.

5. **Structured Reporting**: Use consistent format for feedback: `[SEVERITY] file:line - Issue description - Suggested fix`. Example: `[CRITICAL] auth/service.py:167 - Missing input validation on email parameter - Add email format validation before database query`.

---

*Tool Usage Guide v1.0 - Reviewer Agent*
*Part of Claude Agent Framework - Best Practices Integration*
