# Codebase Concerns

**Analysis Date:** 2026-03-06

## Tech Debt

**Stub SKILL.md Files Reference Nonexistent `references/` Directories:**
- Issue: 9 stub SKILL.md files contain `references/` paths that point to files that do not exist in the stub's directory. The stubs are SKILL.md-only copies (by design), but the SKILL.md content references 20-30 reference files that only exist in the canonical source plugin.
- Files:
  - `foremanos-compliance/skills/delay-tracker/SKILL.md` (stub, no `references/` dir)
  - `foremanos-compliance/skills/document-intelligence/SKILL.md` (stub, 27 broken `references/` paths, only `conflict-detection-rules.md` exists locally)
  - `foremanos-cost/skills/estimating-intelligence/SKILL.md` (stub, no `references/` dir)
  - `foremanos-cost/skills/project-data/SKILL.md` (stub, no `references/` dir)
  - `foremanos-doccontrol/skills/document-intelligence/SKILL.md` (stub, 27 broken `references/` paths, no `references/` dir at all)
  - `foremanos-doccontrol/skills/project-data/SKILL.md` (stub, no `references/` dir)
  - `foremanos-field/skills/project-data/SKILL.md` (stub, no `references/` dir)
  - `foremanos-planning/skills/project-data/SKILL.md` (stub, no `references/` dir)
  - `foremanos-planning/skills/quantitative-intelligence/SKILL.md` (stub, no `references/` dir)
  - `foremanos-planning/skills/report-qa/SKILL.md` (stub, no `references/` dir)
- Impact: When the AI follows a stub's instructions to "Read `references/extraction-rules.md`", the file does not exist. This causes silent failures or hallucinated content. The `document-intelligence` stub is the worst offender -- it instructs reading 27 reference files that only exist in `foremanos-intel/skills/document-intelligence/references/`.
- Fix approach: Either (a) strip `references/` instructions from stub SKILL.md content via `sync-stubs.sh` preprocessing, or (b) add a "STUB NOTE" section at the top of each stub explicitly stating that reference paths resolve to the canonical plugin, not the local directory.

**Duplicate `parse_dxf.py` with Different Implementations:**
- Issue: Two different `parse_dxf.py` files exist with different purposes and implementations.
- Files:
  - `foremanos-intel/skills/document-intelligence/references/parse_dxf.py` -- Spatial extraction pipeline (blocks, hatches, polylines, dimensions)
  - `foremanos-intel/skills/dwg-extraction/scripts/parse_dxf.py` -- Civil 3D DXF entity parser (INSERT+ATTRIB+SEQEND sequences)
- Impact: Ambiguity about which script to use. The CLAUDE.md documentation describes the `dwg-extraction/scripts/` version as "executable" and the `document-intelligence/references/` version as "reference only", but their names are identical.
- Fix approach: Rename one to distinguish purpose (e.g., `parse_dxf_spatial.py` vs `parse_dxf_civil.py`), or consolidate into a single script with subcommands.

**Cross-Reference Pattern Files Duplicated Outside Stub System:**
- Issue: `cross-reference-patterns.md` is duplicated in 3 locations but is NOT managed by `sync-stubs.sh`. Currently identical, but drift is inevitable.
- Files:
  - `foremanos-core/skills/project-data/references/cross-reference-patterns.md` (canonical, 775 lines)
  - `foremanos-intel/skills/project-data/references/cross-reference-patterns.md` (copy, 775 lines)
  - `foremanos-compliance/skills/project-data/references/cross-reference-patterns.md` (copy, 775 lines)
- Impact: Manual edits to the canonical file will not propagate. The three copies will diverge silently.
- Fix approach: Add these to `sync-stubs.sh` reference sync, or remove the copies and have commands use soft refs to the canonical location.

**Plugin Version Inconsistency:**
- Issue: `foremanos-intel` is at version `6.0.0` while all other 6 marketplace plugins are at `5.0.0`.
- Files:
  - `foremanos-intel/.claude-plugin/plugin.json` -- version `6.0.0`
  - All other `*/.claude-plugin/plugin.json` -- version `5.0.0`
- Impact: Suggests intel was updated independently without bumping dependent plugins. Users may not know they need the latest intel plugin for features referenced by other plugins' stubs.
- Fix approach: Align version numbers or adopt semver-based compatibility ranges.

## Known Bugs

