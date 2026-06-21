# Tunnel Performance Benchmarks

## tunnel-qwen

**Endpoint:** `http://100.118.62.87:9099/v1`
**Model:** `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
**Method:** 5 consecutive requests, 512 max tokens, temperature 0.3

### Results (warmed up)

| Req | Total (s) | Tokens | Tok/s |
|-----|-----------|--------|-------|
| 1   | 10.90     | 340    | 31.2  |
| 2   | 9.13      | 313    | 34.3  |
| 3   | 9.31      | 332    | 35.6  |
| 4   | 9.62      | 345    | 35.9  |
| 5   | 9.29      | 322    | 34.6  |

### Summary

| Metric | Value |
|--------|-------|
| Avg tok/s | **34.3** |
| Avg total | 9.65s |
| Range | 31.2 – 35.9 tok/s |

### Notes

- First request is slower (cold start / model loading), subsequent requests stabilize at ~34-36 tok/s.
- Model stays cached between requests, so sustained performance is the relevant metric.
- Benchmark script: `scripts/qwen_benchmark.py` — run with `python3 scripts/qwen_benchmark.py [n]`.
