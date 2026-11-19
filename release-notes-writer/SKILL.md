---
name: release-notes-writing
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

