"""Test a trained classifier on the held-out video: confusion matrix on the test folders, and a
second-by-second timeline over the whole video compared with the PitVis labels.

usage: eval_cls.py <weights.pt> <test_dir> <annotations.csv> <video.mp4> <out_dir>
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from ultralytics import YOLO

weights, test_dir, ann, video, out_dir = sys.argv[1], Path(sys.argv[2]), sys.argv[3], sys.argv[4], Path(sys.argv[5])
out_dir.mkdir(parents=True, exist_ok=True)
model = YOLO(weights)
names = model.names  # index -> class name
order = ["suction", "kerrison", "none"]

# 1) test folders: confusion matrix
cm = np.zeros((3, 3), int)
examples = []
for t, cls in enumerate(order):
    for p in sorted((test_dir / cls).glob("*.jpg")):
        r = model(str(p), verbose=False)[0]
        pred = names[int(r.probs.top1)]
        cm[t, order.index(pred)] += 1
        examples.append({"file": p.name, "true": cls, "pred": pred, "conf": round(float(r.probs.top1conf), 3)})
acc = np.trace(cm) / cm.sum()
print("test accuracy", round(acc, 3))
print("confusion (rows true, cols predicted)", order)
print(cm)

# 2) whole video, one frame per second
frames = out_dir / "video_frames"
frames.mkdir(exist_ok=True)
if not any(frames.iterdir()):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-i", video, "-vf", "fps=1,crop=720:720:267:0,scale=224:224",
                    "-q:v", "3", str(frames / "s%05d.jpg")], check=True)
truth = {}
for r in csv.DictReader(open(ann)):
    a, b = int(r["int_instrument1"]), int(r["int_instrument2"])
    truth[int(r["int_time"])] = ("suction" if a == 16 and b == -2 else "kerrison" if a == 8 and b == -2
                                 else "none" if a == 0 else "other" if a > 0 else "outside")
timeline = []
paths = sorted(frames.glob("*.jpg"))
for i in range(0, len(paths), 64):
    for p, r in zip(paths[i:i + 64], model([str(p) for p in paths[i:i + 64]], verbose=False)):
        sec = int(p.stem[1:]) - 1  # ffmpeg numbers from 1; frame n shows second n-1
        timeline.append((sec, truth.get(sec, "outside"), names[int(r.probs.top1)], round(float(r.probs.top1conf), 3)))
with open(out_dir / "timeline.csv", "w", newline="") as f:
    csv.writer(f).writerows([("second", "truth", "pred", "conf")] + timeline)
scored = [(t, p) for _, t, p, _ in timeline if t in order]
print("timeline seconds scored", len(scored), "agreement", round(np.mean([t == p for t, p in scored]), 3))
json.dump({"test_accuracy": float(acc), "cm": cm.tolist(), "order": order, "examples": examples},
          open(out_dir / "eval.json", "w"), indent=1)
