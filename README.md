# Who's talking?

A project to detect who is talking when, in audio/video, and mark that up as metadata in captions

Note this is alpha code.

## Purpose

To take an srt file, for example created by whisper.cpp, and add info on who is talking for each segment in the .srt file.

Currently it takes an srt file and its corresponding video or audio file and outputs another srt file with the speaker's name or "unknown speaker" per segment. A segment in this project is a piece of subtitle with a start and an end timestamp. Each segment is assumed to only have one speaker in it.

Whisper.cpp actually has a command line flag for diarization, as they call it, but it works poorly in practice: <https://github.com/ggerganov/whisper.cpp/issues/64>

## Syntax

split.py:

    ./bin/python split.py transcript.srt video.mp4

The split files will end up in a subdirectory called ```split-segments```.

identify.py:

    options:
    -h, --help            show this help message and exit
    -r REFERENCES, --reference-files REFERENCES
                            Where to get reference voice files from. If directory or file, the filename(s) without suffix
                            will be used as id for that speaker. If file, only that file will be used. If value is a file
                            with the .txt or .lst extension, it will be interpreted as a file with lines, specifying
                            speakers in order of priority. If the file extension is JSON, it will be intrepreted with name
                            and filepath properties to get reference voice files from.
    -w SEGMENTS_DIR, --wav-segments SEGMENTS_DIR

You should be able to supply a directory of speaker samples also, a bit untested right now. And also in JSON format, see source in "./helpers":

    ./bin/python identify.py -r "speaker-samples-dir"
    ./bin/python identify.py -r "speaker-samples-list.json"


## How it works, high level

It splits a wav file into small parts from an srt file, for example made by whisper.cpp. It then compares each part to a known speaker in a wav file, and indicates if that speaker is the one speaking. It uses SpeechBrain for that last part, see further down. It uses a speaker sample, i.e. you must have a short wav file with only the speaker you're looking for.

See this tweet for an example: <https://twitter.com/jorgenponder/status/1641948460420145152>

## Install SpeechBrain

This project relies on SpeechBrain. Here is one way to install it. It's not the smartest way to do it but I prefer to specify the way I did that worked, instead of an optimized way I haven't tried yet. Instructions for Ubuntu, but should work under most OSes.

Make a directory with virtualenv:

    virtualenv .

Install SpeechBrain:

    ./bin pip install speechbrain

Clone SpeechBrain:

    git clone git@github.com:speechbrain/speechbrain.git

Install ipython:

    ./bin/pip install ipython

Start ipython:

    ./bin/ipython

Then paste in:

    from speechbrain.pretrained import SpeakerRecognition
    verification = SpeakerRecognition.from_hparams(source="speechbrain/speechbrain/spkrec-ecapa-voxceleb", savedir="speechbrain/pretrained_models/spkrec-ecapa-voxceleb")
    score, prediction = verification.verify_files("speechbrain/tests/samples/ASR/spk1_snt1.wav", "speechbrain/tests/samples/ASR/spk2_snt1.wav") # Different Speakers

You can then check what is in ```score```. Should be a value below 0.5. Then paste in the line:

    score, prediction = verification.verify_files("speechbrain/tests/samples/ASR/spk1_snt1.wav", "speechbrain/tests/samples/ASR/spk1_snt2.wav") # Same Speaker

Should be a value above 0.5 in ```score```. The above code snippets slightly modified from: <https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb>

## Benchmarks

30 minutes of split audio seemed to give about 110MB of wav files.

On an AMD Ryzen 4000 series 5 laptop:

The time to split the 30 minute mp4 file into 320 segments was 6 minutes. This included converting from 44.1KHz aac.

The time to identify one speaker only, across 320 segments was 4½ minutes with a 27s identifying file. The speaker was identified in 168 segments.

With a 6s identifying file, it took 2½ minutes
The 6s file had one difference that could go either way, compared to the 27s file.

With a 3s identifying file, it took 2 minutes
The 3s file had one false negative, and one that could go either way (same as the 6s file), compared to the 27s file. If we assume the 27s file is correct then this is about 0.6% worse recall.

Using a different 3s file, there was one false negative. A different one than with the first 3s file. Possibly, this could mean that 3s is not enough to capture enough voice characteristics.

An aac file at 16KHz seems to be 5x to 6x smaller than a wav file. So for long-time storage of audio segments, maybe aac can be an option.

## Anomalies

SpeechBrain seems to create a lot of symlinked wav files. In fact hundreds of them. This may be some kind of handling error from my side. Not sure.

## Roadmap

To implement some heuristics, that if a speaker has not been heard for the first 2 minutes or so, they are likely not in that video at all, and can be disabled as a reference file to be compared with.

This could possibly be controlled in a speakers.json file:

    [{"name":"John Doe", "file":"johndoe.wav", "omit if not detected within":120}]
