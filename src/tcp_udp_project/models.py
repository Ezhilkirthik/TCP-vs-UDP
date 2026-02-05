from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NetworkScenario:
    tag: str
    title: str
    base_bandwidth_mbps: float
    base_rtt_ms: float
    congestion_factor: float
    loss_profile: tuple[float, ...]


@dataclass
class MetricPoint:
    loss_pct: float
    throughput_mbps: float
    latency_ms: float
    jitter_ms: float
    delivery_ratio_pct: float
    throughput_std: float
    latency_std: float


@dataclass
class MetricSeries:
    points: list[MetricPoint]

    def values(self, name: str) -> list[float]:
        return [getattr(p, name) for p in self.points]
