# Daily repository updates

[← Back to MauLab](../README.md) · [Roadmap](roadmap.md)

## What updates

The README activity section refreshes from committed Git history. It shows the refresh time, the number of substantive commits in the previous 24 hours, and the five latest changes with links to their commits. A substantive commit means any commit other than the automation's own `chore: refresh repository activity` commits; it is not a judgment of engineering impact.

Quiet days say that no new substantive commits were recorded. Previous changes remain visible with their original dates. The automation does not invent progress, inspect lab systems, or change infrastructure claims.

## Schedule and controls

- Scheduled daily at **13:17 UTC**: **8:17 a.m. CDT / 7:17 a.m. CST** in America/Chicago.
- Also runs when files other than only the README change on `main`.
- Run on demand under **Actions → Daily repository activity → Run workflow**.
- The workflow uses GitHub's built-in token with repository content write access; no external service or personal access token is required.
- Only the marked activity block in the README is generated. Edit the surrounding content normally and preserve both markers.

GitHub schedules can be delayed, and public-repository schedules can be disabled after 60 days without repository activity. See [GitHub's schedule documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule). The displayed refresh time makes stale output visible.

## Validation and maintenance

The [workflow](../.github/workflows/daily-activity.yml) runs generator tests and documentation checks before committing. It fails without publishing if validation fails. A concurrent change to `main` causes a normal push rejection rather than overwriting someone else's work; rerun the workflow to refresh against the latest branch.

To run locally with Python 3.10 or newer:

```bash
python -m pip install tzdata
python -m unittest discover -s tests -v
python scripts/update_activity.py
python scripts/check_docs.py
```

The `tzdata` package is needed only on systems without an IANA timezone database, such as many Windows installations. GitHub's Ubuntu runner already supplies timezone data.

If the activity badge is red, open the failed run and inspect its logs. Repository rules that prohibit direct bot commits to `main` need a compatible update process before automatic publication can succeed. To stop daily refreshes, disable **Daily repository activity** in GitHub Actions.
