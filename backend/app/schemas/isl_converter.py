import re

# 1. CLEAN WORD
def clean_word(word: str) -> str:
    """
    Remove punctuation and convert to lowercase.
    Keep only alphabets.
    """
    word = word.lower()
    word = re.sub(r"[^a-z]", "", word)  # keep only letters
    return word.strip()


# 2. WORD → LETTERS 
def word_to_isl_letters(word: str) -> list:
    """
    Convert a word into a list of letters (A-Z).
    Example: 'water' → ['W','A','T','E','R']
    """

    word = clean_word(word)

    if not word:
        return []

    return list(word.upper())


# 3. FULL SENTENCE → LIST OF WORD LETTER LISTS
def sentence_to_isl(sentence: str) -> list:
    """
    Convert a full sentence into ISL (alphabet spelling).
    
    Example:
    "water essential"
    
    Output:
    [
        ['W','A','T','E','R'],
        ['E','S','S','E','N','T','I','A','L']
    ]
    """

    words = sentence.split()
    isl_output = []

    for word in words:
        letters = word_to_isl_letters(word)
        if letters:
            isl_output.append(letters)

    return isl_output
