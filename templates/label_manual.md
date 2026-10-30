# Label manual: [project name]

Version [1.0] · Date [ ] · Owner [surgeon champion]

Keep this to one page. Every labeler reads it before the first frame, and any change gets a new version number.

## 1. The question
In one sentence, what should the model answer?
> Example: "Which instrument is in view: suction, Kerrison or none?"

## 2. Image source
- Modality: [endoscope / microscope / exoscope / ultrasound / smear]
- Frames: [1 per second], cropped to [the scope circle]
- Excluded: [out-of-body frames, blurred frames, menus on screen]

## 3. Classes
| Class | Include when | Do not include when | Example frame |
|---|---|---|---|
| [suction] | [tip visible, alone in view] | [two instruments in view] | [file name] |
| [kerrison] | | | |
| [none] | [inside the patient, no instrument] | [scope outside the patient] | |

## 4. Hard cases
[Write down each rule the first time you meet a hard case, for example "instrument only half in view", "instrument blurred", "smoke".]

## 5. Split by patient
- Train: [cases]
- Tune (validation): [cases]
- Test, never seen: [cases]

No patient appears in more than one split.

## 6. Agreement check
- Two labelers independently label the same [10%] of frames.
- Report agreement (percent agreement and Cohen's κ).
- Discuss disagreements, update this manual, and re-label if the rules changed.

## 7. Log
| Date | Labeler | Cases | Frames | Notes |
|---|---|---|---|---|
| | | | | |
