# Testing Patterns

**Analysis Date:** 2026-03-06

## Repository Context

This repository (`foreman-os`) is a Claude Code plugin marketplace. It has **no tests, no build system, and no package manager**. The testing patterns documented here describe the **ForemanOS Next.js application** as captured in `plugins/foremanos-testing/skills/vitest-patterns/SKILL.md` and `plugins/foremanos-testing/skills/api-route-testing/SKILL.md`.

These patterns should be followed when writing tests for the ForemanOS application codebase.

---

## Test Framework

**Runner:**
- Vitest (version managed via `package.json` in the app repo)
- Config: `vitest.config.ts`

**Assertion Library:**
- Vitest built-in `expect` (Chai-compatible)

**E2E Framework:**
- Playwright (23 spec files, separate from Vitest)

**Run Commands:**
```bash
npm test -- --run              # Run all tests once
npm run test:watch             # Watch mode
npx vitest run --coverage      # Coverage report
npm test -- __tests__/api --run       # API tests only
npm test -- __tests__/lib --run       # Lib module tests only
npm test -- __tests__/smoke --run     # Smoke tests only
npx playwright test            # E2E tests
```

## Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    pool: 'forks',             // Required for Node.js v25 (NOT threads)
    include: ['__tests__/**/*.test.ts', '__tests__/**/*.test.tsx'],
    exclude: ['**/node_modules/**', '**/e2e/**'],
    testTimeout: 30000,        // 30s per test
    setupFiles: ['__tests__/setup.ts'],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
    },
  },
});
```

**Critical settings:**
- `pool: 'forks'` -- never use `'threads'` (Node.js v25 incompatibility)
- `environment: 'jsdom'` -- DOM APIs in all tests
- `@` alias maps to project root

## Test File Organization

**Location:** Separate `__tests__/` directory (not co-located)

**Naming:**
- Lib modules: `__tests__/lib/<module-name>.test.ts`
- API routes: `__tests__/api/<path>/route.test.ts`
- Smoke tests: `__tests__/smoke/<name>.test.ts`

**Structure:**
```
__tests__/
├── setup.ts                           # Global setup
├── helpers/
│   └── test-utils.ts                  # Mock factories, request helpers
├── mocks/
│   └── shared-mocks.ts               # Shared mocks (auth, Prisma, Stripe, S3)
├── lib/                               # 75+ lib module tests
│   ├── s3.test.ts
│   ├── rate-limiter.test.ts
│   └── ...
├── api/                               # API route tests
│   ├── signup/route.test.ts
│   ├── auth/
│   │   ├── verify-email.test.ts
│   │   ├── forgot-password.test.ts
│   │   └── reset-password.test.ts
│   ├── stripe/webhook.test.ts
│   └── projects/
│       ├── budget/route.test.ts
│       └── schedules/tasks.test.ts
├── smoke/                             # Smoke tests
e2e/                                   # Playwright E2E (separate, 23 specs)
```

## Test Structure

**Suite Organization:**
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

// 1. Hoisted mocks (MUST come first)
const mocks = vi.hoisted(() => ({
  prisma: {
    user: { findFirst: vi.fn(), create: vi.fn() },
  },
  logger: { info: vi.fn(), error: vi.fn(), warn: vi.fn() },
}));

// 2. Module mocks (reference hoisted values)
vi.mock('@/lib/db', () => ({ prisma: mocks.prisma }));
vi.mock('@/lib/logger', () => ({ logger: mocks.logger }));

// 3. Imports AFTER mocks
import { myFunction } from '@/lib/my-module';

// 4. Test suites
describe('myFunction', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Set defaults for happy path
  });

  it('should do something', () => {
    // Arrange
    mocks.prisma.user.findFirst.mockResolvedValue({ id: '1' });

    // Act
    const result = await myFunction();

    // Assert
    expect(result).toBeDefined();
  });
});
```

**Critical rule:** Always call `vi.clearAllMocks()` in `beforeEach`. Stale mock state causes flaky tests.

## Mocking

### Pattern 1: vi.hoisted() for Mocks Before Imports

Use `vi.hoisted()` when mock values are referenced in `vi.mock()` factory functions:

```typescript
const mockSend = vi.hoisted(() => vi.fn());
const MockS3Client = vi.hoisted(() => {
  return class S3Client {
    send = mockSend;
    config = { region: 'auto' };
    constructor() {}
  };
});

vi.mock('@aws-sdk/client-s3', () => ({
  S3Client: MockS3Client,
  PutObjectCommand: vi.fn().mockImplementation((input: any) => ({ input })),
}));
```

### Pattern 2: Grouped Hoisted Object

For complex test files, group all mocks into a single hoisted object:

