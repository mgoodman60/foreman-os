# Coding Conventions

**Analysis Date:** 2026-03-06

## Repository Context

This repository (`foreman-os`) is a **Claude Code plugin marketplace** containing 7 marketplace plugins and 4 dev-only plugins. It is NOT the Next.js application itself. The codebase consists of markdown files (skills, commands, agents), JSON configs, JavaScript hooks, and Python reference scripts. The actual ForemanOS Next.js application is a separate codebase, but its conventions are documented in the `plugins/` dev plugins.

This document covers **both** the conventions for this plugin repository and the ForemanOS application conventions as documented in the skill files.

---

## Plugin Repository Conventions

### File Types and Structure

**Markdown files (95% of codebase):**
- Commands: `<plugin>/commands/<name>.md` with YAML frontmatter (`description`, `allowed-tools`, `argument-hint`)
- Skills: `<plugin>/skills/<name>/SKILL.md` with YAML frontmatter (`name`, `description`, optional `version`)
- Agents: `<plugin>/agents/<name>.md` with YAML frontmatter (`name`, `description`)
- Reference docs: `<plugin>/skills/<name>/references/<topic>.md`

**JSON files:**
- Plugin manifests: `<plugin>/.claude-plugin/plugin.json` with `name`, `version`, `description`, `author`, `skills`
- Marketplace manifest: `.claude-plugin/marketplace.json`

**JavaScript hooks (4 files in `foremanos-intel/hooks/`):**
- Node.js scripts using CommonJS (`require()`)
- Shebang line: `#!/usr/bin/env node`
- `"use strict";` at top
- Read stdin JSON, process, write stdout JSON (pass-through pattern)
- Log to stderr with `[Hook]` prefix, never stdout
- Never block -- always pass through original input

**Python reference scripts:**
- Located in `foremanos-intel/skills/*/references/`
- Reference implementations, not directly executed by plugins
- Exception: `foremanos-intel/skills/dwg-extraction/scripts/` contains executable scripts

### Naming Patterns

**Plugin directories:**
- Pattern: `foremanos-<domain>` (e.g., `foremanos-core`, `foremanos-field`, `foremanos-intel`)
- Dev plugins: `plugins/foremanos-<concern>` (e.g., `plugins/foremanos-stack`, `plugins/foremanos-testing`)

**Skill directories:**
- Pattern: `kebab-case` (e.g., `project-data`, `daily-report-format`, `risk-management`)

**Command files:**
- Pattern: `kebab-case.md` (e.g., `daily-report.md`, `morning-brief.md`, `pay-app.md`)

**Agent files:**
- Pattern: `kebab-case.md` (e.g., `superintendent-assistant.md`, `doc-orchestrator.md`)

**Hook files:**
- Pattern: `kebab-case.js` (e.g., `data-loss-guard.js`, `counter-reconciler.js`)

### YAML Frontmatter Conventions

**Commands:**
```yaml
---
allowed-tools: Bash(npx vitest:*), Bash(node:*)
description: Short description of what this command does
argument-hint: optional hint for argument
---
```

**Skills:**
```yaml
---
name: skill-name
description: When to use this skill. Written as a directive.
version: 1.0.0  # optional
---
```

**Agents:**
```yaml
---
name: agent-name
description: What this agent does
---
```

### Skill Document Structure

Every SKILL.md follows this structure:
1. **When to Use This Skill** -- bullet list of trigger scenarios
2. **Core Patterns** -- numbered patterns with code examples
3. **Key Files** -- table of file paths and purposes
4. **Anti-Patterns** -- bullet list of what NOT to do
5. **Quick Reference** -- table or code block for fast lookup

### Cross-Plugin References

- Use `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md` for within-plugin references
- Use stub SKILL.md files (no `references/` folder) for cross-plugin skill access
- Every stub has header comment: `<!-- STUB: Canonical source is <plugin>/skills/<name>/SKILL.md -->`
- Never copy agents between plugins -- use soft refs or inlined methodology
- Run `sync-stubs.sh` after editing any canonical SKILL.md

### Hook Conventions (JavaScript)

Use this pattern for all Claude Code hooks:

