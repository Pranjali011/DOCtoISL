from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
from nltk.tokenize import sent_tokenize

# Download punkt tokenizer 
nltk.download("punkt", quiet=True)

# Load a  summarization model
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


# 1. SUMMARIZATION FUNCTION 
def generate_summary(text: str) -> str:
    """
    Summarize long text using DistilBART.
    - If text is short, returns original text.
    - Truncates very long inputs to avoid memory issues.
    """

    if not text:
        return ""

    text = text.strip()

    # If text is too short, just return as-is
    if len(text.split()) < 15:
        return text

    if len(text.split()) > 600:
        text = " ".join(text.split()[:600])

    inputs = tokenizer(
        text,
        truncation=True,
        padding="longest",
        return_tensors="pt"
    )

    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=150,
        min_length=40,
        num_beams=4,
        length_penalty=1.0,
        early_stopping=True,
        no_repeat_ngram_size=3,
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary.strip()


# 2. SPLIT INTO SENTENCES
def split_into_sentences(text: str):
    """
    Split summary into individual sentences.
    """
    try:
        return sent_tokenize(text)
    except Exception:
        return [text]


# 3. SIMPLIFY FOR ISL ( for Basic Rule-Based)
def simplify_sentence(sentence: str) -> str:
    """
    Convert English sentence into ISL-friendly structure.
    Removes helper words, keeps meaningful words.
    """
    sentence = sentence.lower()

    remove_words = ['the', 'is', 'was', 'were', 'a', 'an', 'of', 'to', 'and']
    simplified = " ".join(
        word for word in sentence.split()
        if word not in remove_words
    )

    return simplified.strip()
