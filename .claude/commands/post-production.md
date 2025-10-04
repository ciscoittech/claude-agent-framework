# /post-production Command

**Purpose**: Automate complete video post-production workflow using parallel agent execution

## Command Syntax

```bash
/post-production [options]
```

### Options
- `--skip-narration` - Skip narration generation (use existing audio)
- `--skip-music` - Omit background music
- `--format [youtube|web|all]` - Export specific format only (default: all)
- `--dry-run` - Preview workflow without execution

## Workflow Overview

This command orchestrates a multi-stage video post-production pipeline using the Claude Agent Framework's parallel execution patterns.

```
Stage 1: Asset Generation (PARALLEL - 3 agents)
├─ Narration Generator    → Generate TTS audio files
├─ Effects Compositor     → Create visual overlays
└─ Audio Mixer           → Prepare sound effects library

Stage 2: Video Assembly (SEQUENTIAL - 1 agent)
└─ Video Compositor      → Combine all assets into complete video

Stage 3: Export (PARALLEL - 3 agents)
├─ YouTube Exporter      → 1080p optimized
├─ Web Exporter          → 720p lightweight
└─ Archive Exporter      → ProRes master
```

## Workflow Stages

### Stage 1: Asset Generation (Parallel Execution)

Launch all three agents **simultaneously** using parallel Task calls:

#### Agent 1: Narration Generator
**Task**: Convert script narration text to natural speech audio
**Input**: `manifest.json` scene narration text
**Output**: `automation/assets/narration/scene_*.mp3` (10 files)
**Tech**: Coqui TTS (local) or ElevenLabs Free API
**Duration**: ~2-3 minutes

#### Agent 2: Effects Compositor
**Task**: Generate visual overlays and effects
**Output**:
- Time-jump indicators (4 overlay images)
- Annotation arrows (3 for Scene 6)
- Flow diagram frames (Scene 8 animation)
- Progress bar graphics
**Tech**: MoviePy + PIL (Python)
**Duration**: ~1-2 minutes

#### Agent 3: Audio Mixer
**Task**: Prepare sound effects and background music
**Output**:
- Whoosh sound effect (normalized to -18dB)
- Ding sound effect (normalized to -20dB)
- Background music track (ducked to -30dB)
**Tech**: MoviePy AudioFileClip
**Duration**: ~1 minute

**Stage 1 Total Time**: ~3 minutes (parallel execution)

---

### Stage 2: Video Assembly (Sequential Execution)

After Stage 1 completes, launch the Video Compositor agent.

#### Agent 4: Video Compositor (Orchestrator)
**Task**: Assemble complete video from all components
**Dependencies**: Requires all Stage 1 outputs
**Process**:
1. Load 10 scene video files from Playwright recordings
2. Apply visual overlays at appropriate timestamps
3. Sync narration audio to each scene
4. Insert time-jump effects (Scenes 2, 4, 5, 7)
5. Add sound effects (whoosh, ding)
6. Apply transitions (0.3s cross-dissolve)
7. Mix background music (if enabled)
8. Generate draft master video

**Output**: `output/master/training-video-master.mp4`
**Tech**: MoviePy VideoFileClip + CompositeVideoClip
**Duration**: ~5-7 minutes

---

### Stage 3: Export (Parallel Execution)

Video Compositor spawns 3 export agents **simultaneously**.

#### Agent 5: YouTube Exporter
**Task**: Export YouTube-optimized format
**Settings**:
- Resolution: 1920x1080 (1080p)
- Codec: H.264 (x264)
- Bitrate: 12 Mbps VBR
- Audio: AAC 320 kbps
- Frame Rate: 30 fps
**Output**: `output/youtube/training-video-youtube.mp4`
**Duration**: ~3-4 minutes

#### Agent 6: Web Exporter
**Task**: Export web/social media format
**Settings**:
- Resolution: 1280x720 (720p)
- Codec: H.264
- Bitrate: 6 Mbps VBR
- Audio: AAC 192 kbps
- Frame Rate: 30 fps
**Output**: `output/web/training-video-web.mp4`
**Duration**: ~2-3 minutes

#### Agent 7: Archive Exporter
**Task**: Export high-quality master archive
**Settings**:
- Codec: Apple ProRes 422 HQ
- Resolution: 1920x1080
- Audio: PCM 48kHz 24-bit
- Purpose: Future editing
**Output**: `output/master/training-video-archive.mov`
**Duration**: ~2-3 minutes

