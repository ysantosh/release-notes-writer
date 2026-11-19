# Creating AI Skills for Gemini

A practical guide and teaching reference for building reusable AI skills in Gemini using the **Open Agent Skills Standard**, complete with a multi-file example (`release-notes-writing-pro`).

---

## Table of Contents

1. [Three Ways to Create Skills for Gemini](#three-ways-to-create-skills-for-gemini)
2. [Anatomy of an Agent Skill (Open Standard)](#anatomy-of-an-agent-skill-open-standard)
3. [Multi-File Teaching Example: `release-notes-writing-pro`](#multi-file-teaching-example-release-notes-writing-pro)
   - [`SKILL.md`](#1-skillmd)
   - [`references/style-guide.md`](#2-referencesstyle-guidemd)
   - [`scripts/extract_commits.py`](#3-scriptsextract_commitspy)
   - [`assets/release-template.md`](#4-assetsrelease-templatemd)
4. [Testing the Skill (Sample Input & Output)](#testing-the-skill-sample-input--output)
5. [Managing Your Skills in Chat](#managing-your-skills-in-chat)
6. [Best Practices](#best-practices)

---

## Three Ways to Create Skills for Gemini

Depending on your workflow, there are three main ways to build reusable capabilities for Gemini:

### 1. Reusable Agent Skills (Directly in Chat)
Best for recurring, multi-step workflows where consistency matters (e.g., drafting release notes, reviewing code against team standards, generating structured configs).
- Defined by a `SKILL.md` file with YAML frontmatter and concise Markdown instructions.
- Can be created, tested, and saved directly in a Gemini conversation.

### 2. Custom Gems (Gemini Web App)
Best for dedicated AI assistants with a persistent persona and attached reference documents.
1. Open **gemini.google.com**, go to **Gems** in the left sidebar, and click **New Gem**.
2. Name and describe your Gem.
3. Write instructions covering four pillars: **Persona**, **Task**, **Context**, and **Format**.
4. *(Optional)* Upload reference files under **Knowledge** (from your device, Google Drive, or a Gemini Notebook).
5. Test in the preview pane and click **Save**.

### 3. Developer Skills & Gemini CLI Extensions
Best for engineering workflows, IDEs, and terminal agents.
- **Coding Agent Skills:** Package a folder with `SKILL.md`, `references/`, `scripts/`, and `assets/` using the Open Agent Skills Standard (compatible with Antigravity, Cursor, Claude Code, Codex, etc.). You can install official Gemini API skills via:
  ```bash
  npx skills add google-gemini/gemini-skills --skill gemini-api-dev --global
  ```
- **Gemini CLI Extensions (MCP):** Scaffold executable Model Context Protocol (MCP) tools with:
  ```bash
  gemini extensions new my-first-extension mcp-server
  ```

---

## Anatomy of an Agent Skill (Open Standard)

Under the **Open Agent Skills Specification**, a skill is a self-contained directory centered on a `SKILL.md` file. This design enables **progressive disclosure**: the AI scans only lightweight metadata at startup and loads full instructions or supporting files only when the skill is triggered.

```text
release-notes-writing-pro/
├── SKILL.md                      # Required: metadata + core instructions
├── references/                   # Optional: style guides, rubrics, domain docs
│   └── style-guide.md
├── scripts/                      # Optional: deterministic helper scripts
│   └── extract_commits.py
└── assets/                       # Optional: static output templates or schemas
    └── release-template.md
```

### Key Components

| Component | Purpose | Teaching Tip |
| :--- | :--- | :--- |
| **YAML Frontmatter** | Contains `name` (lowercase alphanumeric + hyphens, 1–64 chars, matching the folder name) and `description`. | The `description` is the **primary trigger**. State both *what* the skill does and *when* to activate it. |
| **Markdown Body** | Loaded only after activation. Includes `When to Use`, `Resources`, `Steps`, and `Gotchas`. | Keep it concise (under 500 lines) and use imperative instructions. |
| **`references/`** | Domain knowledge, lookup tables, and style rules. | Prevents bloating `SKILL.md`; the agent reads these on demand. |
| **`scripts/`** | Deterministic executable code (Python, Bash, etc.). | Offload repetitive parsing or filtering to code instead of relying on the LLM. |
| **`assets/`** | Reusable templates, boilerplate files, or schemas. | Gives the agent a fixed layout with placeholders to fill in consistently. |

---

## Multi-File Teaching Example: `release-notes-writing-pro`

This example demonstrates how a multi-file skill drafts user-facing release notes from merged pull requests and git commit history.

### 1. `SKILL.md`
Links the supporting resources and defines the step-by-step workflow and guardrails.

```markdown
---
name: release-notes-writing-pro
description: Drafts clear, user-facing release notes and changelog entries from merged pull requests and git commit history. Use when the user asks for release notes, a changelog entry, a release summary, or what changed between two versions or git tags.
---

# Release Notes Writing

Draft concise, user-facing release notes and changelog entries from merged pull requests, commit logs, or version diffs.

## When to Use

- The user asks to draft release notes for an upcoming or completed release.
- The user wants a changelog entry formatted from git commits or merged PRs.
- The user asks what changed between two versions, branches, or git tags.

## Resources

- **Style Guide:** Read `references/style-guide.md` for tone, Conventional Commits mapping, and formatting rules.
- **Output Template:** Use `assets/release-template.md` as the structural skeleton for the final release notes.
- **Helper Script:** Provide or run `scripts/extract_commits.py <from_tag> <to_tag>` when the user wants to pre-filter and group a local git repository's commit log before drafting.

## Steps

1. **Filter the raw history.** Review the provided commits and PRs using the mapping in `references/style-guide.md`. Exclude internal noise such as merge commits, typo fixes in internal comments, code formatting, or CI-only tweaks unless they directly affect users or contributors.
2. **Group by impact category.** Organize meaningful changes into standard sections in this priority order (omit empty sections):
   - **Breaking Changes:** Changes that require user action, config updates, or code migrations.
   - **New Features:** Net-new capabilities or endpoints.
   - **Improvements:** Performance gains, UX enhancements, or non-breaking refinements.
   - **Bug Fixes:** Resolved defects and stability fixes.
   - **Security & Deprecations:** Vulnerability patches or features scheduled for removal.
3. **Translate technical diffs into user value.** Rewrite commit titles to explain what changed for the user and why it matters, rather than copying internal implementation details verbatim. Preserve PR or issue references (for example, `(#142)`) at the end of each bullet when available.
4. **Add migration guidance.** For every item under **Breaking Changes**, include a brief before-and-after note or explicit upgrade step.
5. **Format the final output.** Follow the layout in `assets/release-template.md`, replacing placeholders with the version number, release date (if provided), and scannable bullet points starting with strong action verbs.

## Gotchas

- Do not paste raw `git log` output verbatim. Always synthesize related commits into a single cohesive bullet point.
- Never bury breaking changes at the bottom of the notes. Always place them first so users see upgrade risks immediately.
- If the user provides only commit hashes or vague titles without context, draft the best possible notes and explicitly flag ambiguous items that need clarification before publishing.
```

### 2. `references/style-guide.md`
Defines audience, tone, Conventional Commits mapping, and formatting conventions.

```markdown
# Release Notes Style Guide

Use this reference when drafting release notes to keep tone, categorization, and formatting consistent.

## Audience & Tone

- Write for end users and platform operators, not internal maintainers.
- Use active, past-tense verbs: "Added", "Fixed", "Improved", "Removed", "Deprecated".
- Keep each bullet to 1-2 sentences: state *what* changed and *why* it matters.

## Conventional Commits Mapping

| Commit Prefix | Release Note Section |
| --- | --- |
| `feat!:` / `BREAKING CHANGE:` | Breaking Changes |
| `feat:` | New Features |
| `perf:` / `refactor:` (user-visible) | Improvements |
| `fix:` | Bug Fixes |
| `security:` / `deprecate:` | Security & Deprecations |
| `chore:` / `ci:` / `style:` / `test:` / `docs:` (internal) | Omit from release notes |

## Formatting Rules

- Always preserve PR or issue numbers in parentheses at the end of the bullet: `(#412)`.
- Wrap config keys, CLI flags, and file paths in backticks.
- Group multiple commits for the same feature into one unified bullet point.
```

### 3. `scripts/extract_commits.py`
Pre-filters noise and groups git commits between two tags deterministically before the AI drafts the prose.

```python
#!/usr/bin/env python3
"""Extract and group git commits between two refs for release notes drafting.

Usage:
    python3 scripts/extract_commits.py v2.3.0 v2.4.0
"""

import re
import subprocess
import sys
from collections import defaultdict

CATEGORY_MAP = {
    "breaking": "Breaking Changes",
    "feat": "New Features",
    "perf": "Improvements",
    "fix": "Bug Fixes",
    "security": "Security & Deprecations",
}

NOISE_PREFIXES = ("chore", "ci", "style", "test", "build")


def get_commits(from_ref: str, to_ref: str) -> list[str]:
    cmd = ["git", "log", f"{from_ref}..{to_ref}", "--pretty=format:%h %s", "--no-merges"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return [line for line in result.stdout.splitlines() if line.strip()]


def categorize(commits: list[str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    pattern = re.compile(r"^([a-f0-9]+)\s+([a-z]+)(\([^)]+\))?(!)?:\s*(.+)$")

    for line in commits:
        match = pattern.match(line)
        if not match:
            grouped["Uncategorized"].append(line)
            continue

        _, prefix, _, bang, _ = match.groups()
        if bang:
            grouped[CATEGORY_MAP["breaking"]].append(line)
        elif prefix in NOISE_PREFIXES:
            continue
        elif prefix in CATEGORY_MAP:
            grouped[CATEGORY_MAP[prefix]].append(line)
        else:
            grouped["Uncategorized"].append(line)

    return grouped


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/extract_commits.py <from_tag> <to_tag>", file=sys.stderr)
        sys.exit(1)

    commits = get_commits(sys.argv[1], sys.argv[2])
    grouped = categorize(commits)

    for section, items in grouped.items():
        print(f"## {section}")
        for item in items:
            print(f"- {item}")
        print()


if __name__ == "__main__":
    main()
```

### 4. `assets/release-template.md`
Provides a consistent structural skeleton with placeholders.

```markdown
## Release {{VERSION}} ({{RELEASE_DATE}})

> **Summary:** {{ONE_SENTENCE_HIGHLIGHT}}

### Breaking Changes
- **{{CHANGE_TITLE}}:** {{USER_IMPACT}} ({{PR_NUMBER}})
  - *Migration:* {{UPGRADE_STEP_OR_BEFORE_AFTER}}

### New Features
- **{{FEATURE_TITLE}}:** {{USER_VALUE}} ({{PR_NUMBER}})

### Improvements
- **{{IMPROVEMENT_TITLE}}:** {{USER_BENEFIT}} ({{PR_NUMBER}})

### Bug Fixes
- **{{FIX_TITLE}}:** {{RESOLVED_ISSUE}} ({{PR_NUMBER}})

### Security & Deprecations
- **{{SECURITY_OR_DEPRECATION_TITLE}}:** {{ACTION_OR_PATCH_DETAILS}} ({{PR_NUMBER}})
```

---

## Testing the Skill (Sample Input & Output)

### Sample Input (`v2.3.0..v2.4.0`)

```text
a1b2c3d feat!: replace `log_retention_days` config key with `retention_policy.days` (#412)
e4f5g6h Merge branch 'main' into feat/arm-indexing
i7j8k9l feat: add native OTLP gRPC ingestion endpoint (#418)
m1n2o3p perf: optimize inverted index compression for ARM64 nodes (#421)
q4r5s6t style: run rustfmt across storage crate (#422)
u7v8w9x fix: prevent OOM crash when querying empty time ranges (#425)
y1z2a3b ci: bump actions/checkout to v4 (#426)
c4d5e6f security: patch JWT signature validation bypass in API gateway (#429)
g7h8i9j fix: update parser logic (#431)
```

### Generated Output

> ## Release v2.4.0 (2026-11-19)
>
> ### Breaking Changes
> - **Renamed log retention configuration key:** Replaced `log_retention_days` with `retention_policy.days` to support granular retention rules (#412).
>   - *Migration:* Update your configuration file before upgrading (`log_retention_days: 30` -> `retention_policy.days: 30`).
>
> ### New Features
> - **Added native OTLP gRPC ingestion:** You can now stream telemetry directly over OTLP gRPC without an intermediate collector (#418).
>
> ### Improvements
> - **Improved ARM64 indexing performance:** Optimized inverted index compression on ARM64 nodes, reducing memory overhead and speeding up log ingestion (#421).
>
> ### Bug Fixes
> - **Fixed crash on empty time-range queries:** Resolved an out-of-memory (OOM) crash triggered when running queries against time windows with no matching data (#425).
>
> ### Security & Deprecations
> - **Patched JWT signature validation:** Fixed an authentication bypass vulnerability in the API gateway's JWT verification logic (#429).
>
> ### Needs Clarification Before Publishing
> - **`g7h8i9j` (`fix: update parser logic`, #431):** Too vague to describe user-facing impact; confirm before publishing.
>
> *(Filtered out internal noise: merge commit `e4f5g6h`, formatting change `#422`, and CI bump `#426`.)*

---

## Managing Your Skills in Chat

- **View a skill's contents:** Ask *"Show the contents of my `release-notes-writing-pro` skill."*
- **List all saved skills:** Ask *"List my skills."*
- **Invoke explicitly:** Ask *"Use `release-notes-writing-pro` to draft release notes for v3.0.0 from these commits."*

---

## Best Practices

1. **Start simple, scale when needed:** A single `SKILL.md` is enough for lightweight workflows. Add `references/`, `scripts/`, and `assets/` once you need strict templates, style guides, or deterministic parsing.
2. **Make descriptions trigger-friendly:** Include the exact user intents and phrases that should activate the skill.
3. **Include a `Gotchas` section:** Explicitly calling out common failure modes (like dumping raw logs or burying breaking changes) dramatically improves output quality.