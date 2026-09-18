# World Insight Daily Workflow Contract

Apply this contract only when the user explicitly asks to start the
World Insight Daily Workflow and run the Phase 1 Manual Runner.

For all other repository work, including investigation, implementation,
testing, Git operations, explicitly approved diagnosis, and explicitly
approved reruns, do not apply the restrictions below unless the user
specifically instructs otherwise.

## Normal Daily Run

For a normal Daily Workflow start request:

1. Require a specific requested date in YYYY-MM-DD form. If no date is
   specified or reliably established by the user's instruction, do not
   start the Runner; ask for the date and stop.

2. Run exactly once:

   `python3 scripts/manual_runner.py --date YYYY-MM-DD`

3. Do not add `--human-approved-rerun` or any other recovery option.

4. Treat the Manual Runner itself as the normal execution interface.
   Do not reconstruct or independently verify its result by reading
   runtime artifacts.

5. If the Manual Runner produces a Human Gate 1 package for a
   `GATE1_READY` execution, present its complete stdout verbatim and
   stop at Human Gate 1. Do not add analysis, summary, or follow-on work.

6. If the Manual Runner does not produce a `GATE1_READY` Human Gate 1
   package, report the execution failure status available from the
   normal Runner result and stop. Do not inspect runtime artifacts to
   obtain additional detail.

7. Do not independently investigate, recover, rerun, or start any later
   workflow phase.

## Prohibited During a Normal Daily Run

Unless the user gives separate, explicit approval and instructions, do
not:

- inspect runtime artifacts independently
- read `status.json`, `validation_result.json`, `raw-output.txt`,
  `codex_result.json`, or other runtime files for diagnosis
- use `find`, `sed`, `cat`, or similar commands to investigate runtime
  artifacts
- rerun the validator independently
- rerun the Manual Runner
- use `--human-approved-rerun`
- diagnose or recover from a failure
- perform Source Verification
- use Firecrawl or web research
- generate an Article
- perform Editorial Review
- Build or Preview
- run Git add, commit, or push
- Publish
- update Memory

A normal Daily Workflow start request is not approval for diagnosis or
rerun.

Use `--human-approved-rerun` only when the user separately and
explicitly approves a rerun. Do not infer rerun approval from the
original Daily Workflow start request or from a failed run.

The user's current explicit instruction takes precedence over this
contract. Do not infer additional permission from context.
