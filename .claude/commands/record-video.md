# /record-video Command

**Purpose**: Automated training video creation using Playwright/MCP with the Claude Agent Framework

## Command Syntax

```bash
/record-video "path/to/script.md" [options]
```

### Options
- `--output-dir` - Custom output directory (default: `.video-artifacts/[script-name]/`)
- `--dry-run` - Generate automation without recording
- `--skip-validation` - Skip prerequisite checks (not recommended)
- `--compress` - Auto-compress recordings after completion

## Workflow Overview

This command orchestrates a complete video recording pipeline:

```
┌─────────────────────────────────────────────────────┐
│  STAGE 1: Planning & Validation (Parallel)          │
│  - Video Recording Specialist: Parse script         │
│  - Framework Validation Engineer: Check prereqs     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 2: Automation Generation (Sequential)        │
│  - Video Recording Specialist: Create Playwright    │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 3: Recording Execution (Sequential)          │
│  - Video Recording Specialist: Record all scenes    │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  STAGE 4: Validation & Cleanup (Parallel)           │
│  - Framework Validation Engineer: Verify quality    │
│  - Video Recording Specialist: Generate manifest    │
└─────────────────────────────────────────────────────┘
```

## Stage 1: Planning & Validation (Parallel - 15 seconds)

### Agent 1: Video Recording Specialist
**Task**: Parse training script and create recording plan

**Prompt Template**:
```markdown
You are the Video Recording Specialist. Analyze this training video script and create a detailed recording plan.

## Training Script
{SCRIPT_CONTENT}

## Your Tasks
1. Parse all scenes with timings and actions
2. Identify prerequisites (Playwright, MCP tools, project setup)
3. Calculate total duration and resource needs
4. Create scene execution order
5. Identify time-jump points for post-production

## Output Format
**Recording Plan**:
- Total scenes: N
- Estimated duration: Xm Ys
- Prerequisites: [list]
- Artifacts directory: [path]
- Time jumps: [list scenes with jumps]

**Scene Breakdown**:
[Table with: Scene #, Title, Duration, Actions, Time Jump (Y/N)]
```

### Agent 2: Framework Validation Engineer
**Task**: Verify recording prerequisites and environment

**Prompt Template**:
```markdown
You are the Framework Validation Engineer. Verify the recording environment is ready.

## Validation Checklist
1. Check Playwright installation (`npx playwright --version`)
2. Verify MCP tools availability (check for `mcp__playwright__*`)
3. Confirm git safety (`.gitignore` includes `.video-artifacts/`)
4. Validate project structure (CLAUDE.md exists, framework present)
5. Check disk space for recordings (estimate: {DURATION} * 50MB/min)

## Your Tasks
- Run all prerequisite checks
- Report any missing dependencies
- Suggest fixes for any issues
- Confirm ready to record or block if critical failures

## Output Format
**Prerequisite Validation**:
✅/❌ Playwright: [version or install command]
✅/❌ MCP Tools: [available tools or fallback plan]
✅/❌ Git Safety: [.gitignore status]
✅/❌ Project Ready: [CLAUDE.md, framework status]
✅/❌ Disk Space: [available vs needed]

**Status**: READY / BLOCKED
**Blocking Issues**: [if any]
```

**Execution**: Both agents run in parallel (single message with 2 Task calls)

## Stage 2: Automation Generation (Sequential - 30 seconds)

### Agent: Video Recording Specialist
**Task**: Generate Playwright automation scripts for all scenes

**Prompt Template**:
```markdown
You are the Video Recording Specialist. Generate Playwright automation for the approved recording plan.

## Recording Plan
{RECORDING_PLAN_FROM_STAGE_1}

## Training Script
{SCRIPT_CONTENT}

## Your Tasks
1. Create main Playwright test file (`.video-artifacts/{NAME}/recorder.spec.ts`)
2. Generate scene-specific automation for each scene
3. Add time-jump visual indicators at designated points
4. Include validation checks after each scene
5. Configure video output settings (1080p, 30fps, webm)

## Automation Requirements
- Use Playwright video recording API
- Insert visual markers for time jumps (overlay with ⏭️ icon)
- Capture terminal interactions using terminal emulator
- Handle Claude Code CLI authentication flow
- Use `page.waitForTimeout()` for intentional pauses
- Save each scene as separate video file

## Output
Create the complete Playwright test suite in:
`.video-artifacts/{VIDEO_NAME}/recorder.spec.ts`

Include configuration in:
`.video-artifacts/{VIDEO_NAME}/playwright.config.ts`
```

