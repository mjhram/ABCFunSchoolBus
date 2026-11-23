"""
ABC Fun School Bus - asset prompt pack + batch generator (same FLUX schnell Space you used before).

  python generate_assets.py --list                 # show every asset + count
  python generate_assets.py --only words           # generate one category
  python generate_assets.py --only props,kids      # several categories
  python generate_assets.py --variants 2           # 2 candidates per asset (pick the best)
  python generate_assets.py                        # everything not generated yet

Output: app4\assets_new\asset_<name>.webp   (existing files are skipped, so you can resume)

RULES THAT MATTER
 * Never ask the model for text, letters, numbers or words inside an image - it misspells them.
   (That is why letters D / E / F came out wrong earlier.) Letters, signs and labels are drawn in code.
 * Pale / white subjects (snowman, sheep, egg, cloud...) use bg='magenta' so they can be cut out.
 * 1024x1024 for sprites and icons, 1344x768 for the wide 16:9 illustrations.
"""
import os, sys, shutil, time, argparse

OUT_DIR = r"C:\Users\hp2\Downloads\app4\assets_new"

CORE = ("cute 3D glossy cartoon, preschool educational mobile game style, smooth plastic toy texture, "
        "soft rounded bevels, vibrant saturated colors, soft clean studio lighting")
TAIL = "centered, whole object fully visible, no text, no letters, no numbers, no ground shadow, high resolution game asset"

def _bg(bg): return f"isolated on a solid pure {bg} background"

def prop(subject, bg="white"):
    return f"Mobile game asset sprite of {subject}, {CORE}, {_bg(bg)}, {TAIL}"
def scenery(subject, bg="white"):
    return (f"Mobile game roadside scenery sprite of {subject}, viewed straight from the front, {CORE}, "
            f"{_bg(bg)}, {TAIL}")
def char(subject, bg="white"):
    return (f"Mobile game character sprite of {subject}, friendly smiling face, big shiny eyes, chibi proportions, "
            f"full body, {CORE}, {_bg(bg)}, {TAIL}")
def card(subject, bg="white"):
    return (f"Mobile game flash-card illustration of {subject}, single object, {CORE}, {_bg(bg)}, {TAIL}")
def icon(subject):
    return (f"Mobile game UI icon of {subject}, glossy 3D rounded button style, thick white outline, "
            f"{CORE}, {_bg('white')}, {TAIL}")
def wide(subject):
    return (f"Wide 16:9 cartoon game illustration of {subject}, {CORE}, bright cheerful colors, "
            "clean composition, no text, no letters, no numbers, high resolution")

A = []  # (category, name, prompt, width, height)
def add(cat, name, prompt, w=1024, h=1024): A.append((cat, name, prompt, w, h))

