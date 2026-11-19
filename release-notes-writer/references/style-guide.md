# Release Notes Style Guide

Use this reference when drafting release notes to keep tone, categorization, and formatting consistent.

## Audience & Tone

- Write for end users and platform operators, not internal maintainers.
- Use active, past-tense verbs: "Added", "Fixed", "Improved", "Removed", "Deprecated".
- Keep each bullet to 1-2 sentences: state *what* changed and *why* it matters.

## Conventional Commits Mapping

Map commit prefixes to release note sections as follows:

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
