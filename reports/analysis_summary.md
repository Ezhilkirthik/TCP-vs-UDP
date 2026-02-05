# TCP vs UDP Comparative Summary

This table reports averaged values across packet-loss levels.

## Scenario A - Campus LAN (Low Congestion)

| Protocol | Avg Throughput (Mbps) | Avg Latency (ms) | Avg Jitter (ms) | Avg Delivery (%) | Avg Throughput σ | Avg Latency σ |
|---|---:|---:|---:|---:|---:|---:|
| TCP | 90.99 | 25.52 | 1.86 | 99.58 | 1.80 | 1.10 |
| UDP | 107.19 | 14.39 | 1.48 | 98.25 | 1.57 | 0.77 |

## Scenario B - WAN/Cellular (Moderate Congestion)

| Protocol | Avg Throughput (Mbps) | Avg Latency (ms) | Avg Jitter (ms) | Avg Delivery (%) | Avg Throughput σ | Avg Latency σ |
|---|---:|---:|---:|---:|---:|---:|
| TCP | 45.61 | 51.56 | 1.86 | 99.58 | 1.74 | 1.15 |
| UDP | 66.90 | 40.32 | 1.47 | 98.27 | 1.57 | 0.71 |