# ------------------------------------------------------------------ 1. WORD & SOUND PICTURES
WHITE_OK = {
 # animals
 "cat": "a cute orange tabby kitten sitting", "dog": "a friendly golden puppy sitting",
 "pig": "a happy pink piglet standing", "cow": "a cute black and white cow standing",
 "hen": "a cute red and brown hen", "fox": "a cute orange fox sitting with a fluffy tail",
 "bee": "a cute fat yellow and black bumblebee flying", "duck": "a cute yellow duckling",
 "frog": "a cute green frog sitting", "bird": "a cute little blue bird perched",
 "fish": "a cute orange goldfish", "lion": "a cute lion cub with a fluffy mane",
 "bear": "a cute brown teddy bear cub sitting", "goat": "a cute brown and white goat",
 "horse": "a cute brown pony standing", "rabbit": "a cute grey rabbit sitting with long ears",
 "zebra": "a cute zebra standing", "whale": "a cute blue whale spouting a little water",
 # transport
 "bus": "a cute yellow school bus, side view", "car": "a cute red toy car, side view",
 "bike": "a cute blue children's bicycle", "boat": "a cute red sailboat with a white sail",
 "train": "a cute colorful toy steam train", "plane": "a cute little blue airplane",
 "truck": "a cute green dump truck", "van": "a cute pink delivery van, side view",
 # food
 "cake": "a slice of pink birthday cake with a cherry on top", "apple": "a shiny red apple with a green leaf",
 "bread": "a loaf of golden brown bread", "pizza": "a slice of cheesy pizza with pepperoni",
 "jam": "a glass jar of red strawberry jam with a cloth lid", "corn": "a yellow corn cob with green leaves",
 "pear": "a shiny green pear", "orange": "a shiny orange fruit with a green leaf",
 "nut": "a brown acorn nut",
 # nature
 "sun": "a smiling yellow sun with short rays", "moon": "a smiling yellow crescent moon",
 "star": "a shiny golden five-point star", "tree": "a cute round green tree with a brown trunk",
 "leaf": "a big green leaf", "flower": "a cute pink flower with a green stem", "kite": "a colorful diamond kite with a ribbon tail",
 # school
 "book": "a closed red storybook, front cover blank", "bag": "a cute blue school backpack",
 "desk": "a small wooden school desk", "pen": "a red pen", "ruler": "a yellow wooden ruler with no markings",
 "pencil": "a yellow pencil with a pink eraser", "clock": "a round red alarm clock with two small bells",
 "ball": "a shiny red and blue beach ball", "bell": "a golden school bell with a wooden handle",
 "school": "a cute little red school house building with a bell tower and a flag",
 "crayon": "a bright purple crayon",
 # home & things
 "bed": "a cute cozy bed with a blue blanket and a pillow", "cup": "a cute yellow mug", "hat": "a red baseball cap",
 "key": "a big golden key", "box": "a brown cardboard box with an open lid", "door": "a cute blue front door with a round window",
 "lamp": "a cute table lamp with a yellow shade", "sock": "a striped colorful sock",
 "umbrella": "an open red umbrella", "nest": "a bird nest with three small blue eggs",
 "crown": "a golden royal crown with red jewels", "xylophone": "a rainbow-colored toy xylophone with two mallets",
 "yoyo": "a red yo-yo with a string",
}
MAGENTA = {  # pale / white subjects need a chroma-key background
 "sheep": "a cute fluffy white sheep", "egg": "a white egg, slightly cracked open with a yolk visible",
 "milk": "a white milk carton with a blue cap, no label text", "cloud": "a cute fluffy white cloud with a smile",
 "snow": "a big white snowflake crystal", "icecream": "an ice cream cone with a pink and white scoop",
}
for k, v in WHITE_OK.items(): add("words", f"word_{k}", card(v))
for k, v in MAGENTA.items():  add("words", f"word_{k}", card(v, "magenta"))

# ------------------------------------------------------------------ 2. MASCOT POSES + HATS
PUP = "the same cute golden-brown puppy with floppy ears wearing a blue baseball cap and a blue bandana"
for k, v in {
 "cheer":   "jumping with both paws in the air, mouth wide open in joy, tiny confetti around",
 "think":   "one paw on the chin, looking up with a curious thinking face",
 "oops":    "a sweet worried 'oh no' face, ears drooping, one paw touching its cheek (gentle, not sad)",
 "wave":    "waving hello with one paw, big smile",
 "point":   "pointing forward with one paw, excited face",
 "drive":   "holding an imaginary steering wheel, focused happy face",
 "sleep":   "curled up sleeping peacefully with a small blue nightcap",
 "party":   "wearing a party hat and holding a small wrapped gift",
}.items(): add("mascot", f"mascot_{k}", char(f"{PUP}, {v}"))
for k, v in {
 "crown": "a golden royal crown with a red jewel", "party": "a striped party hat with a pompom",
 "cowboy": "a brown cowboy hat", "chef": "a tall white chef hat", "pirate": "a black pirate hat with a gold trim",
 "space": "a round shiny astronaut helmet", "wizard": "a purple wizard hat with gold stars",
}.items(): add("mascot", f"hat_{k}", prop(v, "magenta" if k == "chef" else "white"))

