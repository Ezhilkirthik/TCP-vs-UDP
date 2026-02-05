from __future__ import annotations

from .models import MetricSeries, NetworkScenario


class SvgDashboard:
    def __init__(self, width: int = 1600, height: int = 1080) -> None:
        self.width = width
        self.height = height
        self.body: list[str] = []

    def _append(self, s: str) -> None:
        self.body.append(s)

    def _text(self, x, y, text, size=14, weight="normal", fill="#0f172a", anchor="start"):
        t = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self._append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" font-family="Inter, Segoe UI, Arial, sans-serif">{t}</text>')

    def _line(self, x1, y1, x2, y2, color="#334155", width=1.0, dash=""):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self._append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{width}"{da}/>')

    def _rect(self, x, y, w, h, fill="#fff", stroke="#cbd5e1", sw=1.0, rx=8):
        self._append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}"/>')

    def _polyline(self, points: list[tuple[float, float]], color: str, width: float = 3, dash: str = ""):
        pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self._append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}"{da}/>')

    def _circle(self, x, y, r=4, fill="#fff", stroke="#000", sw=2):
        self._append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def _panel(self, x, y, w, h, title, xlabel, ylabel, x_values, series):
        self._rect(x, y, w, h, fill="#f8fbff", stroke="#bfcee3", sw=1.2)
        pl, pr, pt, pb = 70, 20, 42, 64
        gx, gy, gw, gh = x + pl, y + pt, w - pl - pr, h - pt - pb

        y_values = [v for _, ys, _, _ in series for v in ys]
        y_min, y_max = min(y_values), max(y_values)
        span = y_max - y_min if y_max != y_min else 1.0
        y_min -= span * 0.08
        y_max += span * 0.10

        x_min, x_max = min(x_values), max(x_values)
        x_span = x_max - x_min if x_max != x_min else 1.0

        self._line(gx, gy, gx, gy + gh, width=1.3)
        self._line(gx, gy + gh, gx + gw, gy + gh, width=1.3)

        for i in range(6):
            yy = gy + gh * i / 5
            val = y_max - (y_max - y_min) * i / 5
            self._line(gx, yy, gx + gw, yy, color="#e2e8f0", width=1)
            self._text(gx - 10, yy + 4, f"{val:.1f}", size=10, fill="#475569", anchor="end")

        for i, xv in enumerate(x_values):
            xx = gx + gw * (xv - x_min) / x_span
            self._line(xx, gy + gh, xx, gy + gh + 5, width=1)
            self._text(xx, gy + gh + 20, f"{xv:.0f}%", size=10, fill="#475569", anchor="middle")
            if 0 < i < len(x_values) - 1:
                self._line(xx, gy, xx, gy + gh, color="#f1f5f9", width=1)

        self._text(x + w / 2, y + 24, title, size=17, weight="bold", anchor="middle")
        self._text(x + w / 2, y + h - 14, xlabel, size=12, weight="semibold", fill="#334155", anchor="middle")
        self._text(x + 20, y + h / 2, ylabel, size=12, weight="semibold", fill="#334155", anchor="middle")

        lx, ly = x + w - 150, y + 12
        self._rect(lx, ly, 130, 58 + 21 * (len(series) - 2), fill="#ffffffde", stroke="#dbe4f2", sw=1, rx=6)
        ycur = ly + 20
        for label, ys, color, dash in series:
            points = []
            for xv, yv in zip(x_values, ys):
                px = gx + gw * (xv - x_min) / x_span
                py = gy + gh * (y_max - yv) / (y_max - y_min)
                points.append((px, py))
            self._polyline(points, color=color, width=3, dash=dash)
            for px, py in points:
                self._circle(px, py, r=3.8, fill="#fff", stroke=color, sw=2)
            self._line(lx + 8, ycur - 4, lx + 36, ycur - 4, color=color, width=3, dash=dash)
            self._text(lx + 42, ycur, label, size=12, weight="semibold")
            ycur += 20

    def render(self, scenario_a: NetworkScenario, scenario_b: NetworkScenario, tcp_a: MetricSeries, udp_a: MetricSeries, tcp_b: MetricSeries, udp_b: MetricSeries) -> str:
        self._text(800, 56, "Advanced TCP vs UDP Comparative Dashboard", size=34, weight="bold", anchor="middle")
        self._text(800, 85, "Final-Year Project | Professional Simulation, Analysis, and Visualization", size=15, anchor="middle", fill="#334155")

        xvals = tcp_a.values("loss_pct")
        c1, c2 = "#2563eb", "#e11d48"
        self._panel(42, 120, 745, 430, f"Graph 1: Latency vs Packet Loss ({scenario_a.tag.upper()})", "Packet Loss (%)", "Latency (ms)", xvals, [("TCPa", tcp_a.values("latency_ms"), c1, ""), ("UDPa", udp_a.values("latency_ms"), c2, "")])
        self._panel(812, 120, 745, 430, f"Graph 2: Throughput vs Packet Loss ({scenario_b.tag.upper()})", "Packet Loss (%)", "Throughput (Mbps)", xvals, [("TCPb", tcp_b.values("throughput_mbps"), c1, ""), ("UDPb", udp_b.values("throughput_mbps"), c2, "")])
        self._panel(42, 585, 745, 430, "Graph 3: Delivery Ratio vs Packet Loss", "Packet Loss (%)", "Delivery Ratio (%)", xvals, [("TCPa", tcp_a.values("delivery_ratio_pct"), c1, ""), ("UDPa", udp_a.values("delivery_ratio_pct"), c2, ""), ("TCPb", tcp_b.values("delivery_ratio_pct"), "#1d4ed8", "7,5"), ("UDPb", udp_b.values("delivery_ratio_pct"), "#be123c", "7,5")])
        self._panel(812, 585, 745, 430, "Graph 4: Jitter vs Packet Loss", "Packet Loss (%)", "Jitter (ms)", xvals, [("TCPa", tcp_a.values("jitter_ms"), c1, ""), ("UDPa", udp_a.values("jitter_ms"), c2, ""), ("TCPb", tcp_b.values("jitter_ms"), "#1d4ed8", "7,5"), ("UDPb", udp_b.values("jitter_ms"), "#be123c", "7,5")])

        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">'
            "<defs><linearGradient id='bg' x1='0' y1='0' x2='0' y2='1'><stop offset='0%' stop-color='#f5f8fe'/><stop offset='100%' stop-color='#eaf1fb'/></linearGradient></defs>"
            f"<rect width='{self.width}' height='{self.height}' fill='url(#bg)'/>"
            + "".join(self.body)
            + "</svg>"
        )
