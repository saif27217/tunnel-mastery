# Tunnel Patterns — Reusable Recipes

## Minimal one-shot tunnel for debugging

```bash
ssh -N -o StrictHostKeyChecking=no -o ServerAliveInterval=30 \
  -o ExitOnForwardFailure=yes \
  -L 12028:localhost:20128 user@host
```

Open a second shell to validate:

```bash
curl -s http://127.0.0.1:12028/v1/models | head
```

## Persistent reconnect loop (scripted)

Use this only when a proper `systemd --user` unit is not possible (e.g., container without systemd).

```bash
#!/usr/bin/env bash
set -euo pipefail
TUNNEL_PORT=12028
REMOTE_PORT=20128
REMOTE_USER=shark
REMOTE_HOST=100.77.100.52

while true; do
  ssh -o StrictHostKeyChecking=no \
    -o ServerAliveInterval=15 \
    -o ServerAliveCountMax=3 \
    -o ExitOnForwardFailure=yes \
    -N -L ${TUNNEL_PORT}:localhost:${REMOTE_PORT} ${REMOTE_USER}@${REMOTE_HOST}
  sleep 3
done
```

`ExitOnForwardFailure=yes` is the key — the loop only restarts when the forwards are actually established. Without it, you loop very fast on config errors.

## systemd --user unit (preferred in production)

See `references/systemd-tunnel-unit.md`.

## Composite tunnel with multiple forwards

```bash
ssh -N \
  -L 12028:localhost:20128 \
  -L 5432:localhost:5432 \
  -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
  user@host
```

## Auto-SSH with built-in monitor (alternative)

`autossh` wraps the tunnel and refreshes the session without needing systemd.

```bash
autossh -N \
  -o StrictHostKeyChecking=no \
  -o ServerAliveInterval=15 -o ServerAliveCountMax=3 \
  -M 0 -o "ExitOnForwardFailure=yes" \
  -L 12028:localhost:20128 user@host
```

The `-M 0` disables the monitor port; auto-SSH relies on TCP keepalives alone.

## ProxyCommand (jump host)

```bash
Host inner
  ProxyJump user@jumphost
  HostName 10.0.0.5
  User ubuntu
```

Then `ssh inner` and tunnel on the inner hop.

## SOCKS tunnel (for browser / curl / apt via proxy)

```bash
ssh -N -D 1080 user@host
# use as socks5://127.0.0.1:1080 from any local app
```
