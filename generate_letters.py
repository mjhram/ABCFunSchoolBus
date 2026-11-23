import os
import shutil
import time
from gradio_client import Client

LETTERS = [
    ("E", "tangerine orange"),
    ("F", "bubblegum pink"),
    ("G", "royal purple"),
    ("H", "bright lime green"),
    ("I", "golden amber"),
    ("J", "aqua cyan"),
    ("K", "berry magenta"),
    ("L", "cherry red"),
    ("M", "sunshine yellow"),
    ("N", "sapphire blue"),
    ("O", "emerald green"),
    ("P", "soft lilac purple"),
    ("Q", "warm coral"),
    ("R", "bright tangerine"),
    ("S", "turquoise teal"),
    ("T", "vivid violet"),
    ("U", "fresh mint green"),
    ("V", "deep indigo"),
    ("W", "bright apricot orange"),
    ("X", "chartreuse yellow-green"),
    ("Y", "rose magenta"),
    ("Z", "electric cobalt blue")
]

OUT_DIR = r"c:\Users\hp2\Downloads\app3\assets"
os.makedirs(OUT_DIR, exist_ok=True)

print("Connecting to evalstate/flux1_schnell Space...")
client = Client("evalstate/flux1_schnell")
print("Connected!")

for letter, color in LETTERS:
    dest = os.path.join(OUT_DIR, f"asset_letter_{letter}.webp")
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f"Skipping {letter}, already exists.")
        continue

    prompt = (
        f"Mobile game asset sprite of a cute 3D glossy cartoon alphabet letter {letter}, "
        f"preschool educational style, vibrant {color} with soft rounded bevels, "
        "smooth plastic toy texture, subtle golden star sparkles, isolated on a solid pure white background, "
        "centered, clean studio lighting, high resolution game prop"
    )

    success = False
    for attempt in range(3):
        try:
            print(f"Generating Letter {letter} ({color}) [Attempt {attempt+1}]...")
            res, seed = client.predict(
                prompt=prompt,
                seed=0,
                randomize_seed=True,
                width=1024,
                height=1024,
                num_inference_steps=4,
                api_name="/infer"
            )
            shutil.copy(res, dest)
            print(f"Successfully saved Letter {letter} to {dest} ({os.path.getsize(dest)} bytes)")
            success = True
            time.sleep(1.5)
            break
        except Exception as e:
            print(f"Error on Letter {letter}: {e}. Retrying in 4 seconds...")
            time.sleep(4)

    if not success:
        print(f"Failed to generate Letter {letter} after 3 attempts.")

print("All alphabet letters processed!")
