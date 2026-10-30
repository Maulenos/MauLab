# Engineering case studies

[← Back to MauLab](../README.md) · [Operations](operations.md) · [Architecture](architecture.md)

These are concise accounts of completed, hands-on lab work. They intentionally avoid invented throughput figures, uptime percentages, timestamps, performance improvements, or unverified deployment scope.

## Case study 1: Backup automation and integrity

**Skills:** Linux · systemd · scheduled jobs · PostgreSQL · backup validation · SHA-256 · retention

### Context

A self-hosted environment needs consistent maintenance and a way to check that the data produced by a backup workflow is plausible and unchanged. Manual, undocumented operations are easy to forget and harder to inspect later.

### Work completed

- Implemented **nightly backup automation with systemd**.
- Applied a **14-day retention policy** for backup artifacts.
- Added **PostgreSQL dump validation** to help detect unusable database output.
- Added **SHA-256 checksum verification** to help identify integrity mismatches.
- Practiced safe verification and dry-run reasoning around file-maintenance operations.

### Engineering lessons

- Scheduling alone is not sufficient: success should be verified using job results and artifacts.
- A checksum can detect changes to an artifact; it does **not** prove the application can be fully restored.
- Retention logic must be constrained so deleting old artifacts cannot affect live data.
- Backups become more useful when their restore path is exercised separately.

**Next improvement:** publish sanitized units/scripts and evidence of an isolated restore test, after reviewing them for secrets and environment-specific details.

## Case study 2: Monitoring service recovery

**Skills:** Docker Compose · Linux troubleshooting · Prometheus · Grafana · observability

### Context

Monitoring is useful only when monitoring services are themselves reachable and operating. During lab deployment and troubleshooting, service availability issues included **port conflicts**.

### Work completed

- Deployed and operated containerized services and a Prometheus/Grafana monitoring stack.
- Investigated monitoring availability and service/container state.
- Resolved port conflicts affecting the monitoring setup.
- Continued development of a separate local monitoring/control interface on Mau Envy.

### Engineering lessons

- Check container/service state and logs before assuming the failure is a network outage.
- Port bindings, host listeners, and Docker service mappings can interact unexpectedly.
- Verify the end-to-end user-visible result after making a configuration correction.
- Keep a clear distinction between a service being online and the metrics it reports being healthy.

**Next improvement:** publish a scrubbed reproduction with a minimal Compose file, failure symptoms, expected output, and a documented rollback.

## Case study 3: Remote administration boundary

**Skills:** Tailscale · SSH · remote troubleshooting · access design

### Context

The lab needs to be administrable from trusted devices away from home, while avoiding unnecessary public exposure of management services.

### Approach in use

- Use **Tailscale** to reach authorized lab systems remotely.
- Use **SSH** for Linux host administration.
- Keep private addressing, credentials, and administrative endpoints outside public documentation.
- Experiment with Cloudflare Tunnel selectively rather than exposing all management surfaces by default.

### Tradeoffs and next work

Private connectivity simplifies remote access but still requires appropriate authentication, patching, and access review. Dedicated firewall policies and segmented networks remain planned work rather than existing guarantees.

## Evidence and limits

The repo is currently documentation-first. Private host configuration, backup data, and infrastructure credentials are not checked into GitHub. Descriptions above reflect implemented lab work but should **not** be read as a public, independently reproducible deployment until sanitized source, tests, and screenshots are added.

For a repeatable diagnostic approach, see the [operations runbook](operations.md).
