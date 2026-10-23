"""Synthetic checks for crop geometry and time calibration; no experiment video needed."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from Mp4Reader import Mp4Reader
from Plotter import validate_fps


class ProcessingTests(unittest.TestCase):
    def read_frames(self, frames, **kwargs):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "sample.mp4").touch()
            fake = MagicMock()
            fake.__iter__.side_effect = lambda: iter(frames)
            fake.get_meta_data.return_value = {"fps": 30.0}
            context = MagicMock()
            context.__enter__.return_value = fake
            with patch("Mp4Reader.imageio.get_reader", return_value=context):
                video = Mp4Reader("sample.mp4", directory)
                result = video.pre_process(**kwargs)
            context.__exit__.assert_called_once()
            return result, video.fps

    def test_non_square_crop_matches_original_horizontal_mean(self):
        frames = np.arange(2 * 4 * 7 * 3, dtype=np.uint8).reshape(2, 4, 7, 3)
        result, fps = self.read_frames(frames, xrange=(2, 6), yrange=(1, 3))
        expected = np.mean(frames[:, 1:3, 2:6, :], axis=2)
        np.testing.assert_array_equal(result, expected)
        self.assertEqual(result.shape, (2, 2, 3))
        self.assertEqual(fps, 30.0)

    def test_crop_outside_frame_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid x range"):
            self.read_frames([np.zeros((4, 7, 3), dtype=np.uint8)],
                             xrange=(0, 8), yrange=(0, 4))

    def test_empty_video_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "no frames"):
            self.read_frames([], xrange=(0, 1), yrange=(0, 1))

    def test_changing_dimensions_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "dimensions changed"):
            self.read_frames([np.zeros((4, 7, 3)), np.zeros((5, 7, 3))],
                             xrange=(0, 7), yrange=(0, 4))

    def test_invalid_frame_rates_are_rejected(self):
        for fps in [None, 0, -30, float("nan"), float("inf")]:
            with self.subTest(fps=fps), self.assertRaises(ValueError):
                validate_fps(fps)
        self.assertEqual(validate_fps(29.97), 29.97)


if __name__ == "__main__":
    unittest.main()
