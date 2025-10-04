# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PingToPass** - AI-powered IT certification exam preparation platform using Makerkit Next.js + Supabase stack.

**Status**: Planning phase - product specification and system design documentation
**Target Stack**: Makerkit Next.js Supabase Turbo (chosen for speed, pre-built auth/billing/teams)
**Deployment**: Cloudflare Workers (not Vercel)

## Repository Purpose

This is a **planning/documentation repository** containing:
- Product system specifications
- User journey maps
- Feature requirements
- Mobile/gamification strategies

**No code exists yet** - this repo defines what will be built.

## Key Documentation Files

### productsystem.md
Complete product workflow from idea to shipping:
- 7-stage workflow (Idea → Stack Selection → Agent Validation → Spec → Issues → Build → Ship)
- Stack decision framework (Makerkit vs Laravel vs FastAPI)
- Auto-reject criteria (no native mobile, no blockchain, etc.)
- Time budgets: Idea to first commit = 4-6 hours
- Target: 1-2 weeks to MVP with Makerkit

**Important constraints:**
- Use Makerkit Next.js (never Next.js from scratch)
- Deploy to Cloudflare Workers (never Vercel)
- Use pgvector for AI features (no separate vector DB)
- Use Claude Code for validation/prototyping before building

### userjourney.md
Admin and student user flows for the certification platform:

**Admin Journey:**
1. Content hierarchy setup (Vendors → Certifications → Objectives with weights)
2. AI question generation (Exam Distribution or Single Objective modes)
3. Review/approve generated questions
4. Question bank management

**Student Journey:**
1. Browse and enroll in certifications
2. Practice mode with AI-generated questions (5 answers for MC, 2 for T/F)
3. Comprehensive explanations for all answers
4. Progress tracking and mastery scores

**Critical AI Generation Rules:**
- All Multiple Choice questions have exactly 5 answer options
- All True/False questions have exactly 2 answer options
- Every answer includes an explanation (why it's correct OR why it's incorrect)
- Questions distributed by objective weight percentages
- Quality scoring (1-5 stars) based on plausibility and educational value

### addons.md
Mobile-first experience and gamification strategy:

**Mobile Strategy:**
- PWA with offline support (not native apps)
- Bottom navigation pattern
- Touch-friendly UI (44px minimum tap targets)
- Swipe gestures for quiz navigation
- IndexedDB for offline question caching
- Background sync for progress

**Gamification System:**
- Badge categories: streak, mastery, milestone, speed, special
- Badge rarities: common, uncommon, rare, epic, legendary
- XP and leveling system (30 levels, titles from Beginner to Legend)
- Daily challenges (questions, mastery, speed goals)
- Streak tracking with fire/freeze mechanics

**Database additions needed:**
```sql
- badges table (name, category, rarity, criteria, points)
- user_badges (tracking earned badges)
- user_gamification (level, xp, streak, rank, title)
- daily_challenges (type, target, reward)
```

## Architecture Principles

**From productsystem.md workflow:**

1. **Validation First**: Use Claude Code agents to validate APIs/workflows before building production code
2. **Stack Constraints Drive Speed**: Only build what fits Makerkit/Laravel/FastAPI stacks (60-70% ideas rejected)
3. **AI-Assisted Spec Generation**: 30-60 min specs vs 8+ hours manual
4. **Issue-Driven Development**: GitHub issues with clear acceptance criteria for AI coding agents

**Tech Stack (Pre-approved):**
- Frontend: Makerkit Next.js (not custom Next.js)
- Database: Supabase Postgres with pgvector
- AI Features: OpenRouter API integration
- Deployment: Cloudflare Workers
- Mobile: PWA (no native apps)

## Product Features

**MVP Phase (Weeks 1-2):**
- Admin: Vendor/Cert/Objective management, AI question generation, review interface, basic analytics
- Student: Auth, browse certifications, practice mode, comprehensive explanations, basic progress tracking

**Phase 2:**
- Admin: Advanced filtering, quality monitoring, bulk operations, A/B testing
- Student: Simulation exam mode, objective-focused study, adaptive difficulty, spaced repetition

## Design Constraints

**Hard Constraints (Auto-reject):**
- ❌ Native mobile apps → Use PWA
- ❌ Desktop apps
- ❌ Video/audio processing
- ❌ Blockchain/Web3
- ❌ Gaming
- ❌ Deploy to Vercel → Must use Cloudflare Workers
- ❌ Separate vector DB → Use pgvector in Supabase

**Question Format Rules:**
- Multiple Choice: Always 5 answers, exactly 1 correct
- True/False: Always 2 answers, exactly 1 correct
- All answers require explanations
- Questions must be tied to objectives
- Difficulty levels: Beginner, Intermediate, Advanced

## When Building From These Specs

1. **Reference the full workflow**: Follow productsystem.md stages 1-7
2. **Validate with agents first**: Stage 4 - prototype uncertain integrations with Claude Code
3. **Generate GitHub issues**: Stage 6 format with clear acceptance criteria
4. **Mobile-first always**: Reference addons.md responsive breakpoints and PWA config
5. **Gamification integration**: Badge/XP checking should trigger after quiz completions, answers, and daily logins

## Related Projects

This is part of the **Entrepreneur Projects** category tracked in `/Users/bhunt/development/claude/CLAUDE.md`:
- **PingToPass Nuxt Migration** - Active migration to Nuxt.js + Cloudflare (check `/docs/` for status)
- **CertExamBuilder Prompt System** - FastAPI + MongoDB version (different stack)

Note: This `finalnextpass` repo may be a planning/spec repository distinct from the active Nuxt migration.
