import os
import json
from pathlib import Path

def get_references(references_arg):
    references = []
    node_spec = Path(references_arg)
    if os.path.isdir(node_spec):
        for filename in os.listdir(node_spec):
            if filename.endswith('.wav'):
                references.append({'file':str(node_spec.absolute().joinpath(filename)), 'speaker':Path(filename).stem})
    elif os.path.isfile(node_spec):
        if references_arg.endswith('.wav'):
            references.append({'file':str(node_spec.absolute()), 'speaker':Path(references_arg).stem})
        elif node_spec.suffix in ('.json','.jsn'):
            fo = open(node_spec)
            references = json.load(fo)
            for reference in references:
                reference['file'] = str(node_spec.absolute().parent.joinpath(reference['file']))
            fo.close()
    return references

def get_wav_segments(dir_path):
    dir_spec = Path(dir_path)
    filenames = []
    for filename in os.listdir(dir_spec):
        if filename.endswith('.wav'):
            filenames.append(str(dir_spec.absolute().joinpath(filename)))
    filenames.sort()
    return filenames