# Technology Stack

**Analysis Date:** 2026-03-06

## Repository Nature

This repository (`foreman-os`) is the **plugin marketplace** for ForemanOS -- it contains 7 Cowork plugins (markdown, JSON, shell scripts) and 4 Claude Code dev plugins. It is NOT the Next.js application codebase itself. However, the dev plugins in `plugins/` document the full application stack in detail, and this analysis synthesizes that information.

## Languages

**Primary:**
- Markdown (.md) - All commands, skills, agents, and documentation (95%+ of repo content)
- JSON - Plugin manifests and data schemas

**Secondary:**
- Bash - `sync-stubs.sh` for stub synchronization
- Python 3 - Reference scripts for DWG/DXF parsing, calculation bridging, MCP image generation server
- JavaScript - 4 hooks in `foremanos-intel/hooks/` (counter-reconciler, data-loss-guard, extraction-checkpoint, project-brain-validator)

**ForemanOS Application (documented in dev plugins):**
- TypeScript - Primary language for the Next.js app
- React/TSX - UI components (398+ client components documented)

## Runtime

**Environment:**
- Node.js (v25 compatibility noted in Vitest config `pool: 'forks'`)

**Package Manager:**
- npm (commands reference `npm run dev`, `npm test`, `npx prisma`)

**Python Virtual Environment:**
- Location: `~/foreman-os-venv/` (outside repo to avoid Cowork sandbox issues)

## Frameworks

**Core (ForemanOS App):**
- Next.js 15.5 - Full-stack React framework, App Router
- React 19.2 - UI library
- Prisma 6.7 - ORM with PostgreSQL (124 models per project CLAUDE.md, 112 per skill docs)
- next-auth v5 (beta.30) - Authentication with JWT strategy

**Testing:**
- Vitest - Unit/integration testing (`vitest.config.ts` with `pool: 'forks'`, jsdom environment)
- Playwright - E2E testing

**Build/Dev:**
- TypeScript with `strictNullChecks: true`
- `next.config.js` with `ignoreBuildErrors: false`, `ignoreDuringBuilds: false`

**Plugin System (This Repo):**
- Cowork plugin format - YAML frontmatter + markdown commands/skills/agents
- Claude Code plugin format - `plugin.json` manifests with skill/command auto-discovery

## Key Dependencies (ForemanOS App)

**Critical:**
- `@prisma/client` 6.7 - Database access (singleton at `lib/db.ts`)
- `next-auth` v5 beta.30 - Auth (JWT-only, CredentialsProvider)
- `ioredis` - Redis client for caching and rate limiting (`lib/redis.ts`)
- `@trigger.dev/sdk` v3 - Background job processing (`src/trigger/`)

**LLM Providers:**
- Anthropic SDK - Claude API access (`lib/llm-providers.ts`)
- OpenAI SDK - GPT/o-series API access (`lib/llm-providers.ts`)
- Google Generative AI - Gemini vision pipeline (`lib/llm-providers.ts`)

**File Storage:**
- `@aws-sdk/client-s3` - S3/Cloudflare R2 file operations (`lib/s3.ts`, `lib/aws-config.ts`)
- `@aws-sdk/s3-request-presigner` - Presigned URL generation

**Document Generation:**
- `@react-pdf/renderer` - PDF generation (`lib/pdf-template.tsx`)
- `pdf-lib` - PDF form filling (G702/G703, AIA documents)
- `docxtemplater` + `pizzip` - DOCX template processing
- `xlsx-populate` - XLSX template processing

**Infrastructure:**
- `@axiomhq/js` or Axiom integration - Structured logging (`lib/logger.ts`)
- Stripe SDK - Payment processing

## Configuration

**Environment:**
- `.env` file present (existence noted, contents not read)
- Key env vars documented across dev plugins:
  - `DATABASE_URL` / `DIRECT_DATABASE_URL` - Neon PostgreSQL
  - `REDIS_URL` - Redis connection
  - `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GOOGLE_API_KEY` - LLM providers
  - `S3_ENDPOINT` / `AWS_BUCKET_NAME` / `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` - File storage
  - `VIRUSTOTAL_API_KEY` - Virus scanning (optional)
  - `ONEDRIVE_CLIENT_ID` / `ONEDRIVE_CLIENT_SECRET` / `ONEDRIVE_TENANT_ID` - OneDrive sync
  - `FLUX2_API_KEY` / `GEMINI_API_KEY` - Image generation MCP server
  - `NEXTAUTH_SECRET` / `NEXTAUTH_URL` - Auth config

**Build:**
- `next.config.js` - Next.js config with strict error enforcement
- `tsconfig.json` - TypeScript config with `strictNullChecks: true`
- `vitest.config.ts` - Test runner config (jsdom, forks pool, 30s timeout)
- `trigger.config.ts` - Trigger.dev config (2hr max duration, 3 retries, Prisma extension)
- `prisma/schema.prisma` - Database schema (PostgreSQL, Neon serverless)

**MCP Servers:**
- `~/.claude/.mcp.json` - User-level MCP config (kept outside repo)
- Active: foreman-os image-gen (Flux 2 + Gemini + SVG), context7, github, figma, vercel, playwright

## Platform Requirements

**Development:**
- Node.js v25+ (inferred from Vitest forks pool requirement)
- Python 3 with PyMuPDF (`import fitz`) for PDF processing (pdftoppm not available on Windows)
- Git for version control
- Windows 11 (current dev environment) -- OneDrive paths require double-quoting

**Production:**
- Vercel - Deployment platform for the Next.js app
- Neon - Serverless PostgreSQL
- Cloudflare R2 - Object storage (S3-compatible)
- Redis - Caching and rate limiting
- Trigger.dev - Background job runner (Docker-based, separate from Vercel)

## Plugin Marketplace Structure

**7 Marketplace Plugins:** foremanos-core, foremanos-intel, foremanos-field, foremanos-planning, foremanos-doccontrol, foremanos-cost, foremanos-compliance

**4 Dev Plugins (Claude Code only, not in marketplace):**
- `plugins/foremanos-stack/` - Prisma, NextAuth, Redis, SWR, Trigger.dev patterns
- `plugins/foremanos-llm/` - LLM orchestration, vision, RAG, prompt patterns
- `plugins/foremanos-testing/` - Vitest, API route testing patterns
- `plugins/foremanos-documents/` - PDF gen, Office docs, R2 file storage patterns

**Totals:** 40 commands, 43 full skills, 13 stubs, 11 agents across marketplace plugins

---

*Stack analysis: 2026-03-06*
