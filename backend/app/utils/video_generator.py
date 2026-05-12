import os
import uuid
from moviepy.editor import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)
from PIL import Image


DATASET_PATH = os.getenv("DATASET_PATH", "ISL_Dataset")

# Output directory
OUTPUT_DIR = "generated_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# GET LETTER IMAGE 
def get_letter_image(letter: str):
    folder = os.path.join(DATASET_PATH, letter.upper())

    if not os.path.exists(folder):
        print(f"[ERROR] Missing folder for letter: {letter}")
        return None

    possible_files = ["0.jpg", "0.jpeg", "0.png", "1.jpg", "1.png"]

    for f in possible_files:
        img_path = os.path.join(folder, f)
        if os.path.exists(img_path):
            return img_path

    print(f"[WARNING] No valid image inside: {folder}")
    return None


# Resize image to constant video size
def resize_image(image_path: str, size=(720, 720)):
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize(size)
        temp_path = f"{image_path}_temp.png"
        img.save(temp_path)
        return temp_path
    except Exception as e:
        print(f"[ERROR] Image resize failed: {e}")
        return None


# Generate ISL Video with WORD TITLE + WHITE SEPARATOR
def generate_isl_video(sentence: str) -> str:
    """
    Convert a sentence into an ISL video
    with clear white separators and a TITLE frame for each word.
    """

    clean_sentence = "".join(
        c for c in sentence.upper() if c.isalnum() or c == " "
    )
    words = clean_sentence.split()

    clips = []

    for word in words:

       
        # 1️ WORD TITLE FRAME (white background + text)
        
        white_bg = Image.new("RGB", (720, 720), (255, 255, 255))
        bg_path = os.path.join(OUTPUT_DIR, "word_bg.jpg")
        white_bg.save(bg_path)

        try:
            title = TextClip(
                txt=word,
                fontsize=120,
                color='black',
                font='Arial-Bold'
            ).set_position("center").set_duration(1)
        except Exception:
            # fallback if Arial-Bold is not installed
            title = TextClip(
                txt=word,
                fontsize=120,
                color='black'
            ).set_position("center").set_duration(1)

        title_frame = CompositeVideoClip([
            ImageClip(bg_path).set_duration(1),
            title
        ])
        clips.append(title_frame)

        
        # 2️ LETTER-BY-LETTER ISL IMAGES
        
        for char in word:
            if char.isalpha():

                img_path = get_letter_image(char)
                if not img_path:
                    continue

                resized = resize_image(img_path)
                if not resized:
                    continue

                isl_clip = ImageClip(resized).set_duration(0.6)
                clips.append(isl_clip)

        
        # 3️ WHITE SEPARATOR FRAME
        
        separator = Image.new("RGB", (720, 720), (255, 255, 255))
        sep_path = os.path.join(OUTPUT_DIR, "separator.jpg")
        separator.save(sep_path)

        sep_clip = ImageClip(sep_path).set_duration(0.4)
        clips.append(sep_clip)

    
    # FINAL VALIDATION
    
    if not clips:
        print("[ERROR] No clips generated.")
        return None

    final_video = concatenate_videoclips(clips, method="compose")

    # Unique filename
    uid = uuid.uuid4().hex[:8]
    safe_name = clean_sentence.replace(" ", "_")[:20]
    output_path = os.path.join(OUTPUT_DIR, f"{safe_name}_{uid}.mp4")

    # Export video
    final_video.write_videofile(
        output_path,
        fps=2,
        codec="libx264",
        audio=False
    )

    return output_path
