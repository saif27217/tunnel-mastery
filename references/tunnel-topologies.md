# Tunnel Topologies — Reference and Rationale

## Decision map

```
Remote service reachable by IP?
 YES ─► Do you need localhost-only auth bypass?
       YES ─► use SSH tunnel if SSH available
       NO  ─► use HTTP proxy / reverse proxy
 NO  ─► Can you add an SSH? If yes, use tunnel; otherwise not solvable by you
```

## Topology 1 — Local forward (us)

```
local ltun <PORT1> ──┐
                     ├─ SSH ──► remote:22
local http <PORT2> ──┘         host.remote:20128 (local to remote machine)
```

Use for 9router, database replies, git-daemon.

## Topology 2 — Remote forward (less common)

```
local service:3000 ──┐   reverse-forward exposes itself externally
                     ├── SSH ──► remote:3010
                     │
remote peer hits host:3010 because of reverse anchor
```

## Topology 3 — SOCKS (app-level proxy)

```
app → socks5://127.0.0.1:1080 → SSH → socks proxy on remote → internet
```

Use for browser sessions, apt/yum mirrors in isolated networks, egress control.

## Topology 4 — Composite (multi-forward)

```bash
ssh -N \
  -L 12028:localhost:20128 \
  -L 5432:localhost:5432 \
  user@host
```

One SSH session, multiple forwards. Memory/CPU cost is small; systemd unit runs this cleanly.

## Topology 5 — Paramiko programmatic tunnel

Use when a foreground process cannot keep a gateway-visible SSH session. The channel survives independently of the SSH session's shell streams.

```python
transport = client.get_transport()
chan = transport.open_channel('direct-tcpip', ('127.0.0.1', REMOTE_PORT), ('127.0.0.1', 0))
# read/write to chan as needed, keep reference alive
```

Remember to keep `transport` and `chan` referenced for the tunnel lifetime, or the GC collects them.
