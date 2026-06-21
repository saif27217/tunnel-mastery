# Tunnel Performance Benchmarks

## tunnel-qwen

**Endpoint:** `http://100.118.62.87:9099/v1`
**Model:** `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
**Method:** 5 consecutive requests, temperature 0.3–0.5

### Run 1 — 512 tokens, general knowledge

| Req | Total (s) | Tokens | Tok/s |
|-----|-----------|--------|-------|
| 1   | 10.90     | 340    | 31.2  |
| 2   | 9.13      | 313    | 34.3  |
| 3   | 9.31      | 332    | 35.6  |
| 4   | 9.62      | 345    | 35.9  |
| 5   | 9.29      | 322    | 34.6  |

**Summary:** Avg 34.3 tok/s | Avg total 9.65s | Range 31.2–35.9 tok/s

### Run 2 — 256 tokens, warmed up

| Req | Total (s) | Tokens | Tok/s |
|-----|-----------|--------|-------|
| 1   | 9.91      | 256    | 25.8  |
| 2   | 7.38      | 256    | 34.7  |
| 3   | 7.24      | 256    | 35.4  |
| 4   | 6.99      | 256    | 36.6  |
| 5   | 7.22      | 256    | 35.5  |

**Summary:** Avg 33.6 tok/s | Avg total 7.75s | Range 25.8–36.6 tok/s

### Run 3 — Complex tasks (384–512 tokens, mixed reasoning + code)

| Req | Task | Tokens | Tok/s |
|-----|------|--------|-------|
| 1   | Quantum entanglement + Bell's theorem | 512 | 26.3  |
| 2   | Python BST implementation | 384 | 39.4  |
| 3   | ML comparison (supervised/unsupervised/RL) | 512 | 28.9 |
| 4   | Krebs cycle + ETC explanation | 512 | 32.6  |
| 5   | FastAPI REST API endpoint | 384 | 38.3  |

**Summary:** Avg 33.1 tok/s | Avg total 14.53s | Avg tokens 461 | Range 26.3–39.4 tok/s

### Overall Summary

| Metric | Value |
|--------|-------|
| Avg tok/s (all runs) | **~33–34 tok/s** |
| Sustained (post-cold-start) | 34–37 tok/s |
| Cold start penalty | ~25–26 tok/s on first request |
| Complex tasks vs simple | No measurable degradation |

### Notes

- First request is slower (cold start / model loading), subsequent requests stabilize at ~34–37 tok/s.
- Model stays cached between requests, so sustained performance is the relevant metric.
- No performance degradation with complex reasoning or code generation tasks.
- Benchmark script: `scripts/qwen_benchmark.py` — run with `python3 scripts/qwen_benchmark.py [n]`.
- Heavy benchmark: `python3 /tmp/bench_heavy.py` for complex multi-domain tasks.
