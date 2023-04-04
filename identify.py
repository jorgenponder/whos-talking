from pathlib import Path
from speechbrain.pretrained import SpeakerRecognition

from helpers import args

def try_purge(voice, reference_voices, omitters, total_seconds):
    """Optimization: Deletes a voice from reference_voices if it did not turn up early enough in the show. Only done with voices indicated ok to do so with, i.e. in "omitters", e.g. alternating hosts of a show."""
    if not omitters:
        return reference_voices, omitters
    voice_id = voice['file']
    if voice_id in omitters:
        if omitters[voice_id] < total_seconds: # if appearance is early enough
            del omitters[voice_id] # then it should not be in omitters anymore
        else:
            # otoh if still in omitters, it hasn't appeared within the 
            # threshold seconds, so stop using that voice in the search space
            print('deleted one voice')

            del reference_voices[voice]
    return reference_voices, omitters


def get_score(reference_file, line):
    verification = SpeakerRecognition.from_hparams(source="speechbrain/speechbrain/spkrec-ecapa-voxceleb", savedir="speechbrain/pretrained_models/spkrec-ecapa-voxceleb")
    try:
        score, prediction = verification.verify_files(reference_file, line)
    except RuntimeError:
        print((reference_file, line))
        raise
    return score


def identify():
    wav_segments, reference_voices, omitters = args.get_params()
    print(reference_voices)
    timecode = None
    text = ""
    for ordinal, wav_segment in enumerate(wav_segments):
        line = Path(wav_segment).stem
        # print(line)
        hours, minutes, seconds = line[8:10], line[10:12], line[12:14]
        total_seconds = 3600 * int(hours) + 60 * int(minutes) + int(seconds)
        if timecode:
            timecode += ' --> %s:%s:%s\n' % (hours, minutes, seconds)
            print(timecode + ' ' + text + '\n\n')
        timecode = '%s\n%s:%s:%s' % (ordinal, hours, minutes, seconds)
        for voice in reference_voices:
            reference_voices, omitters = try_purge(voice, reference_voices, omitters, total_seconds)
            if not reference_voices:
                print('no voices left to test against, exiting…')
                return
            score = get_score(voice['file'], wav_segment)
            if score > 0.5:
                text = voice['speaker']
                break
            text = "unidentified speaker"

identify()




