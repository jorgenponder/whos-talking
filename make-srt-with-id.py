import os

from speechbrain.pretrained import SpeakerRecognition

dir_path = '/path/to/wav/files'
reference_file = '/path/to/reference/wav/files/for/speaker.wav'

def get_score(reference_file, line):
    verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
    score, prediction = verification.verify_files(reference_file, line)
    return score

def get_files(dir_path):
    filenames = []
    for filename in os.listdir(dir_path):
        if filename.endswith('.wav'):
            filenames.append(filename)
    filenames.sort()
    return filenames

timecode = None
text = ""

lines = get_files(dir_path)

for number, line in enumerate(lines):
    hours, minutes, seconds = line[8:10], line[10:12], line[12:14]
    if timecode:
        timecode += ' --> %s:%s:%s\n' % (hours, minutes, seconds)
        print(timecode + ' ' + text + '\n\n')
    timecode = '%s\n%s:%s:%s' % (number, hours, minutes, seconds)
    score = get_score(reference_file, dir_path + '/'+ line)
    if score > 0.5:
        text = "Speaker"
    else:
        text = "Another speaker"



