import argparse

from helpers import files

DOC = '''Uses SpeechBrain to identify for each WAV segment who is speaking.

 Id is taken as the file name of the WAV segment file, witout the .wav extension'''

def get_args():
    parser = argparse.ArgumentParser(description=DOC)
    parser.add_argument("-r", "--reference-files", required = True, dest="REFERENCES",help="Where to get reference voice files from. If directory or file, the filename(s) without suffix will be used as id for that speaker. If file, only that file will be used. If value is a file with the .txt or .lst extension, it will be interpreted as a file with lines, specifying speakers in order of priority. If the file extension is JSON, it will be intrepreted with name and filepath properties to get reference voice files from.")
    parser.add_argument('-w','--wav-segments', required = True, dest = "SEGMENTS_DIR" )
    args = parser.parse_args()
    dir_path = args.SEGMENTS_DIR
    return({'reference_voices':args.REFERENCES, 'dir_path':dir_path})

def get_omitters(reference_voices):
    """Builds up a dictionary of after how many seconds into a show voices not found should be omitted from the search space. Used e.g. to filter out alternating hosts not present."""
    omitters = {}
    for voice in reference_voices:
        if 'omit if not detected within' in voice:
            omitters[voice['file']] = voice['omit if not detected within']
    return omitters

def get_params():
    context = get_args()
    wav_segments = files.get_wav_segments(context['dir_path'])
    reference_voices = files.get_references(context['reference_voices'])
    print(reference_voices)
    omitters = get_omitters(reference_voices)
    return wav_segments,reference_voices,omitters
