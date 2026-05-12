import os
import uuid
import random
import cv2

DATASET_PATH = os.path.join(os.getcwd(), "ISL_Dataset")

# Output folder for ISL videos
OUTPUT_VIDEO_DIR = os.path.join(os.getcwd(), "generated_videos")
os.makedirs(OUTPUT_VIDEO_DIR, exist_ok=True)


# 1. Simplify English sentence for ISL grammar
def simplify_sentence(sentence: str) -> str:
    remove_words = {"is", "am", "are", "the", "of", "to", "a", "an", "and", "in", "on"}
    words = sentence.lower().split()
    simplified = [w for w in words if w not in remove_words]
    return " ".join(simplified)


# 2. Convert simplified sentence → list of uppercase letters
def sentence_to_letters(sentence: str):
    letters = []
    for ch in sentence:
        if ch.isalpha():
            letters.append(ch.upper())   
    return letters


# 3. Select  random gesture images 

def get_letter_images(letter: str, max_frames: int = 5):
    folder_path = os.path.join(DATASET_PATH, letter.lower())

    if not os.path.isdir(folder_path):
        print(f"[WARNING] Missing folder for letter: {letter} → {folder_path}")
        return []

    files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(("jpg", "jpeg", "png"))
    ]

    if not files:
        print(f"[WARNING] No images found in {folder_path}")
        return []

    selected_files = random.sample(files, min(len(files), max_frames))

    return [os.path.join(folder_path, f) for f in selected_files]


# 4. Generate ISL video using letter frames
def letters_to_video(letter_list, output_name, caption=None):
    image_paths = []

    # Collect frames for each letter
    for letter in letter_list:
        imgs = get_letter_images(letter)
        image_paths.extend(imgs)

    if not image_paths:
        print("[ERROR] No valid ISL images — video cannot be generated.")
        return None

    # Load first image to determine size
    first_image = cv2.imread(image_paths[0])
    if first_image is None:
        print("[ERROR] Could not read first image.")
        return None

    height, width, _ = first_image.shape

    # Output file path
    unique_id = uuid.uuid4().hex[:8]
    output_path = os.path.join(OUTPUT_VIDEO_DIR, f"{output_name}_{unique_id}.mp4")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 2
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Write frames to video
    for img_path in image_paths:
        img = cv2.imread(img_path)
        if img is None:
            print(f"[ERROR] Could not read: {img_path}")
            continue

        img = cv2.resize(img, (width, height))

        # Add caption 
        if caption:
            cv2.putText(
                img, caption,
                (10, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255), 2, cv2.LINE_AA
            )

        video.write(img)

    video.release()
    return output_path


# 5. Full pipeline — Sentence → Simplified → Letters → Video
def sentence_to_isl(sentence: str):
    simplified = simplify_sentence(sentence)
    letters = sentence_to_letters(simplified)

    safe_name = "".join(c for c in simplified if c.isalnum() or c == "_")
    if not safe_name:
        safe_name = "isl_output"

    video_path = letters_to_video(letters, safe_name, caption=simplified)

    return {
        "sentence": sentence,
        "simplified": simplified,
        "letters": letters,
        "video_path": video_path
    }
