"""Create eight time-height RGB panels from local experiment videos."""

import argparse
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from Mp4Reader import Mp4Reader


CONDITIONS = (("pure", "No salinity / no buoyancy"),
              ("salt", "Salinity / buoyancy"))
SPEED_LABELS = ("1_5", "2_0", "2_5", "3_0")


def validate_fps(value):
    try:
        fps = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Video FPS is unavailable; supply --fps explicitly") from exc
    if not np.isfinite(fps) or fps <= 0:
        raise ValueError("FPS must be finite and positive")
    return fps


def main_plot(data_dir, xrange=(100, 600), yrange=(0, 600), fps=None):
    paths = [Path(data_dir).expanduser() / f"{condition}_v_{speed}.mp4"
             for condition, _ in CONDITIONS for speed in SPEED_LABELS]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing local input videos:\n" + "\n".join(missing))
    override_fps = validate_fps(fps) if fps is not None else None
    fig, axes = plt.subplots(2, 4, figsize=(12, 10), layout="constrained")
    try:
        for row, (condition, label) in enumerate(CONDITIONS):
            for col, speed in enumerate(SPEED_LABELS):
                reader = Mp4Reader(f"{condition}_v_{speed}.mp4", data_dir)
                profiles = reader.pre_process(xrange=xrange, yrange=yrange)
                frame_rate = (override_fps if override_fps is not None
                              else validate_fps(reader.fps))
                rgb = np.swapaxes(profiles / 255.0, 0, 1)
                height, count, _ = rgb.shape
                ax = axes[row, col]
                # Pixel centres: frame 0 is t=0; y=0 is the top of the crop.
                ax.imshow(rgb, aspect="auto", origin="upper", interpolation="nearest",
                          extent=(-0.5 / frame_rate, (count - 0.5) / frame_rate,
                                  height - 0.5, -0.5))
                index = row * 4 + col
                ax.set_title(f"({chr(97 + index)}) v={speed.replace('_', '.')} mm/s",
                             loc="left", weight="bold")
                ax.set_xlabel("Time (s)")
                if col == 0:
                    ax.set_ylabel(f"{label}\nVertical pixel in crop")
        return fig
    except Exception:
        plt.close(fig)
        raise


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True,
                        help="Local directory containing the eight MP4 input videos")
    parser.add_argument("--output", type=Path,
                        default=root / "outputs" / (
                            "time_height_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".png"))
    parser.add_argument("--x-range", type=int, nargs=2, default=(100, 600),
                        metavar=("START", "STOP"))
    parser.add_argument("--y-range", type=int, nargs=2, default=(0, 600),
                        metavar=("START", "STOP"))
    parser.add_argument("--fps", type=float,
                        help="Time-axis calibration override; does not resample frames")
    args = parser.parse_args()
    output = args.output.expanduser()
    if output.exists():
        parser.error(f"Output already exists; choose another path: {output}")
    fig = None
    try:
        fig = main_plot(args.data_dir, args.x_range, args.y_range, args.fps)
        output.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation also protects against overwrites during a long run.
        with output.open("xb") as stream:
            fig.savefig(stream, format="png", dpi=400)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    finally:
        if fig is not None:
            plt.close(fig)
    print(f"Saved {output.resolve()}")


if __name__ == "__main__":
    main()
