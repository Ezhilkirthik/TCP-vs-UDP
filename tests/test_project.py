import tempfile
import unittest
from pathlib import Path

from src.tcp_udp_project.cli import run


class ProjectGenerationTest(unittest.TestCase):
    def test_report_generation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            run(output_dir=out, trials=10, seed=7)
            self.assertTrue((out / "tcp_udp_simulation_dataset.csv").exists())
            self.assertTrue((out / "analysis_summary.md").exists())
            self.assertTrue((out / "executive_insights.md").exists())
            self.assertTrue((out / "tcp_udp_advanced_dashboard.svg").exists())
            self.assertTrue((out / "tcp_udp_advanced_dashboard.html").exists())


if __name__ == "__main__":
    unittest.main()
