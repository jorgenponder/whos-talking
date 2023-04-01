# Who's talking?

A project to detect who is talking when in audio/video and mark that up as metadata in captions

## Install SpeechBrain

Thirs project relies on SpeechBrain. Here is one way to install it. It's not the smartest way to do it but I prefer to specify the way I did that worked, instead of an optimized way I haven't tried yet. Instructions for Ubuntu, but should work under most OSes.

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