**Stub Sync Script Produces Extra YAML Delimiter:**
- Symptoms: Stubs gain an extra `---` line at the top after sync. The canonical SKILL.md starts with `---` (YAML frontmatter opener), and the stub header comment is prepended as a separate line, but the diff shows stubs have `0a1 > ---` -- an extra delimiter versus the canonical.
- Files: `sync-stubs.sh` (line 23-27, the `printf + cat` pattern)
- Trigger: Run `sync-stubs.sh` on any canonical SKILL.md that starts with `---`
- Workaround: The extra line is cosmetic and does not break YAML parsing in most contexts.

## Security Considerations

**Settings File Contains Stale Permission Entries:**
- Risk: `.claude/settings.local.json` contains overly broad `Bash` permissions and stale entries from past sessions (e.g., `Bash(done)`, incomplete multi-line commands stored as permissions).
- Files: `.claude/settings.local.json`
- Current mitigation: Local-only file, not committed to git.
- Recommendations: Audit and clean up permission entries. Remove stale/broken entries. Use more specific permission patterns.

**Python Virtual Environment and MCP Config Outside Repo:**
- Risk: `~/foreman-os-venv/` and `~/.claude/.mcp.json` are external dependencies that are not version-controlled.
- Files: `~/foreman-os-venv/` (Python venv), `~/.claude/.mcp.json` (MCP server config)
- Current mitigation: Documented in CLAUDE.md. Kept outside repo intentionally to avoid Cowork sandbox issues.
- Recommendations: Add a setup script or `Makefile` that bootstraps the venv. Document required MCP config in a template file (without secrets).

## Performance Bottlenecks

