"""Build a folder-per-class image dataset from PitVis per-second instrument labels.

Classes: suction, kerrison (each the only instrument in view) and none (inside the patient, no instrument).
Frames are cropped to the square around the endoscope circle.

usage: make_cls_dataset.py <ann_dir> <video_dir> <out_dir> <video>:<split>:<n_per_class> ...
"""
import csv
import subprocess
import sys
from pathlib import Path

ann_dir, video_dir, out_dir = map(Path, sys.argv[1:4])
CLASSES = {"suction": lambda a, b: a == 16 and b == -2,
           "kerrison": lambda a, b: a == 8 and b == -2,
           "none": lambda a, b: a == 0}
manifest = []

def spaced(times, n, gap=3):
    picked = []
    for t in (times[int(i * len(times) / n)] for i in range(n)) if len(times) > n else times:
        if not picked or t - picked[-1] >= gap:
            picked.append(t)
    return picked

for spec in sys.argv[4:]:
    vid, split, n = spec.split(":")
    rows = list(csv.DictReader(open(ann_dir / f"annotations_{vid}.csv")))
    for name, rule in CLASSES.items():
        ts = [int(r["int_time"]) for r in rows
              if int(r["int_step"]) >= 0 and rule(int(r["int_instrument1"]), int(r["int_instrument2"]))]
        d = out_dir / split / name
        d.mkdir(parents=True, exist_ok=True)
        for t in spaced(ts, int(n)):
            out = d / f"v{vid}_t{t:05d}.jpg"
            if not out.exists():
                subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", str(video_dir / f"video_{vid}.mp4"),
                                "-frames:v", "1", "-vf", "crop=720:720:267:0", "-q:v", "2", str(out)], check=True)
            manifest.append((split, name, out.name, vid, t))

with open(out_dir / "manifest.csv", "w", newline="") as f:
    csv.writer(f).writerows([("split", "class", "file", "video", "second")] + manifest)
print(len(manifest), "frames")
