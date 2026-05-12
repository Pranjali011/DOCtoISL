import os
import uuid
from wordcloud import WordCloud
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt

# Directory to save wordcloud images
WORDCLOUD_DIR = "generated_wordclouds"
os.makedirs(WORDCLOUD_DIR, exist_ok=True)


def generate_wordcloud(text: str) -> str:
    """
    Generate a word cloud image from text.
    Returns path to saved image.
    """

    if not text or not text.strip():
        return ""

    # Clean and normalize text
    cleaned_text = " ".join(text.split())

    # Remove problematic characters
    safe_text = "".join(c for c in cleaned_text if c.isalnum() or c.isspace())

    # Create WordCloud object
    wc = WordCloud(
        width=1200,
        height=800,
        background_color="white",
        collocations=False
    ).generate(safe_text)

    # Create unique filename
    unique_id = uuid.uuid4().hex[:10]
    filename = f"wc_{unique_id}.png"

    output_path = os.path.join(WORDCLOUD_DIR, filename)

    try:
        plt.figure(figsize=(10, 6))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

    except Exception as e:
        print(f"[WORDCLOUD ERROR] {e}")
        return ""

    return output_path
