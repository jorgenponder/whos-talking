import sys
import os
import subprocess
from pathlib import Path
import srt

path = "./splitted/"

# SRT looks like this:

# 00:00:00,000 --> 00:00:04,000

# From ffmpeg docs:

# 2.3 Time duration

# There are two accepted syntaxes for expressing time duration.

# [-][HH:]MM:SS[.m...]

# HH expresses the number of hours, MM the number of minutes for a maximum of 2 digits, and SS the number of seconds for a maximum of 2 digits. The m at the end expresses decimal value for SS.

# or

# [-]S+[.m...][s|ms|us]

# S expresses the number of seconds, with the optional decimal part m. The optional literal suffixes ‘s’, ‘ms’ or ‘us’ indicate to interpret the value as seconds, milliseconds or microseconds, respectively.

# In both expressions, the optional ‘-’ indicates negative duration. 

def get_subs(data):
    
    # print(data)
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
        os.mkdir(path)
    except FileExistsError:
        pass
    # record command line args
    original_file = sys.argv[1]

    # create a template of the ffmpeg call in advance
    cmd_string = "ffmpeg -i {original_file} -acodec copy -ss {start} -to {end} {path}{id}.wav"

    for line in get_subs(data):
        id = Path(original_file).stem + line['start'].split('.')[0].replace(':','')
        print(id)
        command = cmd_string.format(original_file=original_file, start=line['start'], end=line['end'], path=path, id=id)
        print(command)

        # use subprocess to execute the command in the shell
        subprocess.call(command, shell=True)

    return None


if __name__ == "__main__":
    main()