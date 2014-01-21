

def match(text, pattern, base=10):
    text_len = len(text)
    pattern_len = len(pattern)
    text_hash = _get_hash(text[:pattern_len], base)
    pattern_hash = _get_hash(pattern, base)
    matches = []

    for i in xrange(text_len - pattern_len + 1):
        if pattern_hash == text_hash:
            # If the hashes match, we also need to check if the text substring
            # and the pattern are the same. Hash matches can be result of
            # collisons.
            if pattern == text[i:i + pattern_len]:
                matches.append(i)

        if i >= text_len - pattern_len:
            break

        # Text hash considering only the most significant digit.
        text_hash_msd_only = ord(text[i]) * base ** (pattern_len - 1)

        # Note that we do not multiply the exponent of the base for the second
        # term in the summation because the exponent for the least significant
        # digit is 0.
        text_hash = (base * (text_hash - text_hash_msd_only) +
                     ord(text[i + pattern_len]))

    return matches


def _get_hash(text, base):
    text_hash = 0
    for i in xrange(len(text)):
        text_hash = text_hash + (ord(text[-i - 1]) * base ** i)

    return text_hash
