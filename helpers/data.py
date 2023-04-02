

def get_references(args):
    references_arg = args.REFERENCES
    references = []
    if os. path.isdir(references_arg):
        for filename in os.listdir(references_arg):
            if filename.endswith('.wav'):
                references.append({'file':filename, 'speaker':Path(filename).stem})
    elif os.path.isfile(references_arg):
        if references_arg.endswith('.wav'):
            references.append({'file':references_arg, 'speaker':Path(references_arg).stem})
        elif Path(references_arg).suffix in ('txt','lst','spec'):
            pass
        elif Path(references_arg).suffix in ('json','jsn'):
            references = json.load(references_arg)
    return references

def get_files(dir_path):
    filenames = []
    for filename in os.listdir(dir_path):
        if filename.endswith('.wav'):
            filenames.append(filename)
    filenames.sort()
    return filenames