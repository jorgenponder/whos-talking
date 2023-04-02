import sys
import os
import subprocess
from pathlib import Path
import srt

out_path = "./split-segments/"

def get_subs(data):
    """ """
    subs = []
    for sub in srt.parse(data):
        start = str(sub.start)
        end = str(sub.end)
        if start[1] == ":":
            start = '0' + start
        if end[1] == ":":
            end = '0' + end
        subs.append({'start':start, 'end':end})
        print(subs)
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
    cmd_string = "ffmpeg -y -i {original_file} -acodec pcm_s16le -ar 16000 -ss {start} -to {end} {out_path}{id}.wav"

    for line in get_subs(data):
        id = Path(original_file).stem + line['start'].split('.')[0].replace(':','')
        # FIXME, make sure start is left padded with a zero
        # print(id)
        command = cmd_string.format(original_file=original_file, start=line['start'], end=line['end'], out_path=out_path, id=id)
        # print(command)

        # use subprocess to execute the command in the shell
        subprocess.call(command, shell=True)
    print(out_path)
    return None


if __name__ == "__main__":
    main()