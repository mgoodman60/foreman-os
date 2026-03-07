# External Integrations

**Analysis Date:** 2026-03-06

## APIs & External Services

**LLM Providers (Multi-Provider with Prefix Routing):**
- **Anthropic (Claude)** - Primary LLM for complex queries, vision, extraction
  - SDK/Client: Anthropic SDK via `lib/llm-providers.ts`
  - Auth: `ANTHROPIC_API_KEY`
  - Models: `claude-sonnet-4-5-20250929` (default), `claude-opus-4-6` (premium/vision/extraction)
  - Endpoint: `api.anthropic.com/v1/messages`
  - Features: Streaming via `streamAnthropic()`, PDF document source, image source conversion
- **OpenAI (GPT/o-series)** - Fallback and simple queries
  - SDK/Client: OpenAI SDK via `lib/llm-providers.ts`
  - Auth: `OPENAI_API_KEY`
  - Models: `gpt-4o-mini` (simple/free), `gpt-5.2` (fallback)
  - Endpoint: `api.openai.com/v1/chat/completions`
  - Features: Streaming via `streamOpenAI()`, reasoning_effort for o3/o4 models
- **Google (Gemini)** - Vision pipeline for document extraction
  - SDK/Client: Google Generative AI SDK via `lib/llm-providers.ts`
  - Auth: `GOOGLE_API_KEY` (optional)
  - Models: `gemini-3-pro-preview` (pass 1), `gemini-2.5-pro` (pass 2)
  - Used in: Three-pass extraction pipeline (Gemini fast extract -> Gemini validate -> Opus interpret)

**Routing Logic:** Model prefix determines provider -- `claude-*` routes to Anthropic, everything else to OpenAI. All model constants centralized in `lib/model-config.ts`. Never hardcode model IDs.

**Image Generation (MCP Server):**
- **Flux 2 (Black Forest Labs)** - AI image generation
  - Client: `httpx` via `foremanos-core/skills/image-generation-mcp/references/server.py`
  - Auth: `FLUX2_API_KEY`
  - Endpoint: `https://api.bfl.ml/v1`
  - Features: Async polling (2s intervals, 120s timeout), 5 retries with exponential backoff
- **Google Gemini** - Alternative image generation
  - Auth: `GEMINI_API_KEY`
  - Endpoint: `https://generativelanguage.googleapis.com/v1beta`

**Payments:**
- **Stripe** - Payment processing and subscription management
  - SDK/Client: Stripe SDK
  - Auth: Stripe API keys (env vars)
  - Note: Webhook env var checks must be inside handler, not at module scope (build gotcha)

**Logging & Observability:**
- **Axiom** - Structured logging
  - SDK/Client: `@axiomhq/js` or similar via `lib/logger.ts`
  - Pattern: `createLogger()` with `(message, error?, meta?)` signature -- do NOT pass scope as first arg

**Virus Scanning:**
- **VirusTotal** - File upload scanning
  - Client: Native `fetch` via `lib/virus-scanner.ts`
  - Auth: `VIRUSTOTAL_API_KEY` (optional -- graceful degradation)
  - Endpoint: `https://www.virustotal.com/api/v3/files`
  - Features: Rate limit handling (429 returns clean), configurable timeout, polling for results

## Data Storage

**Databases:**
- **PostgreSQL (Neon Serverless)**
  - Connection: `DATABASE_URL` (pooled), `DIRECT_DATABASE_URL` (direct for migrations)
  - Client: Prisma 6.7 (`@prisma/client`)
  - Singleton: `lib/db.ts` using `globalThis` for hot-reload safety
  - Models: 124 models with CUID IDs, timestamps, soft deletes on some models
  - Binary targets: `["native", "debian-openssl-1.1.x"]`
  - Retry: `lib/db-helpers.ts` with `withRetry()` for connection errors (P2024, P1001, P1002, P1008, P1017)
  - Lazy construction: Skips `PrismaClient` when `DATABASE_URL` missing (Trigger.dev Docker indexing)

**File Storage:**
- **Cloudflare R2 (S3-Compatible)**
  - Client: `@aws-sdk/client-s3` singleton via `lib/s3.ts` and `lib/aws-config.ts`
  - Auth: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
  - Endpoint: `S3_ENDPOINT` (e.g., `https://<account-id>.r2.cloudflarestorage.com`)
  - Bucket: `AWS_BUCKET_NAME` (e.g., `foremanos-documents`)
  - Features: Presigned upload/download URLs, retry with timeout (120s default, 2 retries), auth error recovery via `resetS3Client()`
  - Config: `forcePathStyle: true` required for R2, `region: 'auto'`
  - Key files: `lib/aws-config.ts`, `lib/s3.ts`, `app/api/documents/presign/route.ts`

