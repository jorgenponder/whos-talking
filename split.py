import sys
import subprocess

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

def main():
    """split a wav file into specified segments by calling ffmpeg from the shell"""

    # check command line for original wav file and segment list file
    if len(sys.argv) != 3:
        print("usage: split <original_track> <track_list>")
        exit(1)

    # record command line args
    original_track = sys.argv[1]
    track_list = sys.argv[2]

    # create a template of the ffmpeg call in advance
    cmd_string = "ffmpeg -i {tr} -acodec copy -ss {st} -to {en} {nm}.wav"

    # read each line of the segment list and split into start, end, name
    with open(track_list, "r") as f:
        for line in f:
            # skip comment and empty lines
            if line.startswith("#") or len(line) <= 1:
                continue

            # create command string for a given wav segment
            start, end, nm = line.strip().split()
            command = cmd_string.format(tr=original_track, st=start, en=end, nm=nm)

            # use subprocess to execute the command in the shell
            subprocess.call(command, shell=True)

    return None


if __name__ == "__main__":
    main()