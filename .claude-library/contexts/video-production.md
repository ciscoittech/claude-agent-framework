# Video Production Context

Shared knowledge base for all video post-production agents. This context provides specifications, standards, and common patterns used across the training video workflow.

## Project Overview

**Video**: Claude Agent Framework Training Video
**Duration**: 3:50-4:00 minutes
**Resolution**: 1920x1080 (1080p)
**Frame Rate**: 30 fps
**Total Scenes**: 10

## Source Files

### Playwright Recordings
- Location: `test-results/[test-name]/video.webm`
- Format: WebM (VP8)
- Resolution: 1920x1080
- Created by: /record-video command

### Metadata
- `manifest.json`: Scene metadata, timing, narration text
- `POST_PRODUCTION.md`: Complete editing specifications
- `TRAINING_VIDEO_SCRIPT.md`: Original script with narration

## Scene Structure

| Scene | Title | Start | End | Duration | Time Jump |
|-------|-------|-------|-----|----------|-----------|
| 1 | Introduction | 0:00 | 0:20 | 20s | No |
| 2 | Download Framework | 0:20 | 0:45 | 25s | **Yes** |
| 3 | Create CLAUDE.md | 0:45 | 1:10 | 25s | No |
| 4 | Login to Claude Code | 1:10 | 1:30 | 20s | **Yes** |
| 5 | Generate Agent System | 1:30 | 2:00 | 30s | **Yes** |
| 6 | Understanding Creation | 2:00 | 2:30 | 30s | No |
| 7 | Execute Command | 2:30 | 3:00 | 30s | **Yes** |
| 8 | Watch Agents Execute | 3:00 | 3:30 | 30s | No |
| 9 | Key Takeaways | 3:30 | 3:50 | 20s | No |
| 10 | Next Steps | 3:50 | 4:00 | 10s | No |

## Visual Style Standards

### Terminal Appearance
- **Background**: #1e1e1e (dark gray)
- **Text Color**: #d4d4d4 (light gray)
- **Font**: Fira Code or JetBrains Mono, 18pt
- **Prompt Color**: #4ade80 (green)
- **Command Color**: #60a5fa (blue)

### Framework Color Scheme
- **Architect Agent**: #3b82f6 (blue)
- **Engineer Agent**: #10b981 (green)
- **Test Agent**: #fbbf24 (yellow)
- **Reviewer Agent**: #a855f7 (purple)
- **Success/Checkmarks**: #4ade80 (bright green)

### Overlay Styling
- **Semi-transparent backgrounds**: rgba(0, 0, 0, 0.85)
- **Border radius**: 12px for rounded corners
- **Padding**: 24-48px for comfortable spacing
- **Font**: Courier New Bold or JetBrains Mono Bold

## Audio Specifications

### Narration
- **Level**: -12 dB average, -6 dB peak
- **Processing**: De-esser, light compression (3:1), EQ (high-pass 80Hz, boost 2-5kHz)
- **Format**: MP3, 320 kbps, 48 kHz, stereo
- **Source**: Coqui TTS or ElevenLabs

### Sound Effects
- **Whoosh** (time-jumps): -18 dB, 0.9s, frequency sweep 200-1200 Hz
- **Ding** (progress): -20 dB, 0.3s, gentle chime with reverb
- **Background Music**: -30 to -35 dB, ducked -8 dB during narration

### Final Mix Balance
- Narration: 0 dB (reference)
- Sound effects: -12 to -18 dB
- Background music: -24 to -30 dB

## Time-Jump Specifications

Time-jumps allow the video to skip long processes while maintaining viewer awareness.

### Visual Pattern
1. Screen dims to 70% brightness (0.2s fade)
2. Overlay appears: "⏭️ [Process name]... ✓"
3. Hold for 1.5 seconds
4. Whoosh sound effect
5. Screen returns to 100% brightness (0.2s fade)
6. Continue with result

### Time-Jump Locations

**Jump 1 - Scene 2** (~0:35):
- Process: Git clone download
- Skip: ~5-10 seconds of git output
- Message: "Framework downloaded ✓"

**Jump 2 - Scene 4** (~1:20):
- Process: Authentication flow
- Skip: ~30-60 seconds of auth screens
- Message: "Authenticated ✓"

**Jump 3 - Scene 5** (~1:40):
- Process: Agent generation (multi-step)
- Skip: ~2-3 minutes of generation
- Messages:
  - "Analyzing project... ✓"
  - "Assessing complexity... ✓"
  - "Generating agents... ✓"
  - "Creating commands... ✓"

**Jump 4 - Scene 7** (~2:40):
- Process: Feature implementation
- Skip: ~1-2 minutes of coding
- Messages:
  - "Writing tests... ✓"
  - "Implementing feature... ✓"
  - "Running tests... ✓"
  - "Code review... ✓"

## Visual Effects Catalog

### Scene-Specific Effects

