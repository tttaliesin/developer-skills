# Developer skills

Locally maintained public skill adaptations for Codex and Pi, owned by `tools/`.
Workspace authority stays with workspace-rules; Vault operations stay with Second Brain.

| Priority | Package | Applied adaptation |
| --- | --- | --- |
| 1 | [systematic-debugging](skills/systematic-debugging/SKILL.md) | Credential-safe evidence, local test guidance, preserved fourth-fix discussion gate |
| 2 | [api-design-principles](skills/api-design-principles/SKILL.md) | HTTP and asynchronous producer-consumer contracts, execution outcomes, compatibility fixtures |
| 3 | [differential-review](skills/differential-review/SKILL.md) | Evidence-based severity, task-bound report persistence, self-contained analysis |
| 4 | [webapp-testing](skills/webapp-testing/SKILL.md) | Existing browser/test stack, bounded observable readiness, process ownership |

## Sources and changes

[upstream-lock.json](upstream-lock.json) pins repository, revision, source directory, license, and every preserved upstream file hash.
`upstream/` contains unchanged reference snapshots; they are evidence, not installed instructions or executable recommendations.
Each installed package includes its license and attribution notice.
There is no blanket relicensing: the differential-review adaptation remains CC BY-SA 4.0, while the other packages retain their respective MIT or Apache-2.0 terms.
See [changes.md](docs/changes.md) for the approved scope, retained approval gates, and helper exclusions.
Reviewable patches are under `patches/` and reconstruct the local packages from the pinned snapshots, excluding generated installation provenance.

## Validate and update

Run `python3 scripts/validate.py` to verify upstream hashes and byte-for-byte patch reconstruction.
Run skill-creator's `quick_validate.py` on each exact package and the workspace Markdown checker on changed documents.
See [validation.md](docs/validation.md) for behavioral evaluation and limitations.

For an upstream update, preserve the old lock/snapshot and inspect the new full package diff, including scripts, assets, references, licenses, and invocation policy.
Compare local patches with new upstream instructions before adapting them; never blindly reapply a patch over newer instructions.
Check existing global package bytes and preserve independently modified installed files before synchronization.
After committing the final package content, use workspace-rules `scripts/skill-provenance.py write skills/<name>` to record canonical path, base revision, and every package byte hash.
Commit the generated provenance separately; its base revision identifies the preceding content snapshot, not the later provenance-only commit.

## Install globally

From this repository, use the Skills CLI on each exact package path so upstream snapshots are never selected:

```bash
npx skills add ./skills/systematic-debugging --agent codex pi --global --yes
npx skills add ./skills/api-design-principles --agent codex pi --global --yes
npx skills add ./skills/differential-review --agent codex pi --global --yes
npx skills add ./skills/webapp-testing --agent codex pi --global --yes
```

Use the workspace provenance checker after installation for both agent paths.
Do not maintain global copies or symlinks manually.
Normal skill discovery does not grant tool permissions or authorize production operations.
