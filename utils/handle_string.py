def extract_command(text):
    tokens = text.split(' ', 1)
    if len(tokens) > 1:
        return ' '.join(tokens[1:])
    return ''
