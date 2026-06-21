#!/usr/bin/env python3
"""Benchmark tunnel-qwen token speed.

Tests Qwen3.6-35B-A3B-UD-Q4_K_M.gguf via the tunnel-qwen proxy
(http://100.118.62.87:9099/v1) and reports tokens/sec, total time,
and first-request cold-start penalty.

Usage:
    python3 qwen_benchmark.py [num_requests]

Example:
    python3 qwen_benchmark.py 5
"""

import openai
import time
import sys

BASE_URL = "http://100.118.62.87:9099/v1"
MODEL = "Qwen3.6-35B-A3B-UD-Q4_K_M.gguf"
PROMPT = "Explain the Krebs cycle in 200 words."

def benchmark(num_requests=5):
    client = openai.OpenAI(base_url=BASE_URL, api_key="tunnel-qwen")

    print(f"Running {num_requests} requests to tunnel-qwen ({MODEL})...\n")

    results = []
    for i in range(num_requests):
        t0 = time.time()
        r = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT}],
            temperature=0.3,
            max_tokens=512,
        )
        total = time.time() - t0
        tokens = r.usage.completion_tokens
        tok_s = tokens / total if total > 0 else 0
        results.append((total, tokens, tok_s))
        print(f"Req {i+1}: {total:.2f}s | {tokens} tok | {tok_s:.1f} tok/s")

    avg_total = sum(r[0] for r in results) / len(results)
    avg_tokens = sum(r[1] for r in results) / len(results)
    avg_tok_s = sum(r[2] for r in results) / len(results)

    print(f"\n--- SUMMARY ---")
    print(f"Avg total: {avg_total:.2f}s")
    print(f"Avg tokens: {avg_tokens:.0f}")
    print(f"Avg tok/s: {avg_tok_s:.1f}")

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    benchmark(n)