```typescript
const mocks = vi.hoisted(() => ({
  prisma: {
    conversation: { findUnique: vi.fn(), update: vi.fn() },
    project: { findUnique: vi.fn() },
    document: { create: vi.fn() },
  },
  getFileUrl: vi.fn(),
  uploadFile: vi.fn(),
  createScopedLogger: vi.fn(() => ({
    info: vi.fn(), error: vi.fn(), warn: vi.fn(),
  })),
}));

vi.mock('@/lib/db', () => ({ prisma: mocks.prisma }));
vi.mock('@/lib/s3', () => ({
  getFileUrl: mocks.getFileUrl,
  uploadFile: mocks.uploadFile,
}));
vi.mock('@/lib/logger', () => ({
  createScopedLogger: mocks.createScopedLogger,
}));
```

### Pattern 3: Shared Mocks File

For tests sharing common mocks, import from `__tests__/mocks/shared-mocks.ts`:

```typescript
import {
  prismaMock,
  constructEventMock,
  subscriptionsRetrieveMock,
  headersMock,
  mockStripeSubscription,
} from '../../mocks/shared-mocks';
```

The shared mocks file pre-configures:
- NextAuth (`getServerSession`)
- Prisma (user, project, document, paymentHistory, markup models)
- Stripe (webhooks, subscriptions, checkout)
- S3 (upload, getFileUrl, download)
- Rate limiter, email service, audit log, logger
- Password validator, bcrypt, virus scanner

### Pattern 4: Dynamic Import for Route Handlers

API route tests MUST use dynamic import inside each test for fresh module instances:

```typescript
it('should return 401 when not authenticated', async () => {
  getServerSessionMock.mockResolvedValue(null);

  const { GET } = await import('@/app/api/projects/[slug]/budget/route');
  const request = new NextRequest('http://localhost/api/projects/test-project/budget');
  const response = await GET(request, { params: { slug: 'test-project' } });

  expect(response.status).toBe(401);
});
```

**What to Mock:**
- External services: Prisma, S3, Stripe, Redis, email
- Auth: `getServerSession`, `authOptions`
- Infrastructure: logger, rate limiter, virus scanner
- Third-party APIs: LLM providers, VirusTotal, OneDrive

**What NOT to Mock:**
- The module under test itself
- `NextRequest` / `NextResponse` (use real instances)
- Pure utility functions with no side effects
- Type definitions and interfaces

## Test Helpers and Factories

Located at `__tests__/helpers/test-utils.ts`:

```typescript
// Request factories
createMockNextRequest(method, body, headers, url)
createMockTextRequest(body, headers, url)        // Stripe webhooks
createMockFormDataRequest(formData, url)          // File uploads
createMockFile(content, name, type)

// Stripe mock factories
createMockStripeEvent(type, data, id)
createMockCheckoutSession(overrides)
createMockStripeSubscription(overrides)
createMockStripeInvoice(overrides)

// Prisma mock factories
createMockPrismaUser(overrides)
createMockPrismaDocument(overrides)

// Response parsing
extractResponseData(response)
```

## Standard Test Categories for API Routes

Every API route test MUST cover these categories:

1. **Authentication** -- 401 when not authenticated
2. **Authorization** -- 403 when wrong role/ownership
3. **Validation** -- 400 for missing/invalid input
4. **Not Found** -- 404 when resource doesn't exist
5. **Conflict** -- 409 for duplicate creation
6. **Happy Path** -- 200/201 with correct response shape
7. **Error Handling** -- 500 on database/service errors
8. **Rate Limiting** -- 429 when rate limit exceeded (auth routes)
9. **Side Effects** -- Verify email sent, audit logged, webhook processed

### Auth Test Pattern

```typescript
it('should return 401 when not authenticated', async () => {
  getServerSessionMock.mockResolvedValue(null);
  const { GET } = await import('@/app/api/projects/[slug]/budget/route');
  const request = new NextRequest('http://localhost/api/projects/test-project/budget');
  const response = await GET(request, { params: { slug: 'test-project' } });
  expect(response.status).toBe(401);
});
```

### Authorization Test Pattern

```typescript
it('should return 403 when user is not project owner or admin', async () => {
  prismaMock.project.findUnique.mockResolvedValue({
    ...mockProject,
    ownerId: 'different-user',
  });
  const { POST } = await import('@/app/api/projects/[slug]/budget/route');
  const request = new NextRequest('http://localhost/api/projects/test-project/budget', {
    method: 'POST',
    body: JSON.stringify({ totalBudget: 1000000 }),
    headers: { 'Content-Type': 'application/json' },
  });
  const response = await POST(request, { params: { slug: 'test-project' } });
  expect(response.status).toBe(403);
});
```

