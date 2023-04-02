# Who's talking?

A project to detect who is talking when, in audio/video, and mark that up as metadata in captions

Note this is alpha code.

## Purpose

To take an srt file, for example created by whisper.cpp, and add info on who is talking for each segment in the .srt file.

Currently it just takes an srt file and outputs another srt file with "Speaker" or "Not speaker" per segment. A segment in this project is a piece of subtitle with an start and an end timestamp. Each segment is assumed to only have one speaker in it.

Whisper.cpp actually has a command line flag for diarization, as they call it, but it works poorly in practice: <https://github.com/ggerganov/whisper.cpp/issues/64>

## How it works, high level

It splits a wav file into small parts from an srt file, for example made by whisper.cpp. It then compares each part to a known speaker in a wav file, and indicates if that speaker is the one speaking. It uses SpeechBrain for that last part, see further down. It uses a speaker sample, i.e. you must have a short wav file with only the speaker you're looking for.

See this tweet for an example: <https://twitter.com/jorgenponder/status/1641948460420145152>

## How it works, lower level

You need one srt file that contains the video or sound file. Each segment must have an end timestamp and not just a start timestamp.

If you have a video file called ```20200424.mp4```, and a file ```20200424.srt``` containing the segments, split.py will split the mp4 file into wav segments based on the timestamps from those segments:

    cat 2020-04-24.srt | ./bin/python split.py 20200424.mp4
    
Once you have all those wav files, you can run ```./bin python make-srt-with-id.py```. First you must change the specifications in ```make-srt-with-id.py``` to match where the wav files are, and where the speaker sample is.

./bin/python make-srt-with-id.py

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

## Roadmap

The different functions will be split into command line programs that work with STDIN and STDOUT.

The first in the chain will take an .srt file and create a spec file for chopping up into segment wav files.

The second will do the actual chopping.

The third will run SpeechBrain over the wav files, with a set of reference wavfiles for speaker identification. Output from this step migh be JSON or WebVTT.

If JSON, there will also be a step to convert that into WebVTT.

## Benchmarks

30 minutes of split audio seemed to give about 110MB wav files.

The time to split the file into 320 segments was 6 minutes. This included converting from 44.1KHz aac.

The time to speaker identify the speaker in 320 segments was 5 minutes looking for one speaker.


An aac file at 16KHz seems to be 5x to 6x smaller than a wav file. So for long-time storage of audio segments, maybe aac can be an option.
