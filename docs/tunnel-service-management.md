# Service Management — Persistence, Supervision, and Limits

## Principles
- Prefer systemd over background shell loops whenever the host runs systemd.
- Never trust backgrounded SSH from an interactive shell after logout.
- Make tunnels single-responsibility: one tunnel unit per destination port.

## linger + user units

A user unit only persists while an interactive session exists. For servers and long-lived tunnels:

```bash
loginctl enable-linger $UID
systemctl --user enable --now tunnel-<name>.service
```

`lingerd` is what keeps the user slice alive across logout. Nothing in the unit JSON implies this — it lives in `loginctl`.

## Restart policy

`Restart=always` + `RestartSec=5` gives the right balance. Do NOT use `Restart=on-failure` — tunneling failures are not clean exits from systemd's perspective when the exec line itself returns nonzero during an auth fail.

## Hardening notes (optional)

```ini
# place in the [Service] block
StandardOutput=journal
StandardError=journal
SyslogIdentifier=%n
```

For sensitive machines, add a matching `AuthorizedKeysFile` and disable `StrictHostKeyChecking=no` in favor of a fixed `known_hosts` entry.

## Observability

```bash
# Recent events
journalctl --user -u <unit> --since "30m ago"
# Count of restarts (useful in flapping scenarios)
systemctl --user show <unit> -p NRestarts
```

## Clean teardown

```bash
systemctl --user disable --now tunnel-<name>.service
systemctl --user daemon-reload
```

Kill stray tunnels by port: `ss -tlnp | grep <PORT>` then `kill <PID>`.