```javascript
#!/usr/bin/env node
"use strict";

function warn(msg) {
  process.stderr.write(`[Hook] hook-name: ${msg}\n`);
}

function main() {
  let inputData = "";
  process.stdin.setEncoding("utf8");

  process.stdin.on("data", (chunk) => {
    inputData += chunk;
  });

  process.stdin.on("end", () => {
    let hookInput;
    try {
      hookInput = JSON.parse(inputData);
    } catch (_) {
      process.stdout.write(inputData);
      return;
    }

    // Process hook logic here...

    // Always pass through unchanged
    process.stdout.write(inputData);
  });
}

main();
```

---

## ForemanOS Application Conventions (from Dev Plugins)

The following conventions apply to the ForemanOS Next.js application, documented in `plugins/foremanos-stack/`, `plugins/foremanos-testing/`, `plugins/foremanos-llm/`, and `plugins/foremanos-documents/`.

### Naming Patterns

**Files:**
- Lib modules: `kebab-case.ts` (e.g., `lib/llm-providers.ts`, `lib/rate-limiter.ts`, `lib/db-helpers.ts`)
- React components: `kebab-case.tsx` (e.g., `lib/pdf-template.tsx`, `lib/room-pdf-generator.tsx`)
- API routes: `app/api/<path>/route.ts` (Next.js App Router convention)
- Config files: `kebab-case.config.ts` (e.g., `vitest.config.ts`, `trigger.config.ts`)
- Test files: `__tests__/<category>/<module>.test.ts`

**Functions:**
- camelCase for all functions (e.g., `callLLM`, `getFileUrl`, `checkRateLimit`, `uploadFile`)
- Factory functions: `create*` prefix (e.g., `createS3Client`, `createMockNextRequest`, `createScopedLogger`)
- Boolean getters: `is*` or `has*` prefix (e.g., `isRedisAvailable`, `hasDocumentAccess`, `isRestrictedQuery`)
- Async operations: descriptive verb (e.g., `fetchWithRetry`, `scanFileBuffer`, `processDocxTemplate`)

**Variables:**
- camelCase for all variables and parameters
- Constants: SCREAMING_SNAKE_CASE for model IDs and rate limits (e.g., `DEFAULT_MODEL`, `RATE_LIMITS`)
- Mock variables: `mock*` prefix (e.g., `mockSession`, `mockLogger`, `prismaMock`)

**Types/Interfaces:**
- PascalCase (e.g., `LLMMessage`, `LLMOptions`, `TemplateData`, `PhotoMeta`, `DailyReportData`)
- Prisma enums: PascalCase names, SCREAMING_SNAKE values (e.g., `ChangeOrderStatus.PENDING`)

### Import Organization

**Order:**
1. External framework imports (`react`, `next/server`, `vitest`)
2. External library imports (`@aws-sdk/client-s3`, `@react-pdf/renderer`, `pdf-lib`)
3. Internal imports using `@/` alias (`@/lib/db`, `@/lib/logger`, `@/lib/auth-options`)
4. Relative imports (test helpers, shared mocks)

**Path Aliases:**
- `@/` maps to project root (configured in `vitest.config.ts` and `tsconfig.json`)
- Always use `@/` for internal imports, never relative paths from source files

### Key Import Patterns

```typescript
// Database
import { prisma } from '@/lib/db';
import { withRetry } from '@/lib/db-helpers';
import { Prisma, ProcessingQueueStatus } from '@prisma/client';

// Auth
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth-options';
import { apiError, apiSuccess } from '@/lib/api-error';

// Logging
import { logger } from '@/lib/logger';             // Structured logger
import { createScopedLogger } from '@/lib/logger';  // Scoped logger

// LLM
import { callLLM, streamLLM } from '@/lib/llm-providers';
import { DEFAULT_MODEL, VISION_MODEL } from '@/lib/model-config';

// Redis
import { getCached, setCached, deleteCached } from '@/lib/redis';
import { checkRateLimit, RATE_LIMITS } from '@/lib/rate-limiter';

// File Storage
import { uploadFile, getFileUrl, downloadFile } from '@/lib/s3';
import { getBucketConfig, createS3Client } from '@/lib/aws-config';
```

