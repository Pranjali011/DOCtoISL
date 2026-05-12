import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Directory  word clouds will be saved
WORDCLOUD_DIR = "generated_wordclouds"
os.makedirs(WORDCLOUD_DIR, exist_ok=True)


def generate_wordcloud(text: str) -> str:
    """
    Generate a word cloud image from a given text.
    Saves the image and returns its file path.
    """

    if not text or not text.strip():
        return ""

    # Clean text 
    cleaned_text = " ".join(text.split())

    # Create WordCloud object
    wc = WordCloud(
        width=1200,
        height=800,
        background_color="white",
        collocations=False
    ).generate(cleaned_text)

    # Output file name
    filename = cleaned_text[:10].replace(" ", "_").lower() + "_wc.png"
    output_path = os.path.join(WORDCLOUD_DIR, filename)

    # Save image using matplotlib
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    return output_path
