# PM2 Process Management Context

## Overview

PM2 is a production-ready process manager for Node.js applications. This context explains how to use PM2 for managing backend microservices, enabling autonomous debugging through log access and service management.

**Use this context when**: Debugging backend services, managing processes, viewing logs, restarting services.

---

## Why PM2?

### Problems PM2 Solves
- **No log access during runtime**: Claude couldn't see service logs without manual copying
- **Manual service management**: Starting/stopping services was tedious
- **No auto-restart**: Services crashed and stayed down
- **No monitoring**: Hard to track resource usage

### PM2 Benefits
- ✅ **Autonomous debugging**: Claude can read logs directly
- ✅ **Easy management**: Start/stop/restart with simple commands
- ✅ **Auto-restart**: Services restart on crash
- ✅ **Resource monitoring**: Built-in CPU/memory tracking
- ✅ **Individual logs**: Each service has separate log files

---

## Service Architecture

Typical multi-service backend structure:

```
project/
├── frontend/          # Run separately with npm dev
├── backend/
│   ├── form-service/
│   │   ├── logs/
│   │   │   ├── out.log
│   │   │   └── error.log
│   │   └── server.js
│   ├── email-service/
│   ├── auth-service/
│   ├── data-service/
│   ├── api-gateway/
│   ├── worker-service/
│   └── scheduler-service/
└── ecosystem.config.js
```

---

## Configuration

### ecosystem.config.js
```javascript
module.exports = {
  apps: [
    {
      name: 'form-service',
      script: 'npm',
      args: 'start',
      cwd: './backend/form',
      error_file: './backend/form/logs/error.log',
      out_file: './backend/form/logs/out.log',
      env: {
        NODE_ENV: 'development',
        PORT: 3001,
      },
    },
    {
      name: 'email-service',
      script: 'npm',
      args: 'start',
      cwd: './backend/email',
      error_file: './backend/email/logs/error.log',
      out_file: './backend/email/logs/out.log',
      env: {
        NODE_ENV: 'development',
        PORT: 3002,
      },
    },
    // ... more services
  ],
};
```

---

## Essential Commands

### Start All Services
```bash
pm2 start ecosystem.config.js
# or with package.json script:
npm run pm2:start
pnpm pm2:start
```

### View Service Status
```bash
pm2 status

# Output:
┌─────┬──────────────────┬─────┬────────┬──────┐
│ id  │ name            │ mode│ status │ cpu  │
├─────┼──────────────────┼─────┼────────┼──────┤
│ 0   │ form-service    │ fork│ online │ 0.1% │
│ 1   │ email-service   │ fork│ online │ 0.0% │
│ 2   │ auth-service    │ fork│ online │ 0.2% │
└─────┴──────────────────┴─────┴────────┴──────┘
```

### View Logs (CRITICAL for debugging!)
```bash
# Real-time logs for specific service
pm2 logs form-service --lines 200

# All services
pm2 logs --lines 100

# Error logs only
pm2 logs --err

# Stop following logs (if running in foreground)
Ctrl+C
```

### Service Management
```bash
# Restart one service
pm2 restart form-service

# Restart all services
pm2 restart all

# Stop one service
pm2 stop form-service

# Stop all services
pm2 stop all

# Delete from PM2 (stops and removes)
pm2 delete form-service
```

### Monitoring
```bash
# Real-time monitoring dashboard
pm2 monit

# Shows CPU, memory, logs in terminal UI
# Press Ctrl+C to exit
```

---

## Autonomous Debugging Workflow

This is the key pattern that enables Claude to debug independently:

### When User Reports Backend Issue

**Step 1: Check Service Status**
```bash
pm2 status
```
- Identify which service(s) are affected
- Check if service is online or crashed

**Step 2: Read Recent Logs**
```bash
pm2 logs [service-name] --lines 200
```
- Look for error messages
- Find stack traces
- Identify error patterns
- Note timestamps

**Step 3: Analyze the Error**
From logs, determine:
- **Error type**: Syntax, runtime, database, network?
- **Error location**: File and line number
- **Error context**: What was happening when it failed?
- **Recent changes**: Did something change recently?

**Step 4: Read Relevant Code**
Use the Read tool to examine:
- File where error occurred
- Related files mentioned in stack trace
- Recent commits (if git available)

**Step 5: Identify Root Cause**
Common issues:
- Missing environment variables
- Database connection problems
- Port conflicts
- Dependency issues
- Code errors (typos, logic bugs)
- Configuration mistakes