# ------------------------------------------------------------------ 3. KIDS (bus-stop passengers)
for k, v in {
 "boy_backpack":  "a smiling 5-year-old boy with short black hair, a red backpack, waving",
 "girl_pigtails": "a smiling 5-year-old girl with two pigtails, a yellow dress and a purple backpack, waving",
 "girl_scarf":    "a smiling 5-year-old girl wearing a pink headscarf and a green dress, holding a school bag, waving",
 "boy_glasses":   "a smiling 6-year-old boy with round glasses, curly brown hair, blue jacket, holding a book, waving",
 "girl_curly":    "a smiling 5-year-old girl with big curly hair, an orange shirt and a teal backpack, waving",
 "toddler_teddy": "a smiling toddler holding a small teddy bear, wearing a yellow raincoat, waving",
}.items(): add("kids", f"kid_{k}", char(v))

# ------------------------------------------------------------------ 4. ROAD PROPS / CHALLENGE OBJECTS
for k, v, bg in [
 ("cone",        "an orange traffic cone with two white stripes", "white"),
 ("cone_pair",   "two orange traffic cones side by side", "white"),
 ("puddle",      "a blue rain puddle seen from a slight angle, flat on the ground, with a few ripples", "white"),
 ("hay",         "a round golden hay bale", "white"),
 ("barrier",     "a red and white striped road barrier with two legs", "white"),
 ("sheep",       "a cute fluffy white sheep standing", "magenta"),
 ("duck_family", "a mother duck followed by three tiny ducklings walking in a line", "white"),
 ("cow_road",    "a cute black and white cow standing", "white"),
 ("bus_stop_sign","a round yellow bus stop sign on a grey pole, showing only a simple bus icon, no text", "white"),
 ("bus_shelter", "a cute little bus shelter with a blue roof, a bench and clear glass sides", "white"),
 ("crossing_sign","a yellow diamond school crossing sign on a pole showing two simple child silhouettes, no text", "white"),
 ("stop_sign",   "a red octagon stop sign on a grey pole with a plain white border and NO text", "white"),
 ("traffic_pole","an empty grey traffic light pole with a black three-light housing, all three lights turned off", "white"),
 ("light_red",   "a traffic light pole with a black housing, only the RED light glowing brightly, the other two lights dark", "white"),
 ("light_yellow","a traffic light pole with a black housing, only the YELLOW light glowing brightly, the other two lights dark", "white"),
 ("light_green", "a traffic light pole with a black housing, only the GREEN light glowing brightly, the other two lights dark", "white"),
 ("finish_arch", "a checkered black and white finish line arch spanning a road, with colorful balloons on both sides, no text", "white"),
 ("star_gate",   "a golden arch gate made of shiny stars spanning a road, sparkles around it, no text", "white"),
 ("balloon_arch","a colorful balloon arch spanning a road, no text", "white"),
 ("speed_bump",  "a yellow and black striped road speed bump seen from the front", "white"),
]: add("props", f"prop_{k}", prop(v, bg))