**Execution**: Sequential (needs plan from Stage 1)

## Stage 3: Recording Execution (Sequential - Script Duration + 20%)

### Agent: Video Recording Specialist
**Task**: Execute Playwright automation and record all scenes

**Prompt Template**:
```markdown
You are the Video Recording Specialist. Execute the Playwright automation and record the training video.

## Automation Files
- Recorder: `.video-artifacts/{VIDEO_NAME}/recorder.spec.ts`
- Config: `.video-artifacts/{VIDEO_NAME}/playwright.config.ts`

## Your Tasks
1. Run Playwright tests with video recording enabled
2. Monitor execution and capture any errors
3. Save scene recordings to artifacts directory
4. Generate time-jump markers as separate image files
5. Create scene metadata (duration, file size, quality)

## Execution Command
```bash
cd .video-artifacts/{VIDEO_NAME}
npx playwright test --project=chromium --headed
```

## Error Handling
- If scene fails: capture error, save partial recording, continue
- If critical failure: stop, report, preserve artifacts
- Retry policy: 1 retry per scene on non-critical errors

## Output Format
**Recording Progress**:
🎬 Scene 1/10: Introduction
  ⏺️ Recording... (expected: 0:20)
  ✅ Complete - scene-01-intro.webm (actual: 0:21)
  📁 Size: 15MB

[Repeat for all scenes]

**Recording Summary**:
- Scenes completed: X/N
- Total duration: Xm Ys
- Total size: XMB
- Failures: [if any]
```

**Execution**: Sequential (must complete scene-by-scene)

## Stage 4: Validation & Cleanup (Parallel - 20 seconds)

### Agent 1: Framework Validation Engineer
**Task**: Validate recording quality and completeness

**Prompt Template**:
```markdown
You are the Framework Validation Engineer. Validate the training video recordings.

## Validation Criteria
1. **File Existence**: All scene files present
2. **Playability**: Recordings are valid video files (check with `ffprobe`)
3. **Duration**: Actual duration within ±10% of expected
4. **Quality**: Resolution 1080p, frame rate 30fps
5. **Completeness**: All scenes from script recorded

## Artifacts Directory
`.video-artifacts/{VIDEO_NAME}/`

## Your Tasks
- Verify all scene recordings exist
- Check video metadata (resolution, fps, codec)
- Validate durations match script
- Test playability (quick probe, not full playback)
- Report quality metrics

## Output Format
**Validation Results**:

Scene Validation:
✅/❌ Scene 1: scene-01-intro.webm (0:21, 1920x1080, 30fps)
[Repeat for all scenes]

Quality Metrics:
✅/❌ All files exist
✅/❌ Correct resolution (1080p)
✅/❌ Correct frame rate (30fps)
✅/❌ Duration accuracy (±10%)
✅/❌ Playability verified

**Overall Status**: PASSED / FAILED
**Issues**: [if any]
```

### Agent 2: Video Recording Specialist
**Task**: Generate manifest and post-production notes

**Prompt Template**:
```markdown
You are the Video Recording Specialist. Create the recording manifest and post-production guide.

## Recording Artifacts
Directory: `.video-artifacts/{VIDEO_NAME}/`

## Your Tasks
1. Create manifest.json with complete metadata
2. Generate post-production notes for editing
3. Create .gitignore entry (if missing)
4. Provide compression commands (optional)

## Manifest Structure
```json
{
  "video_name": "{VIDEO_NAME}",
  "script_source": "{SCRIPT_PATH}",
  "recorded_date": "YYYY-MM-DD",
  "total_duration_seconds": N,
  "total_size_mb": N,
  "scenes": [
    {
      "number": 1,
      "title": "Introduction",
      "file": "scene-01-intro.webm",
      "duration_seconds": 20,
      "size_mb": 15,
      "has_time_jump": false,
      "time_jump_marker": null
    },
    ...
  ],
  "post_production": {
    "time_jumps": [
      {"scene": 2, "marker_file": "scene-02-jump-marker.png"}
    ],
    "editing_notes": [
      "Add background music at 10% volume",
      "Fade transitions between scenes",
      "Insert time-jump indicators during editing"
    ]
  }
}
```

## Post-Production Notes
Create: `.video-artifacts/{VIDEO_NAME}/POST_PRODUCTION.md`

Include:
- Scene assembly order
- Time-jump insertion points
- Visual effects to add
- Audio mixing notes
- Export settings recommendations

## Your Output
Create both files and report their locations.
```

