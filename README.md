# Who's talking?

A project to detect who is talking when, in audio/video, and mark that up as metadata in captions

Note this is alpha code, it's literally just a first upload to have something to show.

## Purpose

To take an srt file, for example created by whisper.cpp, and add info on who is talking for each segment in the .srt file.

Currently it just takes a modified srt file and outputs another srt file with "Speaker" or "Not speaker" per segment. A segment is a piece of subtitle between two timestamps.

Whisper.cpp actually has a command line flag for diarization, as they call it, but it works poorly in practice: <https://github.com/ggerganov/whisper.cpp/issues/64>

## How it works, high level

It splits a wav file into small parts according to a spec file you've made. It then compares each part to a known speaker in a wav file, and indicates if that speaker is the one speaking. It uses SpeechBrain for that last part, see further down. It uses a speaker sample, i.e. you must have a short wav file with only the speaker you're looking for.

See this tweet for an example: <https://twitter.com/jorgenponder/status/1641948460420145152>

## How it works, lower level

Currently, you need to create a file with the following kind of lines in it:

    00:00:00.000 00:00:05.600 20200424000000
    00:00:05.600 00:00:11.320 20200424000005
    00:00:11.320 00:00:16.720 20200424000011
    00:00:16.720 00:00:25.160 20200424000016
    
This is similar to the timestamps in an .srt file, but with a point instead of a comma as the separator to the millisceonds. This is because ffpmeg uses the dot format. The third item on each line is the global timestamp of the line, i.e. year, date and timestamp. It will be used as the name for the individual wav file that will be classified for who's talking.

If you have a big wav file with a 16k sample rate called ```20200424.wav```, and a file ```20200424.spec``` containing the above lines, split.py will split the wav file into segments based on the timestamps on those lines, each file named after the last item on each line:

    ./bin/python split.py 20200424.wav 20200424.spec
    
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

You will now need to move stuff up from that directory to where virtualenv is. I'm a bit unsure how I did this looking at my bash history. This the iffy step that should have been done differently. Maybe install everything from source or something. Or just change the code below to specify into the speechbrain directory.

Install ipython:

    ./bin/pip install ipython

Start ipython:

    ./bin/ipython

Paste in:

    import torchaudio
    from speechbrain.pretrained import EncoderClassifier, SpeakerRecognition
    classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")
    signal, fs =torchaudio.load('tests/samples/ASR/spk1_snt1.wav')
    embeddings = classifier.encode_batch(signal)

And hit return. I think this step downloads something. Then paste in:

    from speechbrain.pretrained import SpeakerRecognition
    verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
    score, prediction = verification.verify_files("tests/samples/ASR/spk1_snt1.wav", "tests/samples/ASR/spk2_snt1.wav") # Different Speakers

You can then check what is in ```score```. Should be a value below 0.5. Then paste in the line:

    score, prediction = verification.verify_files("tests/samples/ASR/spk1_snt1.wav", "tests/samples/ASR/spk1_snt2.wav") # Same Speaker

Should be a value above 0.5 in ```score```. The above code snipptes taken from: <https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb>

## Roadmap

The different functions will be split into command line programs that work with STDIN and STDOUT.

The first in the chain will take an .srt file and create a spec file for chopping up into segment wav files.

The second will do the actual chopping.

The third will run SpeechBrain over the wav files, with a set of reference wavfiles for speaker identification. Output from this step migh be JSON or WebVTT.

If JSON, there will also be a step to convert that into WebVTT.
