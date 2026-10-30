# Security and responsible disclosure

[← Back to MauLab](../README.md) · [Architecture](architecture.md)

MauLab is a personal infrastructure lab. This page documents security practices and boundaries, not a third-party audit or claim of comprehensive hardening.

## Access model

- Tailscale is used for remote access to authorized lab devices.
- SSH is used for Linux administration.
- Cloudflare Tunnel has been used selectively for remote connectivity experiments.
- Administrative interfaces should not be publicly exposed simply to make a demo convenient.
- The current household network is not yet a dedicated segmented/VLAN lab.

## What is intentionally excluded from GitHub

- Secrets, tokens, private keys, passwords, and credentials.
- Internal addresses, network maps detailed enough to expose access paths, or management endpoints.
- Actual customer or employer information from professional roles.
- Unredacted logs containing personal identifiers or session data.
- Backup contents, database dumps, and sensitive configuration exports.

## Documentation and testing practices

Before publishing a configuration example or incident report:

1. Replace host-specific values with clear placeholders.
2. Remove passwords, tokens, keys, and other sensitive strings.
3. Verify commands cannot accidentally delete or overwrite real data when copied.
4. Clearly label examples, future plans, and completed deployments.
5. If documenting a restore, test in an isolated environment and remove sensitive artifacts before publishing results.

## Planned security improvements

The longer-term design includes a dedicated firewall, managed switching, access-control policy documentation, and isolated lab networks. These changes are **not yet implemented** and should not be mistaken for current controls.

If you spot a potential security problem in the public documentation, please avoid posting sensitive exploit details or credentials in an issue. Contact the repository owner privately through an appropriate GitHub channel.