**Execution**: Both agents run in parallel (single message with 2 Task calls)

## Success Criteria

### Recording Complete
- ✅ All scenes recorded successfully
- ✅ Duration within expected range
- ✅ Quality validation passed
- ✅ Manifest generated
- ✅ Git safety verified

### Deliverables
```
.video-artifacts/{VIDEO_NAME}/
├── scenes/
│   ├── scene-01-intro.webm
│   ├── scene-02-download.webm
│   └── ... [all scenes]
├── markers/
│   ├── scene-02-jump-marker.png
│   └── ... [time-jump markers]
├── recorder.spec.ts
├── playwright.config.ts
├── manifest.json
└── POST_PRODUCTION.md
```

## Error Handling

### Common Issues

**Issue**: Playwright not installed
- **Auto-fix**: Run `npm install -D @playwright/test`
- **Retry**: Attempt Stage 1 again

**Issue**: Recording fails mid-scene
- **Recovery**: Save partial recording, log error, continue to next scene
- **Final**: Report failed scenes in manifest

**Issue**: Disk space insufficient
- **Block**: Stop before recording, report to user
- **Suggest**: Free space or reduce quality settings

**Issue**: Git safety not configured
- **Auto-fix**: Add `.video-artifacts/` to `.gitignore`
- **Verify**: Confirm entry exists before proceeding

## Performance Targets

| Stage | Target Duration | Agents | Execution |
|-------|----------------|--------|-----------|
| Planning & Validation | 15s | 2 | Parallel |
| Automation Generation | 30s | 1 | Sequential |
| Recording Execution | Script + 20% | 1 | Sequential |
| Validation & Cleanup | 20s | 2 | Parallel |

**Total Overhead**: ~65s + script duration

## Usage Examples

### Example 1: Basic Recording
```bash
/record-video "TRAINING_VIDEO_SCRIPT.md"
```

### Example 2: Dry Run (No Recording)
```bash
/record-video "TRAINING_VIDEO_SCRIPT.md" --dry-run
```

### Example 3: Custom Output with Compression
```bash
/record-video "TRAINING_VIDEO_SCRIPT.md" --output-dir "./training-videos/v1" --compress
```

## Integration with Framework

### Contexts Loaded
- Training script (provided as argument)
- Project CLAUDE.md (for demonstration context)
- Framework patterns (for proper workflow demonstration)

### Agents Used
1. **Video Recording Specialist** (primary - all stages)
2. **Framework Validation Engineer** (stages 1 & 4)

### Optional Observability
If enabled in REGISTRY.json:
- Track workflow execution in Logfire
- Validate scene recordings via Observer agent
- Monitor performance metrics

## Git Safety Protocol

### Required .gitignore Entries
```gitignore
# Video recording artifacts
.video-artifacts/
*.webm
*.mp4
*.mov

# Playwright recordings
test-results/
playwright-report/
```

### Verification Steps
1. Check `.gitignore` includes `.video-artifacts/`
2. Add entry if missing (auto-fix enabled)
3. Verify with `git check-ignore .video-artifacts/`
4. Block if git safety cannot be guaranteed

## Cleanup Options

### Auto-Cleanup (Optional)
After successful recording:
- Compress recordings (if `--compress` flag used)
- Remove intermediate files (Playwright cache, etc.)
- Keep: scenes, markers, manifest, post-production notes

### Manual Cleanup
User can delete artifacts:
```bash
rm -rf .video-artifacts/{VIDEO_NAME}/
```

Manifest preserved for reference if needed later.

## Framework Compliance

### Simplicity Enforcement
- ✅ Minimal prerequisites (Playwright only)
- ✅ Sequential recording (one scene at a time)
- ✅ Simple validation (file existence + metadata)
- ✅ No over-engineering (basic Playwright API)

### Progressive Complexity
- **Level 1**: Basic terminal recording
- **Level 2**: Time-jump markers (this implementation)
- **Level 3**: Multi-window coordination (future)
- **Level 4**: Real-time editing (future)

### Performance Optimization
- Parallel validation where possible (Stages 1 & 4)
- Minimal context loading (script + project context only)
- Agent reuse (same specialist across stages)
- Fast validation (probe, don't full playback)

---

*Training Video Recording Command v1.0*
*Part of Claude Agent Framework - Optimized for minimal overhead and maximum automation*
