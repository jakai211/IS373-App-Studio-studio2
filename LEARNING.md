# Conversation evidence

AI-drafted task summary, not a transcript or grade. It may be public. Use actual
short words or labeled paraphrases; disclose help and leave missing responses
pending. The learner reviews, corrects or removes new excerpts before commit/push.
Accuracy approval is not proof of understanding. Label simulated trials explicitly.

**Available conversation context:** App Studio setup and APP-001 choices in this chat on November 10, 2026. Earlier setup notes retained; the November 17 continuation supplies the reviewed APP-001 observation, interpretation and keep decision below.

## APP-001

- Prediction: Learner wrote, "if its organized they can quickly navigate" in response to how a clear professional layout could help a busy student.
- Check interpretation: The learner said the starting-point button check would catch "that the starting button is broken".
- Browser observation: Reviewed paraphrase: the button takes the learner straight to the starting point, helping when they need to be somewhere.
- Keep decision: "i would keep it because i like ease of access".
- Review: On November 17 the learner answered "yes" when asked whether the observation, keep decision, check interpretation and AI-help summary were accurate and okay to publish.
- Help/gaps: Learner chose Student Assistant and a professional style, accepted the coach's student audience/promise, and delegated visual creativity. AI handled setup and implementation. AI ran checks and prompted the learner explanation. The new observation, keep decision, interpretation and help summary were reviewed before publication. Earlier setup and prediction are retained from the existing local record; this continuation did not independently recover that conversation.
- Evidence links / next step: [Issue #1](https://github.com/jakai211/IS373-App-Studio-studio2/issues/1). See SPEC.md for checks and PR evidence; [PR #2](https://github.com/jakai211/IS373-App-Studio-studio2/pull/2) merged and issue closed.

## APP-002

- Prediction: Reviewed paraphrase of agreed behavior: Before login, dashboard visits should go to login. Successful login should allow the private dashboard. A wrong password should show an error and leave the visitor logged out. After logout, the dashboard should require login again. The learner chose a simple “Welcome, [username]” dashboard with a logout button.
- Check interpretation: Reviewed paraphrase: If access still worked after logout, other people could get into the private dashboard. Learner wrote, "if they could still get in then others can".
- Browser observation: Reviewed paraphrase: A wrong password showed an incorrect-password error. The learner answered yes when asked whether correct login showed the welcome dashboard and revisiting the dashboard after logout returned to login.
- Keep decision: The learner would not change the flow because "its convient" (convenient).
- Review: On November 19 the learner approved the observation, interpretation, keep reason and AI-help summary for publication.
- Help/gaps: AI implemented the account routes and forms using the prepared security helpers, ran automated checks and a separate AI browser trial. The full local run encountered a Windows symbolic-link privilege failure; feature checks passed. Learner observations, interpretation and keep reason were supplied; the learner approved the summary for publication.
- Evidence links / next step: See SPEC.md for actual local evidence. [Issue #3](https://github.com/jakai211/IS373-App-Studio-studio2/issues/3) is open. [PR #4](https://github.com/jakai211/IS373-App-Studio-studio2/pull/4); full APP-002 CI passed. [Final PR checks passed](https://github.com/jakai211/IS373-App-Studio-studio2/actions/runs/44577958018); PR #4 merged and issue #3 closed.

## APP-003

- Prediction: Reviewed paraphrase: a member typing the admin API address should be asked for a password.
- Check interpretation: Reviewed paraphrase: members should be blocked because they are not admins; knowing a leaked address should not grant access.
- Browser observation: Pending. The learner has not supplied an actual admin-page observation.
- Keep decision: The learner chose keep because members are not admins and knowing the address should not grant access.
- Review: On November 19 the learner approved this summary, including the missing browser observation, and authorized publication and completion.
- Help/gaps: AI proposed the small permission matrix, which the learner accepted, and explained login versus permission. AI built and tested the boundary with prepared helpers and performed a separate browser trial. The learner supplied an interpretation and keep reason after prompting. The learner browser observation remains pending; the approved summary preserves that gap.
- Evidence links / next step: [Issue #5](https://github.com/jakai211/IS373-App-Studio-studio2/issues/5). [PR #6](https://github.com/jakai211/IS373-App-Studio-studio2/pull/6); full CI pending.