# ------------------------------------------------------------------ 5. SCENERY (4 per world, front view, ground-anchored)
SC = {
 "w1_sunny": {   # Sunny Street (day)
   "lamp": "a cute old-fashioned street lamp with a warm glow", "flowerbed": "a row of colorful tulips and daisies in a wooden planter",
   "fence": "a short white picket fence section with flowers", "schoolbus_stop": "a tiny wooden mailbox with a red flag next to a small bush"},
 "w2_sunset": {  # Sunset Hills (warm farmland)
   "barn": "a cute red barn with white trim and a small hayloft door", "windmill": "a cute wooden windmill with four sails",
   "haystack": "three golden hay stacks with a pitchfork", "scarecrow": "a friendly smiling scarecrow with a straw hat"},
 "w3_night": {   # Starry Night
   "streetlamp": "a tall glowing street lamp with a soft yellow light", "house_lit": "a cute cottage with warm glowing yellow windows",
   "pine_dark": "a tall dark-green pine tree with tiny fairy lights", "owl_tree": "a cute round tree with a smiling owl sitting on a branch"},
 "w4_snow": {    # Snowy Town (white subjects -> magenta)
   "snowman": ("a cute snowman with a carrot nose, red scarf and top hat", "magenta"),
   "pine_snow": ("a green pine tree covered with thick white snow", "magenta"),
   "igloo": ("a cute white igloo with a small arched door", "magenta"),
   "house_snow": ("a cute cottage with a snow-covered roof and smoke from the chimney", "magenta")},
 "w5_rainbow": { # Rainbow Meadow (candy land)
   "mushroom": "a giant red mushroom with white spots and a tiny door", "lollipop_tree": "a tree whose crown is a giant swirly rainbow lollipop",
   "flowers": "a big cluster of giant colorful flowers with smiling faces", "candy_house": "a cute gingerbread-style cottage decorated with candy and frosting"},
}
for world, items in SC.items():
    for k, v in items.items():
        txt, bg = (v if isinstance(v, tuple) else (v, "white"))
        add("scenery", f"scn_{world}_{k}", scenery(txt, bg))
# sky items
for k, v, bg in [("balloon", "a colorful striped hot air balloon with a basket", "white"),
                 ("kite_sky", "a pair of colorful kites flying with ribbon tails", "white"),
                 ("birds", "three tiny cute blue birds flying in a V formation", "white"),
                 ("plane_banner", "a small cute plane towing a blank plain white banner", "magenta"),
                 ("shooting_star", "a golden shooting star with a glittering tail", "white")]:
    add("scenery", f"sky_{k}", prop(v, bg))

# ------------------------------------------------------------------ 6. UI ICONS
for k, v in {
 "pause": "a round pause button with two bars", "play": "a round green play button with a triangle",
 "home": "a round blue home button with a little house", "replay": "a round orange replay button with a circular arrow",
 "next": "a round green next button with a right arrow", "sound_on": "a round blue speaker button with sound waves",
 "sound_off": "a round grey speaker button with a diagonal slash", "settings": "a round grey gear settings button",
 "parent": "a round purple button with a simple adult-and-child silhouette", "lock": "a golden padlock",
 "trophy": "a shiny golden trophy cup with two handles", "medal": "a golden medal with a red ribbon and a star",
 "timer": "a round red stopwatch", "star_grey": "a dull grey five-point star, empty",
 "sticker_book": "a closed colorful sticker album book with a star on the cover", "shop": "a cute shopping bag with a star",
 "garage": "a cute little garage with a yellow bus peeking out",
}.items(): add("ui", f"ui_{k}", icon(v))

# ------------------------------------------------------------------ 7. WORLD ICONS (level-select cards)
for k, v in {
 "w1": "a sunny street scene: bright sun over a tiny yellow school bus and a house", "w2": "a sunset hill with a red barn and a big orange sun",
 "w3": "a night sky with a smiling moon, stars and a tiny glowing house", "w4": "a snowy scene with a snowman and falling snowflakes",
 "w5": "a rainbow over a meadow with a giant red mushroom",
}.items(): add("worlds", f"world_{k}", icon(v))

# ------------------------------------------------------------------ 8. STICKER BOOK BADGES
for k, v in {
 "w1": "a round badge with a smiling sun and a small yellow bus", "w2": "a round badge with a red barn and a sunset",
 "w3": "a round badge with a smiling moon and stars", "w4": "a round badge with a cheerful snowman",
 "w5": "a round badge with a rainbow and a flower", "perfect": "a round badge with a golden star and a laurel wreath",
 "speed": "a round badge with a lightning bolt and sneakers", "words": "a round badge with an open storybook and sparkles",
 "driver": "a round badge with a steering wheel and a thumbs up", "helper": "a round badge with a smiling kid waving next to a bus stop sign",
 "explorer": "a round badge with a compass and a tiny map", "champion": "a round badge with a golden crown and ribbons",
}.items(): add("stickers", f"sticker_{k}", icon(v))

