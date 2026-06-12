# Systemd Tunnel Unit

Use this as a template for a single user-managed tunnel. It survives logout, sleep/wake, and network resets.

```ini
[Unit]
Description=SSH tunnel remote:<PORT> to 127.0.0.1:<LOCAL>
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/ssh -o StrictHostKeyChecking=no -o \
  ServerAliveInterval=30 -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes \
  -N -L 127.0.0.1:<LOCAL>:localhost:<REMOTE> <user>@<host>
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Operational notes
- `<LOCAL>` and `<REMOTE>` are the ports on the two ends.
- Replace `-N -L 127.0.0.1:<LOCAL>` with `-N -R` for reverse, or add multiple `-L` for composite.
- `RestartSec=5` avoids rapid storm if auth flaps on boot/wake.
- The host key will be accepted on first run; for reproducibility pre-populate `known_hosts`.

Enable and start the unit:

```bash
systemctl --user daemon-reload
systemctl --user enable --now tunnel-9router.service
```

Validation:

```bash
systemctl --user is-active tunnel-9router.service
systemctl --user status tunnel-9router.service --no-pager
```
