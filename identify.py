import os
from pathlib import Path
import json
from helpers import files, args

from speechbrain.pretrained import SpeakerRecognition

def get_score(reference_file, line):
    verification = SpeakerRecognition.from_hparams(source="speechbrain/speechbrain/spkrec-ecapa-voxceleb", savedir="speechbrain/pretrained_models/spkrec-ecapa-voxceleb")
    score, prediction = verification.verify_files(reference_file, line)
    return score


timecode = None
text = ""
context = args.get_args()
wav_segments = files.get_wav_segments(context['dir_path'])
reference_voices = files.get_references(context['reference_voices'])
print(reference_voices)

# loop over wav files
for number, wav_segment in enumerate(wav_segments):
    line = Path(wav_segment).stem
    # print(line)
    hours, minutes, seconds = line[8:10], line[10:12], line[12:14]
    if timecode:
        timecode += ' --> %s:%s:%s\n' % (hours, minutes, seconds)
        print(timecode + ' ' + text + '\n\n')
    timecode = '%s\n%s:%s:%s' % (number, hours, minutes, seconds)
    for speaker_candidate in reference_voices:
        score = get_score(speaker_candidate['file'], wav_segment)
        if score > 0.5:
            text = speaker_candidate['speaker']
            break
        text = "unidentified speaker"



