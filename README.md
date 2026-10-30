# Computer vision in intraoperative imaging: a starter kit

Companion to the talk **"Computer Vision Applications in Intraoperative Imaging: Where to Start?"**
CNS Annual Meeting, Washington DC, 31 October 2026, by Dr. Bhushan D. Thombre.

The kit lets a neurosurgeon train and honestly test a first model on public surgical video in an afternoon, on a laptop, with free tools. No patient data are included.

## What's inside

| Folder | Contents |
|---|---|
| `scripts/` | The exact scripts used for the tutorial in the talk |
| `templates/label_manual.md` | A one-page label manual to copy and fill in |
| `templates/deidentification_checklist.md` | What to remove from operative video before it leaves your computer |
| `resources.md` | Key papers (with DOIs) and public neurosurgical video datasets |

## The tutorial: which instrument is in view?

The task is to classify frames as **suction**, **Kerrison** or **none**, using endoscopic pituitary video from the public PitVis dataset.

### 1. Get video

Download PitVis from the UCL Research Data Repository: <https://doi.org/10.5522/04/26531686>. It has 25 videos, plus `annotations_XX.csv` with the step and the instrument for every second. Licence: CC BY-NC-SA 4.0, for research and teaching only.

The talk used videos 03, 07 and 25 for training, 22 for tuning and 23 as the never-seen test case.

### 2–3. Extract frames and sort them into class folders

This needs Python 3 and ffmpeg (`brew install ffmpeg` on a Mac).

```bash
python3 scripts/make_cls_dataset.py pitvis/ pitvis/ pitvis_instruments/ \
  03:train:60 07:train:60 25:train:60 22:val:30 23:test:40
```

The script picks evenly spaced seconds for each label from the PitVis annotation files and saves one frame per second. Each frame is cropped to the endoscope circle and written to `pitvis_instruments/{train,val,test}/{suction,kerrison,none}/`. The folder name is the label.

**Rule:** a patient's frames go into one split only. Neighbouring frames are near-copies, so a frame-level split turns the test into a memory test.

### 4a. Train without code (Mac)

Open **Create ML** (free with Xcode), choose New project → Image Classification, and drag in the `train`, `val` and `test` folders. Press **Train**, then read the **Evaluation** tab.

To get the same result from a script: `swift scripts/createml_train.swift pitvis_instruments/ model.mlmodel`

A browser alternative is Teachable Machine: make one class per folder and upload that folder's images.

### 4b. Train with code

```bash
pip install ultralytics
yolo classify train model=yolo26n-cls.pt data=pitvis_instruments epochs=30 imgsz=224
yolo classify val model=runs/classify/train/weights/best.pt data=pitvis_instruments split=test
```

### 5–6. Test on the unseen case, then run on the whole operation

```bash
python3 scripts/eval_cls.py runs/classify/train/weights/best.pt pitvis_instruments/test \
  pitvis/annotations_23.csv pitvis/video_23.mp4 results_23/
```

This writes a confusion matrix for the test frames, plus `timeline.csv`, which classifies every second of video 23 and compares it with the surgeons' labels.

### Results in the talk (MacBook, Apple M4 Pro, October 2026)

| | Training frames | Video 22 (tuning) | Video 23 (never seen) | Training time |
|---|---|---|---|---|
| No-code (Create ML, default settings) | 100% | 64% | 48% | 4 s |
| Code (YOLO26n-cls, 30 epochs) | 100% | 81% | 78% | 1.8 min |

Across every second of video 23 that had one of the three labels (2,285 s), the code model agreed with the surgeons 69% of the time. Its main error was calling Kerrison frames "suction".

The same recipe on open-microscope aneurysm clipping video (MACS dataset, three training patients) scored 51%, a coin flip. The dataset's authors reached about 81% with 12 training videos. How much data you need depends on how hard the question is.

### Boxes instead of whole-frame labels

`scripts/click_to_box.py` shows the one-click method: click once on each instrument, SAM 2 draws the outline, and the script writes the box and a YOLO label line. When we tried placing the clicks automatically, about half the boxes landed on bone or a cottonoid. A surgeon still has to check every box.

## Before you use your own patients' video

- Ask your IRB and your IT or privacy office first.
- De-identify the video (see `templates/deidentification_checklist.md`).
- Keep identifiable video on hospital computers. Train offline.
- Test on patients the model has never seen, and report the misses.

## Licences and disclaimers

The scripts in this kit are released under the MIT licence. The tools they call keep their own licences: Ultralytics YOLO is AGPL-3.0 (free for research; commercial products need a licence), and SAM 2 is Apache 2.0. Datasets keep their own licences (PitVis CC BY-NC-SA 4.0; MACS CC BY-NC 4.0).

Tool names are examples for teaching, not endorsements. This kit is for research and education. It is not a medical device and must not guide patient care.

Contact: Dr. Bhushan D. Thombre
