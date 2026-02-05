from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from .dashboard import SvgDashboard
from .models import MetricSeries, NetworkScenario
from .reporting import ArtifactWriter
from .simulator import ProtocolSimulator


def default_scenarios() -> tuple[NetworkScenario, NetworkScenario]:
    scenario_a = NetworkScenario(
        tag="a",
        title="Scenario A - Campus LAN (Low Congestion)",
        base_bandwidth_mbps=120,
        base_rtt_ms=11,
        congestion_factor=0.18,
        loss_profile=(0.00, 0.01, 0.02, 0.03, 0.04, 0.05),
    )
    scenario_b = NetworkScenario(
        tag="b",
        title="Scenario B - WAN/Cellular (Moderate Congestion)",
        base_bandwidth_mbps=85,
        base_rtt_ms=37,
        congestion_factor=0.42,
        loss_profile=(0.00, 0.01, 0.02, 0.03, 0.04, 0.05),
    )
    return scenario_a, scenario_b


def build_rows(scenario: NetworkScenario, protocol: str, series: MetricSeries) -> Iterable[dict]:
    for p in series.points:
        yield {
            "scenario": scenario.title,
            "scenario_tag": scenario.tag,
            "protocol": protocol,
            "loss_pct": round(p.loss_pct, 3),
            "throughput_mbps": round(p.throughput_mbps, 3),
            "latency_ms": round(p.latency_ms, 3),
            "jitter_ms": round(p.jitter_ms, 3),
            "delivery_ratio_pct": round(p.delivery_ratio_pct, 3),
            "throughput_std": round(p.throughput_std, 3),
            "latency_std": round(p.latency_std, 3),
        }


def write_html_wrapper(svg_path: Path) -> Path:
    html_path = svg_path.with_suffix(".html")
    html_path.write_text(
        """<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'/>
  <meta name='viewport' content='width=device-width, initial-scale=1'/>
  <title>TCP vs UDP Dashboard</title>
  <style>
    body { margin: 0; background: #0f172a; color: #fff; font-family: Inter, Segoe UI, Arial, sans-serif; }
    .container { max-width: 1640px; margin: 0 auto; padding: 18px; }
    .card { background: #0b1222; border: 1px solid #1e293b; border-radius: 14px; padding: 14px; }
    object { width: 100%; border: none; min-height: 1080px; background: #e2e8f0; border-radius: 10px; }
    p { color: #cbd5e1; }
  </style>
</head>
<body>
  <div class='container'>
    <h1>TCP vs UDP — Advanced Final-Year Dashboard</h1>
    <p>Legends preserved as requested: Graph 1 (TCPa/UDPa), Graph 2 (TCPb/UDPb).</p>
    <div class='card'>
      <object data='tcp_udp_advanced_dashboard.svg' type='image/svg+xml'></object>
    </div>
  </div>
</body>
</html>
""",
        encoding="utf-8",
    )
    return html_path


def run(output_dir: Path, trials: int, seed: int) -> None:
    scenario_a, scenario_b = default_scenarios()
    sim = ProtocolSimulator(trials=trials, seed=seed)

    tcp_a = sim.simulate_tcp(scenario_a)
    udp_a = sim.simulate_udp(scenario_a)
    tcp_b = sim.simulate_tcp(scenario_b)
    udp_b = sim.simulate_udp(scenario_b)

    rows: list[dict] = []
    rows.extend(build_rows(scenario_a, "TCP", tcp_a))
    rows.extend(build_rows(scenario_a, "UDP", udp_a))
    rows.extend(build_rows(scenario_b, "TCP", tcp_b))
    rows.extend(build_rows(scenario_b, "UDP", udp_b))

    writer = ArtifactWriter(output_dir)
    csv_path = writer.write_csv(rows)
    summary_path = writer.write_summary(rows)
    insights_path = writer.write_insights(rows)

    svg_renderer = SvgDashboard()
    svg = svg_renderer.render(scenario_a, scenario_b, tcp_a, udp_a, tcp_b, udp_b)
    svg_path = output_dir / "tcp_udp_advanced_dashboard.svg"
    svg_path.write_text(svg, encoding="utf-8")
    html_path = write_html_wrapper(svg_path)

    print(f"Generated dataset: {csv_path}")
    print(f"Generated summary: {summary_path}")
    print(f"Generated insights: {insights_path}")
    print(f"Generated dashboard: {svg_path}")
    print(f"Generated dashboard viewer: {html_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TCP vs UDP Advanced Final-Year Project Generator")
    parser.add_argument("--output-dir", type=Path, default=Path("reports"), help="Directory for generated artifacts")
    parser.add_argument("--trials", type=int, default=60, help="Simulation trials per datapoint")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(output_dir=args.output_dir, trials=args.trials, seed=args.seed)
