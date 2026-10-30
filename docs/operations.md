# Operations and troubleshooting runbook

[← Back to MauLab](../README.md) · [Architecture](architecture.md) · [Case studies](case-studies.md)

**Purpose:** A reusable, safety-conscious process for observing service health and troubleshooting Linux and Docker workloads. Commands below are **examples to adapt to the target host**, not a claim that a complete orchestration or automated incident-response system already exists.

## 1. Establish impact and scope

Record:

- Time, affected service(s), affected host, observed symptoms, and user impact.
- Whether the issue is isolated to a service, container, host, or network path.
- Recent changes, including configuration updates, restarts, and deployments.
- Baseline and comparison observations where available.

Check host state before making changes:

```bash
hostnamectl
uptime
df -h
free -h
systemctl --failed
```

Read-only commands are preferred during initial triage.

## 2. Investigate service and container health

On a Docker host, inspect inventory and state:

```bash
docker ps --all
docker stats --no-stream
docker compose ps
docker compose logs --tail=100
```

Run `docker compose` commands in the relevant project directory (or specify the Compose file explicitly). Logs can contain private identifiers or tokens; **redact before sharing**.

For a systemd-managed service:

```bash
systemctl status SERVICE_NAME
journalctl -u SERVICE_NAME --since "1 hour ago" --no-pager
```

Replace `SERVICE_NAME` with the actual unit. Avoid posting raw logs publicly without review.

## 3. Inspect network and port conflicts

```bash
ss -ltnp
ip route
ip addr
getent hosts example.com
```

If a container or monitoring service fails to bind to a port:

1. Identify the expected listener and configured port.
2. Compare actual listeners with the service's Docker/Compose configuration.
3. Inspect service logs for bind errors or repeated restarts.
4. Determine whether to change the service mapping or retire an obsolete listener.
5. Make one controlled change and validate the expected endpoint.

Do not stop or reconfigure an unknown listener merely to free its port.

## 4. Validate a change

After an approved change:

- Verify the service starts and remains running.
- Inspect recent logs for new errors.
- Confirm the intended network endpoint is reachable from an authorized device.
- Check any relevant Grafana/Prometheus metrics if those systems are available.
- Document what changed, how it was tested, and the rollback approach.

Treat `docker compose up -d`, configuration changes, and service restarts as **mutating operations**; use them only after validating the appropriate target and impact.

## 5. Backup and restore verification

A backup file existing is not equivalent to confirmed recovery.

The lab's implemented maintenance work includes nightly systemd scheduling, a 14-day retention policy, PostgreSQL dump validation, and SHA-256 integrity checks. The following verification questions guide further maturity:

| Check | Purpose |
| --- | --- |
| Scheduled unit execution | Did the intended job run, and did it exit successfully? |
| Artifact presence and age | Was a current artifact produced in the expected location? |
| Database dump validation | Was the generated database dump checked for validity? |
| SHA-256 digest | Can the artifact be checked for unexpected modification? |
| Retention behavior | Are older artifacts pruned according to policy, without removing active data? |
| Restore exercise | Can a selected artifact be restored and verified in an isolated test? |

**Important:** A recurring isolated restore drill and published recovery-time measurement are **future improvements**, not completed work claimed here.

## 6. Record an incident

Use this compact template for lab incidents:

```text
Incident:
Timestamp / timezone:
Affected component:
Observed symptoms:
Impact:
Evidence (metrics, logs, status):
Working hypothesis:
Change made:
Validation performed:
Rollback plan / actual rollback:
Root cause (if verified):
Follow-up action:
```

Distinguish confirmed root cause from a hypothesis. Keep raw secrets and private endpoints out of public incident write-ups.

## 7. Escalation and communication mindset

Professional NOC experience informs the process: prioritize impact, communicate what is known, maintain clear notes, track ownership, and hand off unresolved issues with evidence. MauLab is a personal lab, so enterprise customer SLAs and organizational change approvals are **not claimed**.

See [case studies](case-studies.md) for specific lab work and [security](security.md) for public documentation boundaries.
