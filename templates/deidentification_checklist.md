# De-identification checklist for operative video

Use this before any video or frame leaves the computer it was recorded on. Your institution's policy and IRB come first; this list does not replace them. In the US, HIPAA de-identification is either Safe Harbor (all 18 identifiers removed) or Expert Determination.

## Picture
- [ ] **Out-of-body frames removed.** When the endoscope or camera is outside the patient, it records faces, staff and the room. Cut these segments, or use a tool that detects them (for example Endoshare, which is free).
- [ ] **Burned-in overlay text removed or blacked out:** patient name, ID or medical record number, date of birth, date and time of surgery, hospital name.
- [ ] **Monitors, whiteboards and paperwork in view** are cropped or blurred.
- [ ] **Distinguishing marks** such as tattoos or unusual anatomy that could identify the patient are considered.

## Sound
- [ ] **Audio track removed.** Room audio often contains names.

## File
- [ ] **File names pseudonymized** (for example `case_017.mp4`, not a name, medical record number or date).
- [ ] **Metadata stripped**, such as creation date, device serial number and GPS (for example `ffmpeg -i in.mp4 -map_metadata -1 -an -c:v copy out.mp4`, which also drops audio).
- [ ] **Key file**, linking pseudonyms to patients, stored separately on a secure hospital drive, or not kept at all.

## Where it goes
- [ ] **Green:** identifiable video stays on hospital computers; labeling and training run offline.
- [ ] **Amber:** de-identified video leaves only with IRB approval and a data agreement (BAA).
- [ ] **Red, never:** consumer chatbots, public or free-tier cloud projects, personal drives, messaging apps, or USB sticks that leave the hospital.

Checked by: __________  Date: __________