**Caching:**
- **Redis** (via `ioredis`)
  - Connection: `REDIS_URL`
  - Client: Singleton via `lib/redis.ts` (general ops) and `lib/redis-client.ts` (connection manager)
  - Config: `enableOfflineQueue: false`, `lazyConnect: true`
  - Features: JSON auto-serialization, pattern-based invalidation via SCAN, graceful null returns when unavailable
  - Specialized caches:
    - `lib/redis-cache-adapter.ts` - Structured cache with prefix namespacing, hit/miss stats
    - `lib/query-cache.ts` - LLM response cache with semantic similarity (Jaccard > 0.7), construction term normalization, dynamic TTL (48-72h)

## Authentication & Identity

**Auth Provider:**
- **NextAuth.js v5 (beta.30)** - Custom implementation
  - Config: `lib/auth-options.ts` (main), `auth.ts` + `auth.config.ts` (root), `lib/auth.ts` (`requireAuth()`)
  - Strategy: JWT-only (no session database adapter)
  - Provider: CredentialsProvider (username/email + password, case-insensitive)
  - Session: 30-day lifetime, 24-hour update interval
  - Login page: `/login`

**Role System (Three-tier):**
- `admin` - Full access to all documents and features
- `client` - Client + guest documents (no financial restrictions)
- `guest` - Guest documents only (plans, specs, schedule -- no budget/cost data)

**Guest PIN System:**
- Namespaced PINs: `{ownerId}_{pin}` in database
- Password-less login for `role === 'guest'` users
- Utilities: `lib/guest-pin-utils.ts` (`namespacePIN()`, `stripPINPrefix()`)

**Daily Report RBAC (Four-tier):**
- VIEWER / REPORTER / SUPERVISOR / ADMIN hierarchy
- State machine: DRAFT -> SUBMITTED -> APPROVED | REJECTED -> DRAFT
- Implementation: `lib/daily-report-permissions.ts`

**Middleware:**
- `middleware.ts` using `withAuth` from `next-auth/middleware`
- Protected: `/dashboard/*`, `/projects/*`, `/admin/*`, `/profile/*`, `/settings/*`, `/chat/*`, `/api/*`
- Public bypasses: `/api/auth/*`, `/api/webhooks/*`, `/api/cron/*`, `/api/documents/presigned-url`

**Access Control:**
- `lib/access-control.ts` - Document-level and query-level access checks
- `hasDocumentAccess(userLevel, documentName)` - Document access
- `isRestrictedQuery(query, userLevel)` - Budget/cost content restriction

## Rate Limiting

**Implementation:** Redis-based counters with in-memory fallback (`lib/rate-limiter.ts`)

**Predefined Limits:**
| Endpoint | Limit |
|----------|-------|
| Chat | 20 messages/minute |
| Upload | 10 uploads/minute |
| API | 60 requests/minute |
| Auth | 5 login attempts/5 minutes |
| Render | 5 renders/10 minutes |

**Utilities:** `checkRateLimit()`, `getRateLimitIdentifier()`, `getClientIp()`, `createRateLimitHeaders()`

## Background Jobs

**Trigger.dev v3:**
- Config: `trigger.config.ts` (project: `proj_gwelfqscrhdgtzzmqgxk`)
- Task directory: `src/trigger/`
- Max duration: 7200s (2 hours) for large document processing
- Retries: 3 attempts with exponential backoff (1-10s, factor 2, randomized)
- Prisma extension: `mode: "legacy"`, version `6.7.0`, no auto-migrate
- Primary use: Document processing pipeline exceeding Vercel serverless timeout

## Cloud Document Sync

**Microsoft OneDrive:**
- Client: Microsoft Graph API via `lib/onedrive-service.ts`
- Auth: OAuth2 with `ONEDRIVE_CLIENT_ID`, `ONEDRIVE_CLIENT_SECRET`, `ONEDRIVE_TENANT_ID`
- Tokens: Stored per-project in database (`oneDriveAccessToken`, `oneDriveRefreshToken`, `oneDriveTokenExpiry`)
- Features: Folder sync, file upload, per-project folder mapping (`oneDriveFolderId`)
- Auto-sync: Daily reports auto-uploaded to OneDrive on approval (`lib/daily-report-onedrive-sync.ts`)