**Stage 3 Total Time**: ~4 minutes (parallel execution)

---

## Total Workflow Time

- **Stage 1 (Parallel)**: 3 minutes
- **Stage 2 (Sequential)**: 7 minutes
- **Stage 3 (Parallel)**: 4 minutes
- **Total**: ~15 minutes

## Prerequisites

### Software Requirements
- Python 3.9+
- MoviePy 2.2.1+
- FFmpeg (already installed)
- Coqui TTS or ElevenLabs API access

### Input Requirements
- Playwright recordings in `test-results/` (10 scenes)
- `manifest.json` with scene metadata
- `POST_PRODUCTION.md` with specifications
- Training script narration text

### Disk Space
- Temporary files: ~500 MB
- Final exports: ~200 MB total
- **Required**: 1 GB free space

## Usage Examples

### Basic Usage (All Formats)
```bash
/post-production
```
Generates narration, effects, and exports all 3 formats.

### YouTube Only
```bash
/post-production --format youtube
```
Fastest option - only exports YouTube format.

### Skip Background Music
```bash
/post-production --skip-music
```
Narration and sound effects only.

### Dry Run (Preview Workflow)
```bash
/post-production --dry-run
```
Shows what would be executed without running.

## Output Structure

```
automation/
├── assets/
│   ├── narration/
│   │   ├── scene_01.mp3
│   │   ├── scene_02.mp3
│   │   └── ... (10 files)
│   ├── overlays/
│   │   ├── time-jump-01.png
│   │   ├── time-jump-02.png
│   │   ├── arrow-fastapi.png
│   │   ├── arrow-postgresql.png
│   │   ├── arrow-pytest.png
│   │   └── flow-diagram-*.png (10 frames)
│   └── sound-effects/
│       ├── whoosh.mp3
│       ├── ding.mp3
│       └── background-music.mp3
└── output/
    ├── youtube/
    │   └── training-video-youtube.mp4
    ├── web/
    │   └── training-video-web.mp4
    └── master/
        ├── training-video-master.mp4
        └── training-video-archive.mov
```

## Success Criteria

After completion, verify:
- ✅ All 10 scenes assembled correctly
- ✅ Narration synced to video
- ✅ 4 time-jumps applied with visual effects
- ✅ Sound effects audible but not overpowering
- ✅ Video duration: 3:50-4:00 minutes
- ✅ All export formats generated
- ✅ Audio/video sync maintained
- ✅ No compression artifacts

## Error Handling

### Narration Generation Fails
- **Fallback**: Use silent placeholders, continue with visuals
- **Recovery**: Re-run with `--skip-effects --skip-mixing`

### Effect Composition Fails
- **Fallback**: Use original recordings without overlays
- **Recovery**: Generate effects separately, re-compose

### Export Fails
- **Fallback**: Retry with lower quality settings
- **Recovery**: Export one format at a time

## Agent Coordination

This command demonstrates the framework's key patterns:

1. **Parallel Execution**: Stage 1 and 3 maximize throughput
2. **Sequential Dependencies**: Stage 2 waits for Stage 1
3. **Hierarchical Orchestration**: Video Compositor spawns exporters
4. **Clear Boundaries**: Each agent has single responsibility
5. **Tool Restrictions**: Agents only use required tools

## Performance Optimization

- Stage 1 parallelism: 3x speedup (9 min → 3 min)
- Stage 3 parallelism: 3x speedup (12 min → 4 min)
- Total savings: ~18 minutes vs sequential
- Framework overhead: < 30 seconds

## Next Steps After Completion

1. **Review Output**: Watch `output/master/training-video-master.mp4`
2. **Quality Check**: Verify audio sync and visual quality
3. **Upload**: Use `output/youtube/` for YouTube
4. **Archive**: Store `training-video-archive.mov` for future edits
5. **Distribute**: Use `output/web/` for website/social media

---

**Command Version**: 1.0
**Framework Pattern**: Parallel Multi-Stage Workflow
**Complexity Level**: Medium (7 agents, 3 stages)
**Estimated Runtime**: 15 minutes
**Total Cost**: $0 (all free/open-source tools)