# ------------------------------------------------------------------ 9. BUS SKINS (shop cards, side view)
for k, v in {"yellow": "yellow", "blue": "sky blue", "pink": "bubblegum pink", "green": "lime green",
             "rainbow": "rainbow striped", "space": "silver with a tiny rocket decal and star decals"}.items():
    add("bus", f"bus_{k}", prop(f"a cute {v} cartoon school bus, side view, big round wheels, smiling headlights, no text", "white"))

# ------------------------------------------------------------------ 10. EFFECTS
for k, v in {"confetti": "a burst of colorful confetti pieces and streamers exploding outward",
             "sparkle": "a cluster of golden four-point sparkles", "poof": "a soft round white smoke puff cartoon explosion",
             "firefly": "a soft glowing yellow-green firefly light orb", "snowflake": "a single detailed white snowflake"}.items():
    add("fx", f"fx_{k}", prop(v, "magenta" if k in ("poof", "snowflake") else "white"))

# ------------------------------------------------------------------ 11. WIDE ILLUSTRATIONS (1344x768)
for k, v in {
 "title":   "a giant friendly yellow school bus seen from the front on a sunny rainbow road, the puppy mascot waving from the driver window, colorful balloons, empty sky area at the top for a logo",
 "worldmap":"a top-down winding road map linking five cheerful regions: a sunny street, a red barn farm at sunset, a starry night village, a snowy town, and a rainbow candy meadow, with empty space around each region",
 "school":  "a cheerful big red school building with a bell tower, a playground, and children's silhouettes, seen from the front, sunny day, final destination of the road",
 "garage":  "the inside of a cozy bright garage with a yellow school bus in the middle, paint cans, and tools, empty wall space for UI",
 "sticker_page": "an empty open sticker album page with soft pastel gradient background and 12 empty round slots, no text",
}.items(): add("wide", f"bg_{k}", wide(v), 1344, 768)


# ====================================================================== runner
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--variants", type=int, default=1)
    ap.add_argument("--token", default=os.environ.get("HF_TOKEN", ""), help="free Hugging Face token (hf_...) - gives a bigger ZeroGPU quota")
    ap.add_argument("--limit", type=int, default=0, help="stop after N new images (to stay inside the daily quota)")
    a = ap.parse_args()
    sel = [x for x in a.only.split(",") if x]
    todo = [t for t in A if not sel or t[0] in sel]
    if a.list:
        cats = {}
        for c, n, p, w, h in todo: cats.setdefault(c, []).append(n)
        for c, ns in cats.items(): print(f"[{c}] {len(ns)}: " + ", ".join(ns))
        print("TOTAL", len(todo)); return
    from gradio_client import Client
    os.makedirs(OUT_DIR, exist_ok=True)
    client = Client("evalstate/flux1_schnell", token=a.token or None)
    made = 0
    for cat, name, prompt, w, h in todo:
        for v in range(1, a.variants + 1):
            suffix = f"_v{v}" if a.variants > 1 else ""
            dest = os.path.join(OUT_DIR, f"asset_{name}{suffix}.webp")
            if os.path.exists(dest) and os.path.getsize(dest) > 1000: continue
            for attempt in range(3):
                try:
                    print(f"{name}{suffix} [{attempt+1}]")
                    res, seed = client.predict(prompt=prompt, seed=0, randomize_seed=True, width=w, height=h,
                                               num_inference_steps=4, api_name="/infer")
                    shutil.copy(res, dest); time.sleep(1.5); break
                except Exception as e:
                    print("  error:", e); time.sleep(4)
    print("done")

if __name__ == "__main__":
    main()