**Photo Retention:**
- 7-day tiered retention with OneDrive archival (`lib/photo-retention-service.ts`)
- Metadata tracks `uploadedAt`, `expiresAt`, `onedriveSynced`, `fullResDeleted`
- Thumbnails generated with `-thumb` suffix key pattern

## Document Processing Pipeline

**Vision Pipeline (Three-Pass):**
1. Pass 1: Gemini 3 Pro Preview - Fast visual extraction (ThinkingLevel.LOW, 8192 tokens)
2. Pass 2: Gemini 2.5 Pro - Validates Pass 1, fills gaps (thinkingBudget: 1024)
3. Pass 3: Claude Opus 4.6 - Text-only validation, correction, enrichment (fallback: GPT-5.2)
4. Full fallback: Smart routing by document classification (visual/text-heavy/mixed)

**Single-Page Vision:**
- Round-robin load balancing between Claude Opus and GPT-5.2
- Quality score threshold >= 50, multi-provider fallback chain

**RAG System:**
- 9 query intent types with synonym expansion
- 1000+ point scoring system for relevance
- Three-pass retrieval (precision -> notes-first -> context)
- Project isolation enforced via `projectSlug` filtering

## CI/CD & Deployment

**Hosting:**
- **Vercel** - Next.js application hosting (serverless functions)
- **Trigger.dev** - Background job runner (Docker-based, separate infrastructure)

**CI Pipeline:**
- Build enforces zero type errors (`ignoreBuildErrors: false`)
- Build enforces zero lint errors (`ignoreDuringBuilds: false`)
- `prisma generate` runs as prebuild step

## Environment Configuration

**Required env vars:**
- `DATABASE_URL` - Neon PostgreSQL connection string
- `DIRECT_DATABASE_URL` - Direct Neon connection (for migrations)
- `NEXTAUTH_SECRET` - JWT signing secret
- `NEXTAUTH_URL` - Application URL
- At least one of `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`

**Optional env vars:**
- `REDIS_URL` - Redis (graceful fallback to in-memory)
- `GOOGLE_API_KEY` - Gemini vision pipeline
- `S3_ENDPOINT` / `AWS_*` vars - File storage
- `VIRUSTOTAL_API_KEY` - Upload scanning
- `ONEDRIVE_*` vars - Document sync
- `FLUX2_API_KEY` / `GEMINI_API_KEY` - MCP image generation
- Stripe API keys - Payments

**Secrets location:**
- `.env` file (local development, gitignored)
- Vercel environment variables (production)
- MCP server config at `~/.claude/.mcp.json` (user-level, outside repo)

## Webhooks & Callbacks

**Incoming:**
- `/api/webhooks/*` - Public (bypasses auth middleware), includes Stripe webhooks
- `/api/cron/*` - Public (bypasses auth middleware), scheduled tasks

**Outgoing:**
- OneDrive sync callbacks (OAuth2 token refresh)
- Trigger.dev task status callbacks
- LLM provider API calls (streaming responses)

## Plugin Data Store (28-File JSON System)

The plugin ecosystem operates on a 28-file JSON data store in the user's `AI - Project Brain/` folder. This is NOT a database -- it is file-based project intelligence consumed by all 7 plugins:

**Core files:** `project-config.json`, `plans-spatial.json`, `specs-quality.json`, `schedule.json`, `directory.json`
**Field files:** `daily-report-intake.json`, `daily-report-data.json`, `safety-log.json`, `inspection-log.json`, `labor-tracking.json`, `punch-list.json`
**Document files:** `rfi-log.json`, `submittal-log.json`, `drawing-log.json`, `annotation-log.json`
**Cost files:** `cost-data.json`, `change-order-log.json`, `delay-log.json`, `procurement-log.json`
**Quality files:** `quality-data.json`, `material-test-log.json`
**Other:** `visual-context.json`, `rendering-log.json`, `closeout-data.json`, `risk-register.json`, `claims-log.json`, `environmental-log.json`, `meeting-log.json`

Pipeline: Documents -> `document-intelligence` skill (5-phase extraction) -> JSON files -> consumed by commands/skills across all plugins.

---

*Integration audit: 2026-03-06*
