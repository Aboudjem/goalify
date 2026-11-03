# Proposed CI job: validate the HyperFrames promo source

Paste this job into `.github/workflows/validate.yml` (under `jobs:`). It replaces the old Remotion
typecheck of `video/`. It never renders: `lint` is static, and `check` boots a headless Chrome to
seek the timeline and audit runtime errors, layout, motion and contrast. Both exit non-zero only on
errors (craft warnings are reported but do not fail).

Commands verified with `npx -y hyperframes@0.9.8 lint --help`, `check --help` and
`browser --help` (subcommand `ensure`) on 0.9.8. `lint --json` on this project prints
`"ok": true, "errorCount": 0`.

```yaml
video:
  name: Validate promo video source (HyperFrames)
  runs-on: ubuntu-latest
  timeout-minutes: 15
  defaults:
    run:
      working-directory: video
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: "22"
    - name: FFmpeg (HyperFrames probes the music files)
      run: sudo apt-get update && sudo apt-get install -y --no-install-recommends ffmpeg
    - name: index.html is the main cut (generated from scripts/build-roots.js)
      run: |
        node scripts/build-roots.js main
        git diff --exit-code -- index.html
    - name: Lint (static)
      run: npx -y hyperframes@0.9.8 lint
      env:
        HYPERFRAMES_SKIP_SKILLS: "1"
    - name: Chrome for the browser pass
      run: npx -y hyperframes@0.9.8 browser ensure
    - name: Check (runtime, layout, motion, contrast; no render)
      run: npx -y hyperframes@0.9.8 check --timeout 60s
      env:
        HYPERFRAMES_SKIP_SKILLS: "1"
```

Notes

- If the Chrome step is too slow or flaky on the runner, keep only the lint step: it covers the
  composition contract (timing attributes, timeline registration, media ids, transform conflicts).
- The pin `0.9.8` matches `video/package.json`. Bump both together
  (`npx hyperframes@latest upgrade --project . --check`).
- Optional: also validate the other cuts by looping
  `for c in vertical short demo; do node scripts/build-roots.js $c && npx -y hyperframes@0.9.8 lint; done`
  and restoring with `node scripts/build-roots.js main`.
