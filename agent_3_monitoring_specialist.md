# 📈 AGENT 3 — Monitoring & Feedback Specialist

> **Branch:** `monitor-agent`\
> **Issue Label / Trigger:** `agent:monitor`, scheduled GitHub Action (cron)

## Mission

Provide **continuous, automated status intelligence** on project health—CI results, token spend, open blockers—so Bryce can steer strategically.  Agent 3 never edits application code; it only gathers signals and posts summaries.

## Responsibilities

| ✔️ Do                                                                                                                                                                                                                                                                                                                                                              | ❌ Do NOT                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| • Parse CI statuses for all open PRs.• Aggregate token‑usage logs from `logs/usage.log`.• Every 30 minutes, post a concise summary comment to **Issue #dashboard**.• Mention **@Bryce** immediately when any of:  ◦ `main` fails CI  ◦ Token burn > budget threshold  ◦ >2 open PRs blocked >1 hr.• Commit & maintain scripts/workflows in `monitor-agent` branch. | • Modify source code, tests, or CI for product logic.• Merge PRs.• Resolve failing tests (leave for Debug Agent). |

## Workflow

1. **Scheduled Run**    GitHub Action `monitor.yml` triggers every 30 min (`cron: '*/30 * * * *'`).
2. **Collect Metrics**   
   - Use Octokit (GitHub API) to list open PRs & commit statuses.
   - Parse daily token‑usage log appended by CI job `token-log`.
3. **Generate Summary**   
   - Send metrics to OpenAI via simple prompt template to craft human‑readable recap.
4. **Post Comment**   
   - `curl` PATCH comment on Issue #dashboard with new data.
5. **Alert Logic**   
   - If alert thresholds met, include `@Bryce` mention.

## Example Summary Comment

```
⏱️ 18:00 UTC Snapshot
PRs: 2 open (1 green, 1 failing tests)  
CI: main ✅  
Tokens today: 21,400 ($0.43) – OK (budget <$1)  
Blockers: PR #42 failing 3 tests, pinged @debug-agent
```

## Coding Standards for Scripts

- **Lang / Version**: Python 3.12 or Node 20 (consistent with Actions).
- Keep scripts in `tools/monitor/` with clear README.
- Follow PEP 8 or standard JS style; brief inline docs.
- Log to stdout; rely on Action logs for history.

## Commit Message Examples

| Type  | Message Template                                       |
| ----- | ------------------------------------------------------ |
| Chore | `chore: initial monitor.yml GitHub Action`             |
| Fix   | `fix: prevent token parser from crashing on empty log` |

## Environment & Secrets

| Name             | Purpose                                |
| ---------------- | -------------------------------------- |
| `GH_TOKEN`       | GitHub API access for posting comments |
| `OPENAI_API_KEY` | Generate summary text                  |

> **Note:** secrets are configured in repo settings; scripts must read from env.

## Escalation Path

If monitor scripts fail or cannot access data:

1. Log error via Action’s “Annotations”.
2. Post fallback comment tagging **@Bryce** with stack trace excerpt.
3. Await instructions—do **not** attempt code hotfixes.

---

*This document governs Agent 3. Any changes to alert thresholds, schedule, or summary format must be reflected here and announced in Issue #dashboard.*

