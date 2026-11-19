# App Studio decisions

The durable agreement between learner and AI. Update only agreed decisions and
actual evidence; pending is a valid state. Keep explanations/help in
[LEARNING.md](LEARNING.md), not a second copy here.

## Current stage

- **Current feature:** APP-003.
- **Status:** APP-001 and APP-002 merged. APP-003 implemented locally; final learner evidence and full CI pending.
- **Next step:** Finish APP-003 learner review and full CI before merge.
- **Implementation marker:** `studio.json` declares `implemented_through: 2` after full cumulative CI passed.

This repository owns application code. Server/proxy changes and production
deployment are outside these three local-development lessons. Prepared helpers
are reusable foundations, not evidence that unfinished routes are implemented.

## APP-001 · Branded homepage

**Scope:** make the neutral FastAPI homepage express one chosen identity with
a simple original SVG mark, coherent copy, navigation and shared style tokens.
Keep account actions honest about their unfinished state.

| Decision | Agreement |
|---|---|
| Visitor and concrete use situation | Students juggling classes and work who need a clear starting point. |
| Reused IS117 brand, or name / promise / primary archetype | Student Assistant / A clearer next step for your school day / Sage, expressed as a helpful guide. AI-proposed purpose accepted by the learner. |
| One visible choice and visitor benefit | Professional navy-and-white style, clear headings and navigation to help busy students find their next step quickly. Visual details delegated to AI. |
| Own issue / branch / PR | [Issue #1](https://github.com/jakai211/IS373-App-Studio-studio2/issues/1) / `app-001-student-assistant` / [PR #2](https://github.com/jakai211/IS373-App-Studio-studio2/pull/2). |

**Keep when:** the agreed identity is visible and usable at desktop/narrow widths;
full foundation + APP-001 checks pass; AI review and the learner's actual check
interpretation/browser observation/keep reason are recorded; reviewed evidence
and verified GitHub state are linked below.

## APP-002 · Signup, login and logout

**Scope:** add browser forms and REST behavior for member signup, login, a private
dashboard and logout backed by SQLite. Reuse the prepared password/JWT/CSRF/session
helpers; keep data local. New accounts cannot choose their role.

| Decision | Agreement |
|---|---|
| Expected public/private behavior and account flow | Anonymous dashboard visits redirect to login. Successful login opens a private dashboard saying “Welcome, [username]” with a logout button. Logout removes access until login again. |
| Valid and rejected cases to demonstrate | Successful signup/login; wrong password shows an error and leaves the visitor logged out; dashboard access after logout requires login. |
| Own issue / branch / PR | [Issue #3](https://github.com/jakai211/IS373-App-Studio-studio2/issues/3) / `app-002-accounts` / [PR #4](https://github.com/jakai211/IS373-App-Studio-studio2/pull/4). |

**Keep when:** the agreed forms/API work; duplicate/invalid signup and wrong
credentials are rejected; passwords are hashed; authentication uses validated,
expiring JWTs with protected cookies and CSRF; private requests require a live
session and logout revokes it. Full cumulative checks, AI review, actual learner
contributions and GitHub state are recorded. This is not a production-security certification.

## APP-003 · Server-enforced roles

**Scope:** enforce a small member/admin boundary in the API and browser. Assign
roles only through the trusted local terminal command; use current server-side
permissions, including for an existing session after a role change.

| Visitor | Homepage | Member area | Admin area/API |
|---|---|---|---|
| Anonymous | Allowed | Login required | Login required |
| Member | Allowed | Allowed | Forbidden |
| Admin | Allowed | Allowed | Allowed |

| Decision | Agreement |
|---|---|
| Intended admin-only result | A simple protected admin page and API: anonymous visitors need login, members are denied, admins are allowed. Scope proposed by AI and approved by learner. Current database roles apply on every request; roles managed only through the prepared local CLI. |
| Actual allowed/denied request evidence | Prepared contracts: anonymous API 401/page redirect; member API/page 403; admin API/page 200; demotion to member denies the existing session again. All passed locally. |
| Own issue / branch / PR | [Issue #5](https://github.com/jakai211/IS373-App-Studio-studio2/issues/5) / `app-003-roles` / PR pending. |

**Keep when:** a direct request cannot bypass the role boundary, role changes
take effect as specified, new signup remains member-only, and full cumulative
checks plus AI review pass. Link the learner's actual interpretation/observation,
reviewed record and verified GitHub result. Hidden navigation alone is insufficient.

## Evidence

Link actual files/checks and the student's own issues/PRs. No fabricated URLs,
customer research or claims that a timestamp proves learning.

| Feature | Files / own issue / PR | Actual checks and learner observations | Kept / GitHub state |
|---|---|---|---|
| APP-001 | [Brand](app/brand.json), [homepage](app/templates/home.html), [shared layout](app/templates/base.html), [styles](app/static/student.css), [logo](app/static/logo.svg); [issue #1](https://github.com/jakai211/IS373-App-Studio-studio2/issues/1) | November 17: Black and Pylint passed; foundation 95 passed, 2 skipped, 1 Windows symlink-permission failure; APP-001 contracts 2 passed; Chromium 2 passed. AI reviewed desktop and 390px layout. Learner observation, interpretation, keep reason and publication approval recorded in LEARNING.md. Full local check failed; no pass claimed. | Learner chose keep; [APP-001 Linux and Windows CI passed](https://github.com/jakai211/IS373-App-Studio-studio2/actions/runs/44142077646). [Final main Linux and Windows checks passed](https://github.com/jakai211/IS373-App-Studio-studio2/actions/runs/44573659283); merged, issue closed. See [PR #2](https://github.com/jakai211/IS373-App-Studio-studio2/pull/2). |
| APP-002 | [Routes](app/features/accounts.py), [account form](app/templates/account.html), [dashboard](app/templates/dashboard.html), [additional checks](tests/test_account_routes.py); [issue #3](https://github.com/jakai211/IS373-App-Studio-studio2/issues/3), [PR #4](https://github.com/jakai211/IS373-App-Studio-studio2/pull/4) | November 19: Black and Pylint passed; foundation 95 passed, 2 skipped, 1 Windows symlink-permission failure; cumulative APP-001/002 contracts 14 passed; Chromium journeys 2 passed; additional route checks 3 passed separately. Full local run failed due to the symlink privilege error. AI browser trial: signup led to login, successful login showed personalized dashboard, logout followed by dashboard revisit redirected to login. Learner reported an incorrect-password error, confirmed dashboard/login redirects and chose keep for convenience; approved summary in LEARNING.md. | Learner keep/review approved; [full APP-002 Linux and Windows CI passed](https://github.com/jakai211/IS373-App-Studio-studio2/actions/runs/44577140344). [Final APP-002 PR checks passed](https://github.com/jakai211/IS373-App-Studio-studio2/actions/runs/44577958018); PR #4 merged and issue #3 closed. |
| APP-003 | [Routes](app/features/roles.py), [admin page](app/templates/admin.html), [denied page](app/templates/admin_denied.html); [issue #5](https://github.com/jakai211/IS373-App-Studio-studio2/issues/5), PR pending | November 19: Black/Pylint passed; 18 cumulative contracts and 2 Chromium journeys passed. Full local run failed on the Windows symlink privilege check (foundation: 98 passed, 2 skipped, 1 failed). AI browser review confirmed member denial, admin access after trusted CLI promotion, and denial after demotion in the same session. Desktop denial and narrow admin layouts reviewed. | Learner final evidence/review and full CI pending. |

The instructor's reference branches show possible implementations. They do not
establish this repository's completion or the learner's own reasoning.