### Rate Limiting Test Pattern

```typescript
it('should return 429 when rate limit exceeded', async () => {
  checkRateLimitMock.mockResolvedValue({
    success: false, limit: 5, remaining: 0,
    reset: Math.floor(Date.now() / 1000) + 300,
    retryAfter: 300,
  });
  const { POST } = await import('@/app/api/signup/route');
  const request = new NextRequest('http://localhost/api/signup', {
    method: 'POST',
    body: JSON.stringify(validSignupData),
    headers: { 'Content-Type': 'application/json' },
  });
  const response = await POST(request);
  expect(response.status).toBe(429);
});
```

### Stripe Webhook Test Pattern

```typescript
function createWebhookRequest(body: string, signature?: string): NextRequest {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (signature) headers['stripe-signature'] = signature;
  return new NextRequest('http://localhost/api/stripe/webhook', {
    method: 'POST', body, headers,
  });
}

it('should update user subscription on checkout completed', async () => {
  headersMock.mockResolvedValue({
    get: vi.fn().mockReturnValue('valid_signature'),
  });
  const session = createMockCheckoutSession();
  const event = createMockStripeEvent('checkout.session.completed', session);
  constructEventMock.mockReturnValue(event);

  const request = createWebhookRequest(JSON.stringify(event));
  const response = await POST(request);

  expect(response.status).toBe(200);
  expect(prismaMock.user.update).toHaveBeenCalledWith(
    expect.objectContaining({
      where: { id: 'user-1' },
    })
  );
});
```

### Error Recovery Test Pattern

```typescript
it('should rollback user creation if Stripe checkout fails', async () => {
  checkoutSessionsCreateMock.mockRejectedValue(new Error('Stripe error'));
  const { POST } = await import('@/app/api/signup/route');
  // ... create request
  const response = await POST(request);
  expect(response.status).toBe(500);
  expect(prismaMock.user.delete).toHaveBeenCalled();
});
```

## Coverage

**Requirements:** Not formally enforced, but coverage priorities documented:

| Priority | Area | Examples |
|----------|------|---------|
| Critical (must test) | Auth, Stripe, rate limiting, document processing | `lib/auth-options.ts`, `app/api/stripe/webhook/route.ts` |
| High (should test) | API routes with mutations, budget/schedule services | `app/api/projects/*/route.ts` |
| Medium (nice to test) | Read-only API routes, utility modules | GET-only routes, pure helpers |
| Low (optional) | UI components, type definitions | React components, `.d.ts` files |

**View Coverage:**
```bash
npx vitest run --coverage
```

## Known Skipped Tests

- `fillPdfForm` tests -- skipped due to pdf-lib/Vitest Buffer incompatibility
- Upload tests -- skipped due to FormData Node.js environment limitation
- Vision API wrapper tests -- have retry delays (~6s each)

## Anti-Patterns

- **Never use `pool: 'threads'`** -- causes issues with Node.js v25. Always use `pool: 'forks'`
- **Never reference hoisted mocks before `vi.hoisted()`** -- the mock must be created inside the callback
- **Never import modules before `vi.mock()` calls** -- Vitest hoists `vi.mock()` but module imports must come after
- **Never skip `vi.clearAllMocks()` in `beforeEach`** -- stale mock state causes flaky tests
- **Never mock `@prisma/client` directly** -- mock `@/lib/db` instead: `vi.mock('@/lib/db', () => ({ prisma: prismaMock }))`
- **Never use `describe.skip` casually** -- only skip with documented compatibility issues
- **Never test route handlers without `await import()`** -- always dynamically import for fresh instances
- **Never mock `next-auth` without also mocking `@/lib/auth-options`** -- routes import auth options
- **Never use `new Request()` for API route tests** -- use `new NextRequest()` (Next.js-specific properties)
- **Never hardcode timestamps in assertions** -- use `expect.any(Date)` or `expect.any(String)`
- **Never test Prisma calls without `expect.objectContaining`** -- Prisma calls include timestamps and generated fields

## Quick Reference

| Task | Command |
|------|---------|
| Run all tests | `npm test -- --run` |
| Run specific file | `npm test -- __tests__/lib/s3.test.ts --run` |
| Run tests matching pattern | `npm test -- --run -t "should upload file"` |
| Run API tests | `npm test -- __tests__/api --run` |
| Run auth tests | `npm test -- __tests__/api/auth --run` |
| Run Stripe tests | `npm test -- __tests__/api/stripe --run` |
| Run smoke tests | `npm test -- __tests__/smoke --run` |
| Coverage | `npx vitest run --coverage` |
| Watch mode | `npm run test:watch` |
| E2E tests | `npx playwright test` |

---

*Testing analysis: 2026-03-06*
