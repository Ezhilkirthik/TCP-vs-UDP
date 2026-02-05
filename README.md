# Advanced TCP vs UDP Final-Year Project (Professional Edition)

This is an advanced, submission-ready TCP vs UDP analysis project with polished reports and professional visualization.

## What's improved now

- Modular architecture (`src/tcp_udp_project/`) for maintainability.
- Reproducible stochastic simulation with configurable random seed.
- High-quality 4-panel dashboard with requested legend labels:
  - Graph 1: `TCPa`, `UDPa`
  - Graph 2: `TCPb`, `UDPb`
- Rich artifacts:
  - CSV dataset
  - Markdown statistical summary
  - Executive insights markdown
  - SVG dashboard
  - HTML dashboard viewer
- Basic automated test coverage.

## Project structure

- `main.py` — thin entrypoint.
- `src/tcp_udp_project/models.py` — data models.
- `src/tcp_udp_project/simulator.py` — protocol simulation logic.
- `src/tcp_udp_project/reporting.py` — CSV and markdown outputs.
- `src/tcp_udp_project/dashboard.py` — SVG dashboard renderer.
- `src/tcp_udp_project/cli.py` — orchestration and CLI.
- `tests/test_project.py` — smoke test for generated artifacts.

## Run

```bash
python3 main.py
```

## Options

```bash
python3 main.py --trials 80 --seed 123 --output-dir my_reports
```

## Test

```bash
python3 -m unittest -q
```

## Generated artifacts (default)

- `reports/tcp_udp_simulation_dataset.csv`
- `reports/analysis_summary.md`
- `reports/executive_insights.md`
- `reports/tcp_udp_advanced_dashboard.svg`
- `reports/tcp_udp_advanced_dashboard.html`
