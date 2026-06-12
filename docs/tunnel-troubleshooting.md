# Tunnel Troubleshooting — Deterministic Decision Tree

Rule: do NOT retry a failing probe instead of moving to a different probe.

## 1. Port is not listening

```bash
ss -tlnp | grep <PORT> || true
```

If nothing is listening:
- No tunnel process is running.
- If a systemd unit exists, check its status and logs: `systemctl status`, `journalctl --user -u <unit> --since "10m ago"`.
- Look for `bind ...: Address already in use` in the SSH log: this means a dead tunnel still holds the port. Kill stale `ssh` processes, then restart.

## 2. Port is listening, but curl to 127.0.0.1:<PORT> fails

If the port shows a valid SSH LISTEN state, tunnel failure is either:
- authentication rejection on remote (password/key mismatch, `StrictHostKeyChecking` interaction awaiting TTY)
- remote service not listening on `<REMOTE_PORT>`
- firewall between local and remote machines

For each SSH authentication failure, SSH exits with code 255, even with `RestartSec`. Scan for `Permission denied (publickey,password)` in logs.

## 3. Authentication succeeds, but upstream is unreachable from the tunnel

From inside the tunnel session, on the remote:
```bash
# on the remote host, if you have shell access via ssh command:
ssh -o StrictHostKeyChecking=no -W localhost:<REMOTE_PORT> <user>@<host> curl -sv http://localhost:<REMOTE_PORT>/health
```
If remote service is dead or on a non-standard address, reconnect.

## 4. Tunnel dies after sleep/wake

- Without supervision, SSH dies on network change.
- Prefer `systemd --user` `Restart=always` over ad-hoc background processes.
- The unit-plus-linger combo is required: `loginctl enable-linger $UID` and `Restart=always`.

## 5. Tunnel stutters, then works

Transient Tailscale peer flapping. Increase `ServerAliveInterval` to 60 and `RestartSec` to 10 if the peer is roamed frequently.

## 6. "API key required for remote API access"

You are hitting a 9router without a tunnel. Do NOT add remote auth keys — use a tunnel. Confirm with:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:<LOCAL>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"antigravity","messages":[]}'
```

200 with the tunnel is the failure mode to ignore. 401 through the tunnel means the middleware no longer localhost-whitelists your caller — check remote-side updates.
