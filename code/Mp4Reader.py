"""Read local experiment videos without retaining every full-resolution frame."""

from pathlib import Path

import imageio.v2 as imageio
import numpy as np


class Mp4Reader:
    """Crop RGB frames and average horizontally, retaining (time, y, RGB)."""

    def __init__(self, filename, data_dir):
        self.path = Path(data_dir).expanduser() / filename
        if not self.path.is_file():
            raise FileNotFoundError(f"Video not found: {self.path}")
        self.fps = None

    @staticmethod
    def _validate_range(bounds, limit, name):
        start, stop = bounds
        if not (0 <= start < stop <= limit):
            raise ValueError(
                f"Invalid {name} range {bounds}; expected 0 <= start < stop <= {limit}"
            )

    def pre_process(self, xrange=(100, 600), yrange=(0, 600)):
        """Use half-open x/y pixel ranges; keep the original RGB mean method.

        Image arrays use [y, x, channel]. The crop must fit every frame.
        Only the reduced RGB profile of each frame is retained in memory.
        """
        profiles = []
        expected_shape = None
        with imageio.get_reader(str(self.path), format="FFMPEG") as reader:
            self.fps = reader.get_meta_data().get("fps")
            for frame in reader:
                if frame.ndim != 3 or frame.shape[2] != 3:
                    raise ValueError(f"Expected RGB frames, got shape {frame.shape}")
                if expected_shape is None:
                    expected_shape = frame.shape
                    self._validate_range(xrange, frame.shape[1], "x")
                    self._validate_range(yrange, frame.shape[0], "y")
                elif frame.shape != expected_shape:
                    raise ValueError("Frame dimensions changed within the video")
                crop = frame[yrange[0]:yrange[1], xrange[0]:xrange[1], :]
                profiles.append(np.mean(crop, axis=1))
        if not profiles:
            raise ValueError(f"Video contains no frames: {self.path}")
        return np.stack(profiles, axis=0)
