import json, sys

DOC = '''Uses SpeechBrain to identify for each WAV segment who is speaking. It gets JSON on STDIN with info on the location of the directory with WAV files.

It ouputs JSON with an array of objects, where each object has an id and a speaker property. Id is taken as the file name of the WAV segment file, witout the .wav extension'''


import argparse
def get_args():
    parser = argparse.ArgumentParser(description=DOC)
    parser.add_argument("-r", "--reference-files", required = True, dest="REFERENCES",help="Where to get reference voice files from. If directory or file, the filename(s) without suffix will be used as id for that speaker. If file, only that file will be used. If value is a file with the .txt or .lst extension, it will be interpreted as a file with lines, specifying speakers in order of priority. If the file extension is JSON, it will be intrepreted with name and filepath properties to get reference voice files from.")
    parser.add_argument('--indata', dest="INDATA", default=sys.stdin)
    args = parser.parse_args()
    stdin_json = ''.join(args.INDATA.readlines())
    stdin_data = json.loads(stdin_json)
    dir_path = stdin_data['dir_path']
    return({'reference_voices':args.REFERENCES, 'dir_path':dir_path})