# Tunnel 101 — Basics

## What an SSH tunnel is and why it's your first line for local-only ports

An SSH tunnel (`ssh -L local:remote:dest`) makes traffic look like it comes from `remote`, as far as the service on `dest` is concerned. It does not move ports, NAT, or proxy HTTP — it forwards TCP.

## Three canonical topologies

```
1) Local forward — most common for us
    laptop/VPS:PORT1 ──SSH──► remote:PORT2
    remote thinks traffic is from 127.0.0.1 (or remote's loopback)
```

```
2) Remote forward — expose a local service to the remote
                  ◄────── remote:PORT2
    laptop/VPS:PORT1 ──SSH──► remote:PORT2
    remote reachable at remote:PORT2
```

```
3) Dynamic / SOCKS
    local:SOCKS_PORT ──SSH──► remote
    apps use socks5://127.0.0.1:SOCKS_PORT as proxy
```

For 9router and the like, we almost exclusively use topology 1.

## The 127.0.0.1 rule

A tunnel from `127.0.0.1:20128` is only reachable by the local machine. A tunnel from `0.0.0.0:20128` is reachable from the LAN. In production, bind to `127.0.0.1` only unless you explicitly need other hosts to see it.

## Auth bypass via localhost

Many middleware stacks short-circuit auth when `request.remoteAddress` is 127.x.x.x. The 9router middleware is one of them. Tunnelling through SSH makes the caller appear as 127/1 on the remote side, bypassing remote API-key checks.

## Mental model of a tunnel lifecycle

- `ssh -N -L local:remote:target host` is a long-lived authenticated TCP connection.
- When that SSH link dies, `local` stops accepting connections with no signal on TCP.
- Hermes/proxy layers observe this as `ConnectionRefused`, `ConnectTimeout`, or generic 502s.
- The link does NOT auto-heal after one failure. Each tunnel is a single session.
