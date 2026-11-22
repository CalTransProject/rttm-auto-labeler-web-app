"""Unit tests for the LiDAR frame auditor using synthetic point clouds."""
import tempfile
import unittest
import zipfile
from pathlib import Path

import numpy as np

from lidar_frame_auditor import scan, write_reports


class AuditorTests(unittest.TestCase):
    def test_valid_frames_and_reports(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            frames = base / "frames"
            frames.mkdir()
            points = np.array([[1, 2, 3, 4], [0, 0, 0, 5]], dtype="<f4")
            (frames / "000203.bin").write_bytes(points.tobytes())
            report = scan(frames)
            self.assertEqual(report["frames_scanned"], 1)
            self.assertEqual(report["total_points"], 2)
            self.assertEqual(report["frames_with_warnings"], 1)
            self.assertEqual(report["frames"][0]["zero_xyz_points"], 1)
            out = base / "results"
            write_reports(report, out)
            self.assertTrue((out / "audit_summary.csv").exists())
            self.assertTrue((out / "audit_summary.json").exists())
            self.assertTrue((out / "numbered_txt_reports" / "000203.txt").exists())

    def test_zip_and_nonfinite_value(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "frames.zip"
            point = np.array([[np.nan, 2, 3, 4]], dtype="<f4")
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("dataset/000204.bin", point.tobytes())
            report = scan(archive)
            self.assertEqual(report["frames_scanned"], 1)
            self.assertEqual(report["frames"][0]["nonfinite_points"], 1)

    def test_invalid_frame_size(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "000205.bin"
            path.write_bytes(b"invalid")
            report = scan(Path(temp))
            self.assertEqual(report["frames"][0]["point_count"], 0)
            self.assertTrue(any("size not divisible" in w for w in report["frames"][0]["issues"]))


if __name__ == "__main__":
    unittest.main()
