from __future__ import annotations

import math
import random
from statistics import mean, pstdev

from .models import MetricPoint, MetricSeries, NetworkScenario


class ProtocolSimulator:
    def __init__(self, trials: int = 60, seed: int = 42) -> None:
        self.trials = trials
        self.seed = seed
        self.rng = random.Random(seed)

    @staticmethod
    def _clip(v: float, lo: float, hi: float | None = None) -> float:
        v = max(v, lo)
        return min(v, hi) if hi is not None else v

    def _dist_stats(self, fn) -> tuple[float, float]:
        vals = [fn() for _ in range(self.trials)]
        return mean(vals), pstdev(vals)

    def simulate_tcp(self, scenario: NetworkScenario) -> MetricSeries:
        points: list[MetricPoint] = []
        for loss in scenario.loss_profile:
            t_avg, t_std = self._dist_stats(
                lambda: scenario.base_bandwidth_mbps
                * (1 - scenario.congestion_factor)
                * math.exp(-3.2 * loss)
                + self.rng.gauss(0, 1.8)
            )
            l_avg, l_std = self._dist_stats(
                lambda: scenario.base_rtt_ms + 8 + 260 * loss + self.rng.gauss(0, 1.1)
            )
            j_avg = mean(1.4 + 18 * loss + self.rng.gauss(0, 0.55) for _ in range(self.trials))
            d_avg = mean(99.7 - 4.4 * loss + self.rng.gauss(0, 0.1) for _ in range(self.trials))

            points.append(
                MetricPoint(
                    loss_pct=loss * 100,
                    throughput_mbps=self._clip(t_avg, 1.0),
                    latency_ms=self._clip(l_avg, 1.0),
                    jitter_ms=self._clip(j_avg, 0.1),
                    delivery_ratio_pct=self._clip(d_avg, 94.0, 100.0),
                    throughput_std=max(t_std, 0.01),
                    latency_std=max(l_std, 0.01),
                )
            )
        return MetricSeries(points)

    def simulate_udp(self, scenario: NetworkScenario) -> MetricSeries:
        points: list[MetricPoint] = []
        for loss in scenario.loss_profile:
            t_avg, t_std = self._dist_stats(
                lambda: scenario.base_bandwidth_mbps
                * (1 - 0.45 * scenario.congestion_factor)
                * math.exp(-1.15 * loss)
                + self.rng.gauss(0, 1.55)
            )
            l_avg, l_std = self._dist_stats(
                lambda: scenario.base_rtt_ms + 1.5 + 74 * loss + self.rng.gauss(0, 0.75)
            )
            j_avg = mean(0.85 + 25 * loss + self.rng.gauss(0, 0.5) for _ in range(self.trials))
            d_avg = mean(99.2 - 37.5 * loss + self.rng.gauss(0, 0.3) for _ in range(self.trials))

            points.append(
                MetricPoint(
                    loss_pct=loss * 100,
                    throughput_mbps=self._clip(t_avg, 1.0),
                    latency_ms=self._clip(l_avg, 1.0),
                    jitter_ms=self._clip(j_avg, 0.1),
                    delivery_ratio_pct=self._clip(d_avg, 68.0, 100.0),
                    throughput_std=max(t_std, 0.01),
                    latency_std=max(l_std, 0.01),
                )
            )
        return MetricSeries(points)
