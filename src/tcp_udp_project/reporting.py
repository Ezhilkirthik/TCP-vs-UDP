from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean


class ArtifactWriter:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_csv(self, rows: list[dict]) -> Path:
        path = self.output_dir / "tcp_udp_simulation_dataset.csv"
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        return path

    def write_summary(self, rows: list[dict]) -> Path:
        grouped: dict[tuple[str, str], list[dict]] = {}
        for row in rows:
            grouped.setdefault((row["scenario"], row["protocol"]), []).append(row)

        lines = ["# TCP vs UDP Comparative Summary", "", "This table reports averaged values across packet-loss levels.", ""]
        for scenario in sorted({k[0] for k in grouped}):
            lines.append(f"## {scenario}")
            lines.append("")
            lines.append("| Protocol | Avg Throughput (Mbps) | Avg Latency (ms) | Avg Jitter (ms) | Avg Delivery (%) | Avg Throughput σ | Avg Latency σ |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|")
            for protocol in ["TCP", "UDP"]:
                vals = grouped[(scenario, protocol)]
                lines.append(
                    f"| {protocol} | {mean(v['throughput_mbps'] for v in vals):.2f} | {mean(v['latency_ms'] for v in vals):.2f} "
                    f"| {mean(v['jitter_ms'] for v in vals):.2f} | {mean(v['delivery_ratio_pct'] for v in vals):.2f} "
                    f"| {mean(v['throughput_std'] for v in vals):.2f} | {mean(v['latency_std'] for v in vals):.2f} |"
                )
            lines.append("")

        path = self.output_dir / "analysis_summary.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def write_insights(self, rows: list[dict]) -> Path:
        def avg(rows2: list[dict], key: str) -> float:
            return mean(r[key] for r in rows2)

        lines = ["# Executive Insights", ""]
        for scenario in sorted({r["scenario"] for r in rows}):
            tcp = [r for r in rows if r["scenario"] == scenario and r["protocol"] == "TCP"]
            udp = [r for r in rows if r["scenario"] == scenario and r["protocol"] == "UDP"]
            lines.append(f"## {scenario}")
            lines.append(f"- UDP average throughput is **{avg(udp, 'throughput_mbps') - avg(tcp, 'throughput_mbps'):+.2f} Mbps** vs TCP.")
            lines.append(f"- UDP average latency is **{avg(tcp, 'latency_ms') - avg(udp, 'latency_ms'):+.2f} ms** lower than TCP (positive means UDP is lower).")
            lines.append(f"- TCP delivery reliability is **{avg(tcp, 'delivery_ratio_pct') - avg(udp, 'delivery_ratio_pct'):+.2f}%** higher than UDP.")
            lines.append("")

        path = self.output_dir / "executive_insights.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        return path
