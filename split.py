import sys
import os
import subprocess
from pathlib import Path
import srt

out_path = "./splitted/"

def get_subs(data):
    """ """
    subs = []
    for sub in srt.parse(data):
        # use case is no subs 10 hours or longer
        start = "0" + str(sub.start)
        end = "0" + str(sub.end)
        subs.append({'start':start, 'end':end})
    return subs

def main():
    """split a wav file into specified segments by calling ffmpeg from the shell"""

    # check command line for original wav file and segment list file
    if len(sys.argv) != 2:
        print("usage: split <original_file>")
        exit(1)
    data = ''.join(sys.stdin.readlines())
    try:
        os.mkdir(out_path)
    except FileExistsError:
        pass
    # record command line args
    original_file = sys.argv[1]

    # create a template of the ffmpeg call in advance
    cmd_string = "ffmpeg -y -i {original_file} -acodec copy -ss {start} -to {end} {out_path}{id}.wav"

    for line in get_subs(data):
        id = Path(original_file).stem + line['start'].split('.')[0].replace(':','')
        print(id)
        command = cmd_string.format(original_file=original_file, start=line['start'], end=line['end'], out_path=out_path, id=id)
        print(command)

        # use subprocess to execute the command in the shell
        subprocess.call(command, shell=True)

    return None


if __name__ == "__main__":
    main()