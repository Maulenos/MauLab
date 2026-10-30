# Engineering roadmap

[← Back to MauLab](../README.md) · [Architecture](architecture.md) · [Case studies](case-studies.md)

This page separates **existing lab capabilities** from proposed upgrades and learning goals. It is a planning document, not a completion claim.

## Current foundation

- [x] Operate an Unraid host for storage, containers, and virtual machines.
- [x] Administer Linux-based infrastructure and services.
- [x] Use Tailscale and SSH for authorized remote access.
- [x] Work with Docker Compose and self-hosted services.
- [x] Use Prometheus and Grafana for lab monitoring.
- [x] Implement nightly systemd backups with retention and integrity checks.
- [x] Document a current-state architecture and operational lessons.

## Near term — operational maturity

- [ ] Publish sanitized, reproducible Compose examples without secrets.
- [ ] Add a small documented service-deployment demonstration with tests.
- [ ] Capture an isolated restore drill and record what was validated.
- [ ] Publish a redacted monitoring dashboard screenshot or example metrics.
- [ ] Convert a lab incident into a dated troubleshooting write-up with before/after evidence.
- [ ] Add automated checks for public configuration examples.

## Next — infrastructure as code and deployment

- [ ] Practice configuration management with Ansible.
- [ ] Create a small Terraform experiment with documented state and cleanup.
- [ ] Build an end-to-end CI workflow for **application code**, including tests and release criteria.
- [ ] Learn container orchestration through a small Kubernetes deployment after establishing networking fundamentals.

## Hardware and networking expansion (not installed)

| Candidate | Intended learning outcome |
| --- | --- |
| UPS | Power protection and controlled shutdown/recovery |
| MikroTik CRS310 | Managed switching, VLANs, trunks, and port configuration |
| Protectli VP6650 | Firewall and routing policy experiments |
| Framework-based compute | Additional virtualization and isolated experimentation |
| SBC or Jetson nodes | Small distributed services and automation |
| Additional storage | Resilience and capacity |

**Important:** The presence of a product in this table is not evidence of purchase, installation, or a working deployment.

## Documentation quality

This repository includes a lightweight GitHub Actions job that checks Markdown files for missing local links, headings, and unbalanced code fences. That workflow is specifically **documentation CI**, not deployment CI. It provides a first quality gate while the lab's reusable configuration and code examples are being prepared.

The next milestone is to move from narrative explanations to **redacted, reproducible examples with validation evidence**.