**Massive Token Load When All Plugins Installed:**
- Problem: The entire codebase is 855,612 words / 6.4 MB of markdown. When all 7 marketplace plugins plus 4 dev plugins are installed, the AI's context window must absorb a large skill surface.
- Files: All `*.md` files across all plugins (280 files total)
- Cause: Each plugin is self-contained with full SKILL.md files. Stubs duplicate entire SKILL.md content (1,000+ lines for `document-intelligence`). Reference files are large (top 10 files average 1,500 lines each).
- Improvement path:
  - Truncate stub SKILL.md files to only the frontmatter + description + data-source sections (remove deep methodology that is only needed by the canonical plugin's commands)
  - Split large reference files (>1,000 lines) into smaller, lazy-loaded chunks
  - Add `load_on_demand: true` metadata to reference files that should only be read when explicitly needed

**Plugin Size Imbalance:**
- Problem: `foremanos-field` (1.29 MB, 63 files) and `foremanos-intel` (1.48 MB, 50 files) are 2-3x larger than other plugins.
- Files: `foremanos-field/skills/field-reference/references/` (21 trade guides), `foremanos-intel/skills/document-intelligence/references/` (32 reference files)
- Cause: Field has 21 trade-specific guides (each 400-1,400 lines). Intel has 32 extraction templates.
- Improvement path: Move trade guides and extraction templates to a separate lazy-loading pattern where they are only read when the specific trade or document type is being processed.

## Fragile Areas

**Stub Sync Pipeline:**
- Files: `sync-stubs.sh`, all 13 stub SKILL.md files
- Why fragile: Manual process. If a developer edits a canonical SKILL.md and forgets to run `sync-stubs.sh`, stubs silently diverge. No CI/CD or pre-commit hook enforces sync.
- Safe modification: Always edit canonical sources, never stubs. Run `sync-stubs.sh` after every canonical edit.
- Test coverage: None. No automated verification that stubs match canonicals.

**Document-Intelligence Skill (Most Complex Single Skill):**
- Files: `foremanos-intel/skills/document-intelligence/SKILL.md` (1,084 lines), plus 32 reference files
- Why fragile: The 5-phase extraction pipeline spans 32 reference documents with intricate cross-dependencies. Changes to extraction-rules.md affect every deep-extraction reference. The SKILL.md references files by relative path, so any directory restructuring breaks all references.
- Safe modification: Read `foremanos-intel/skills/document-intelligence/references/extraction-rules.md` first to understand the framework before modifying any extraction template.
- Test coverage: None. No automated tests for extraction pipeline correctness.

**28-File JSON Data Store:**
- Files: 28 JSON files in user's `AI - Project Brain/` directory (listed in CLAUDE.md)
- Why fragile: No schema enforcement at write time (hooks only warn, never block). Cross-file references use string IDs with no foreign key validation. 20 downstream skills read from this store with hardcoded field paths.
- Safe modification: Use the `data-integrity-watchdog` agent or `/data-health scan` command before and after modifications. Always validate with the 4 hooks in `foremanos-intel/hooks/`.
- Test coverage: Hooks provide runtime validation only: `counter-reconciler.js` (array counts), `data-loss-guard.js` (array shrinkage), `project-brain-validator.js` (JSON validity + canonical keys), `extraction-checkpoint.js` (pre-compact state save). No unit tests for hooks.

## Scaling Limits

**Linear Stub Growth:**
- Current capacity: 7 skills synced to 13 stub locations
- Limit: Each new cross-plugin skill dependency adds N stub copies. At 20+ cross-plugin skills, the sync script becomes a maintenance burden and divergence risk grows.
- Scaling path: Replace stubs with a runtime skill resolution system where commands can reference skills by name (not path) and the platform resolves the canonical location.

**28-File Flat JSON Store:**
- Current capacity: Works for single-project scenarios with moderate document sets
- Limit: No indexing, no query optimization, no concurrent write safety. Large projects (500+ documents, 10,000+ data records) will cause slow reads and potential write conflicts.
- Scaling path: Migrate to SQLite or a lightweight embedded database. The `foremanos-stack/skills/prisma-patterns/SKILL.md` already documents Prisma patterns for the web app -- consider a parallel local-only store for the plugin system.

## Dependencies at Risk

**No Package Manager / No Dependency Tracking:**
- Risk: Python scripts reference external libraries (`ezdxf`, `fitz/PyMuPDF`, `reportlab`) but there is no `requirements.txt` or `pyproject.toml` in the repo. The venv at `~/foreman-os-venv/` is untracked.
- Impact: New developers or machines cannot reproduce the environment. Library version drift could break scripts.
- Migration plan: Add a `requirements.txt` or `pyproject.toml` with pinned versions. Document the venv setup in a bootstrap script.

**Cowork Platform Dependency:**
- Risk: Commands reference Cowork platform skills (`docx`, `pdf`, `construction-takeoff`) that are not part of this repo. If Cowork changes or removes these platform skills, commands break silently.
- Impact: Commands that generate DOCX/PDF output depend on external platform capabilities.
- Migration plan: Document which platform skills are required per command. Add graceful fallbacks in command instructions.

## Missing Critical Features

**No Automated Testing:**
- Problem: Zero test files exist. No test framework configured. No CI/CD pipeline.
- Blocks: Cannot verify that stub sync works, hooks function correctly, reference paths resolve, or Python scripts produce correct output.

**No Git Hooks or CI Enforcement:**
- Problem: No pre-commit hooks enforce stub sync, no CI validates markdown structure or YAML frontmatter.
- Blocks: Quality regressions go undetected until runtime.

**No Version Compatibility Matrix:**
- Problem: No documentation of which plugin versions are compatible with each other. The intel v6.0.0 / others v5.0.0 split is undocumented.
- Blocks: Users cannot determine safe upgrade paths.

## Test Coverage Gaps

**Hooks Have No Tests:**
- What's not tested: All 4 hooks in `foremanos-intel/hooks/` -- `counter-reconciler.js`, `data-loss-guard.js`, `extraction-checkpoint.js`, `project-brain-validator.js`
- Files: `foremanos-intel/hooks/*.js`
- Risk: Hook logic errors (false positives/negatives) go undetected. A bug in `data-loss-guard.js` could silently allow data loss.
- Priority: High

**Python Scripts Have No Tests:**
- What's not tested: All 7 Python scripts across intel and core plugins
- Files:
  - `foremanos-intel/skills/document-intelligence/references/parse_dxf.py`
  - `foremanos-intel/skills/document-intelligence/references/convert_dwg.py`
  - `foremanos-intel/skills/document-intelligence/references/visual_plan_analyzer.py`
  - `foremanos-intel/skills/dwg-extraction/scripts/parse_dxf.py`
  - `foremanos-intel/skills/quantitative-intelligence/references/calc_bridge.py`
  - `foremanos-intel/skills/quantitative-intelligence/references/sheet_xref.py`
  - `foremanos-core/skills/image-generation-mcp/references/server.py`
- Risk: DXF parsing, visual analysis, and calculation bridging could produce incorrect structured data that propagates through the entire 28-file data store.
- Priority: High

**Stub Sync Has No Verification:**
- What's not tested: `sync-stubs.sh` output correctness, stub-to-canonical equality
- Files: `sync-stubs.sh`
- Risk: Stubs silently diverge from canonicals. The extra `---` delimiter bug (documented above) is an example of undetected sync issues.
- Priority: Medium

**Command-to-Skill Path Resolution Not Validated:**
- What's not tested: Whether `${CLAUDE_PLUGIN_ROOT}/skills/<name>/SKILL.md` paths in commands actually resolve to existing files
- Files: All 40 command files across 7 plugins
- Risk: A renamed or moved skill breaks commands silently at runtime.
- Priority: Medium

---

*Concerns audit: 2026-03-06*