### Error Handling

**API Routes -- always use try/catch:**
```typescript
export async function GET(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    if (!session?.user?.email) {
      return apiError('Unauthorized', 401, 'UNAUTHORIZED');
    }
    // ... business logic
    return apiSuccess({ data });
  } catch (error) {
    return apiError('Failed to fetch data', 500, 'INTERNAL_ERROR');
  }
}
```

**Error codes:** `UNAUTHORIZED`, `FORBIDDEN`, `NOT_FOUND`, `RATE_LIMITED`, `VALIDATION_ERROR`, `INTERNAL_ERROR`, `SERVICE_UNAVAILABLE`

**Prisma error classification:**
- Non-retryable: `P2025` (not found), `P2003` (FK constraint), `P2002` (unique constraint)
- Retryable: `P2024` (pool timeout), `P1001` (unreachable), `P1002` (timeout)

**Error sanitization in background tasks:**
```typescript
function sanitizeError(error: unknown): string {
  const message = error instanceof Error ? error.message : String(error);
  return message
    .replace(/sk-[a-zA-Z0-9]{20,}/g, '[REDACTED_KEY]')
    .replace(/key-[a-zA-Z0-9]{20,}/g, '[REDACTED_KEY]')
    .replace(/Bearer\s+[a-zA-Z0-9._-]+/g, 'Bearer [REDACTED]')
    .substring(0, 500);
}
```

**Graceful degradation pattern:**
- Redis: all operations return `null`/`false`/`0` when unavailable (never throws)
- Virus scanning: returns `{ clean: true }` when API key is missing
- S3: retry with backoff, reset client on auth errors

### Logging

**Framework:** Custom structured logger at `lib/logger.ts`

**Patterns:**
- Use `logger.info('SCOPE', 'message', { meta })` with a scope prefix
- Use `createScopedLogger('scope')` for module-level loggers
- In Trigger.dev tasks, use dual logging: `triggerLogger` (dashboard) + `logger` (application)
- Never use `console.log` in production code -- always use structured logger

**Logger signature:**
```typescript
createLogger()(message: string, error?: Error, meta?: object)
// NOT: createLogger(scope)(message)
```

### API Response Format

**Success:** `{ data: T }` via `apiSuccess()`
**Error:** `{ error: string, code: string }` via `apiError()`

### Client-Side Data Fetching

- Use vanilla `fetch` with `useEffect` + `useState` (no SWR, no React Query)
- Three state variables: `data`, `loading`, `error`
- Always check `response.ok` before parsing JSON
- Mutations: `fetch` with POST/PUT + `Content-Type: application/json`
- Long operations: `setInterval` polling with cleanup

### Singleton Patterns

- **Prisma:** Global singleton via `globalThis` in `lib/db.ts`
- **Redis:** Singleton via `ioredis` with lazy connect in `lib/redis.ts`
- **S3:** Cached singleton in `lib/s3.ts` with `resetS3Client()` for recovery
- Never create new client instances per request

### Database Conventions

- IDs: `@id @default(cuid())` -- always CUID strings, never autoincrement
- Timestamps: `createdAt DateTime @default(now())` + `updatedAt DateTime @updatedAt`
- All foreign keys must have `@@index`
- Cascade deletes for child records, `SetNull` for optional refs
- Always import Prisma from `@/lib/db`, never instantiate directly

### Module Design

**Exports:** Named exports preferred over default exports
**Barrel files:** Not used -- import directly from module path
**Service classes:** Factory methods (e.g., `OneDriveService.fromProject()`) over constructors

### Comments

- JSDoc not widely used -- rely on TypeScript types
- Inline comments for non-obvious logic
- `// TODO:`, `// FIXME:`, `// HACK:` for known issues

### Security Patterns

- Always call `getServerSession(authOptions)` in every API route (middleware is first-pass only)
- XSS sanitization via `sanitizeText()` for user text input
- Filename sanitization: `fileName.replace(/[^a-zA-Z0-9.-]/g, "_")`
- Error messages must never leak API keys -- use `sanitizeError()`
- Rate limiting on auth routes, chat, uploads, renders, and general API

---

*Convention analysis: 2026-03-06*