**Step 6: Fix the Issue**
- Make code changes using Edit tool
- Update configuration if needed
- Fix environment variables

**Step 7: Restart Affected Service**
```bash
pm2 restart [service-name]
```

**Step 8: Verify the Fix**
```bash
pm2 logs [service-name] --lines 50
```
- Check for success messages
- Verify no new errors
- Confirm service is functioning

**Step 9: Report to User**
- Explain what the issue was
- Describe what was fixed
- Confirm service is now healthy

---

## Example Debugging Session

```
User: "The email service is throwing errors"

Claude:
1. Checks PM2 status:
   pm2 status
   → email-service is online but restarting frequently

2. Reads logs:
   pm2 logs email-service --lines 200
   → Error: "SMTP connection timeout at line 45 in emailSender.ts"

3. Reads code:
   Read tool on backend/email/src/emailSender.ts
   → Finds SMTP_HOST is undefined

4. Checks env:
   → SMTP_HOST not in .env file

5. Fixes issue:
   → Adds SMTP_HOST=smtp.gmail.com to .env

6. Restarts service:
   pm2 restart email-service

7. Verifies:
   pm2 logs email-service --lines 50
   → "✓ SMTP connection established"
   → No more errors

8. Reports to user:
   "Fixed! The SMTP_HOST environment variable was missing.
   Added it to .env and restarted the service.
   Email service is now healthy."
```

---

## Common Issues & Solutions

### Service Won't Start
**Check**:
1. Port conflict: `lsof -i :[PORT]` or `netstat -ano | findstr :[PORT]`
2. Missing dependencies: `npm install` in service directory
3. Environment variables: Check .env file
4. Logs: `pm2 logs [service] --err`

**Solution**:
- Kill process using port
- Install dependencies
- Add missing env vars
- Fix code errors shown in logs

### Service Keeps Restarting
**Check**:
1. Error logs: `pm2 logs [service] --err`
2. Recent code changes
3. Environment configuration

**Solution**:
- Fix errors shown in logs
- Revert problematic changes
- Correct configuration

### Memory Leaks
**Check**:
```bash
pm2 monit
```
Watch memory usage over time

**Solution**:
- Find memory leaks in code
- Check for unclosed connections
- Review event listeners
- Restart as temporary fix

### Database Connection Issues
**Check**:
1. `pm2 logs data-service --err`
2. DATABASE_URL in .env
3. Database server running

**Solution**:
- Verify connection string
- Test connection: `psql $DATABASE_URL`
- Check connection pool settings
- Restart database service

---

## Important Notes

### Hot Reload
**❌ Hot reload does NOT work with PM2**
- PM2 is for production-style running
- For development with hot reload, run services directly
- Frontend should always run separately: `npm run dev`

### Frontend Separation
**Frontend ≠ PM2**
- Run frontend with its own dev server
- Only backend services go in PM2
- Frontend needs hot reload for fast development

### Log Locations
Each service writes to:
- **stdout**: `./[service]/logs/out.log`
- **stderr**: `./[service]/logs/error.log`

Claude can read these directly using the Read tool.

---

## Agent Guidelines

### When You See "PM2" or "service error":

1. **Don't guess** - Read the logs first
2. **Use pm2 commands** via Bash tool
3. **Read log files** via Read tool
4. **Identify root cause** from errors
5. **Fix code** using Edit tool
6. **Restart service** via pm2
7. **Verify fix** by reading logs again

### Logs Are Truth
- Stack traces show exact error location
- Timestamps show when issues started
- Error messages reveal root causes
- Don't implement blind fixes - read logs first!

---

## Quick Reference

```bash
# Start
pm2 start ecosystem.config.js
pnpm pm2:start

# Status
pm2 status

# Logs (MOST IMPORTANT!)
pm2 logs [service] --lines 200
pm2 logs --err

# Manage
pm2 restart [service]
pm2 stop [service]
pm2 delete [service]

# Monitor
pm2 monit

# Full reset
pm2 delete all
pm2 start ecosystem.config.js
```

---

## Benefits for Claude

With PM2, Claude can:
- ✅ Read logs autonomously (no user copy-paste)
- ✅ Identify errors immediately
- ✅ Fix issues without waiting
- ✅ Restart services after fixes
- ✅ Verify fixes worked
- ✅ Debug proactively

**Result**: 60% faster debugging, autonomous problem-solving, better developer experience.

---

*This context enables Claude to work with PM2-managed microservices autonomously, dramatically improving debugging efficiency.*