**Scene 6 - Annotations** (2:00-2:30):
- Arrow 1: Points to FastAPI patterns (cyan, left side)
- Arrow 2: Points to PostgreSQL queries (green, left side)
- Arrow 3: Points to pytest integration (yellow, left side)
- Timing: Stagger by 2-3 seconds each

**Scene 8 - Flow Diagram** (3:00-3:30):
- Animated agent workflow diagram
- Shows: Architect → Engineers (parallel) → Test → Reviewer → Done
- Colors: Blue, Green, Yellow, Purple
- Duration: 6 seconds animated sequence

## Transition Standards

- **Between scenes**: 0.3s cross-dissolve
- **Exception**: Scene 9→10 uses 1s fade to black, then fade in

## Export Format Specifications

### YouTube (1080p)
```
Resolution: 1920x1080
Codec: H.264 (High, L4.2)
Bitrate: 12 Mbps VBR
Audio: AAC 320 kbps
Target Size: ~150 MB
```

### Web (720p)
```
Resolution: 1280x720
Codec: H.264 (Main, L3.1)
Bitrate: 6 Mbps VBR
Audio: AAC 192 kbps
Target Size: ~75 MB
```

### Archive (ProRes)
```
Resolution: 1920x1080
Codec: ProRes 422 HQ
Audio: PCM 24-bit 48 kHz
Target Size: ~1 GB
```

## File Naming Conventions

### Assets
- Narration: `scene_01.mp3` through `scene_10.mp3`
- Overlays: `time-jump-##.png`, `arrow-*.png`, `progress-#.png`
- Sound FX: `whoosh.mp3`, `ding.mp3`, `background-music.mp3`

### Outputs
- Master: `training-video-master.mp4`
- YouTube: `training-video-youtube.mp4`
- Web: `training-video-web.mp4`
- Archive: `training-video-archive.mov`

## Directory Structure

```
automation/
├── assets/
│   ├── narration/          # 10 MP3 files (scene audio)
│   ├── overlays/           # PNG images (time-jumps, arrows, diagrams)
│   └── sound-effects/      # MP3 files (whoosh, ding, music)
└── output/
    ├── youtube/            # YouTube-optimized export
    ├── web/                # Web-optimized export
    └── master/             # Master + Archive files
```

## Quality Gates

Before finalizing video, verify:
- ✅ Duration: 3:50-4:00 minutes
- ✅ Resolution: 1920x1080
- ✅ Frame rate: 30 fps consistent
- ✅ Audio sync: No drift throughout
- ✅ Levels: -12 dB avg narration, no clipping
- ✅ Time-jumps: All 4 applied correctly
- ✅ Overlays: Visible and properly positioned
- ✅ Transitions: Smooth 0.3s crossfades
- ✅ Final size: Within expected ranges

## Success Metrics

After watching, users should be able to:
1. Understand why CLAUDE.md is important
2. Know how to download the framework
3. Know how to generate an agent system
4. Understand how agents work together
5. Execute their first /build command
6. Know where to find documentation

**Call to Action**: "Try it yourself in the next 5 minutes"

## Technical Dependencies

### Required Software
- Python 3.9+
- MoviePy 2.2.1+
- FFmpeg 4.0+
- Coqui TTS or ElevenLabs API
- PIL/Pillow for image generation

### Python Libraries
```python
moviepy>=2.2.1
pillow>=10.0.0
numpy>=1.24.0
pydub>=0.25.0
TTS>=0.22.0  # Coqui TTS
requests>=2.31.0
```

## Performance Benchmarks

### Expected Timings
- **Stage 1** (Parallel): 2-3 minutes
- **Stage 2** (Sequential): 5-7 minutes
- **Stage 3** (Parallel): 3-4 minutes
- **Total**: 12-15 minutes

### Resource Usage
- **CPU**: High during encoding (multi-core recommended)
- **Memory**: 2-4 GB peak
- **Disk**: 2 GB temporary, 1.5 GB final
- **Bandwidth**: ~50 MB if using cloud TTS

## Common Issues & Solutions

### Audio Sync Drift
- **Cause**: Frame rate mismatch
- **Fix**: Ensure all clips are 30 fps, use `fps=30` in exports

### Overlay Positioning
- **Cause**: Resolution mismatch
- **Fix**: Generate overlays at 1920x1080, use absolute positioning

### Export Too Large
- **Cause**: Bitrate too high
- **Fix**: Verify VBR settings, use 2-pass encoding

### Time-Jump Jarring
- **Cause**: Abrupt transition
- **Fix**: Ensure 0.2s fade in/out, add whoosh sound

## Version History

- **v1.0** (2025-10-03): Initial production specifications
- Framework: Claude Agent Framework v1.0
- Pattern: Parallel Multi-Stage Workflow

---

**Context Type**: Shared Knowledge Base
**Used By**: All video production agents
**Maintained By**: Video Compositor (orchestrator)
**Updated**: Per production cycle
