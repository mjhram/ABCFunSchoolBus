"""
Draw the "no-AI" assets for ABC Fun School Bus in the same glossy toy style as the letters.
  python gen_code_assets.py            # everything
  python gen_code_assets.py lc,ui      # only some groups: lc, lights, bump, ui, fx, stickers
Output: ABCFunSchoolBus/assets/resources/textures/<name>.png   +  review/code_*.jpg contact sheets
NOTE: lowercase files are named lc_a..lc_z (Windows is case-insensitive, letter_a would clash with letter_A).
"""
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

OUT = r'C:\Users\hp2\Downloads\app4\ABCFunSchoolBus\assets\resources\textures'
REV = r'C:\Users\hp2\Downloads\app4\review'
os.makedirs(OUT, exist_ok=True); os.makedirs(REV, exist_ok=True)
S = 512

def rgb(h):
    h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float) / 255
def dark(h, f): return np.clip(rgb(h) * f, 0, 1)

# ----------------------------------------------------------------- mask primitives (S-space coords)
def M(fn):
    im = Image.new('L', (S * 2, S * 2), 0); d = ImageDraw.Draw(im); fn(d, 2)
    return np.asarray(im.resize((S, S), Image.LANCZOS), dtype=float) / 255
def poly(pts): return M(lambda d, k: d.polygon([(x * k, y * k) for x, y in pts], fill=255))
def circ(cx, cy, r): return M(lambda d, k: d.ellipse([(cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k], fill=255))
def ell(cx, cy, rx, ry): return M(lambda d, k: d.ellipse([(cx - rx) * k, (cy - ry) * k, (cx + rx) * k, (cy + ry) * k], fill=255))
def rrect(x0, y0, x1, y1, r): return M(lambda d, k: d.rounded_rectangle([x0 * k, y0 * k, x1 * k, y1 * k], radius=r * k, fill=255))
def U(*ms): return np.maximum.reduce(ms)
def SUB(a, b): return np.clip(a - b, 0, 1)
def soft(m, s=5):
    return np.clip((ndi.gaussian_filter(ndi.gaussian_filter(m, s) > 0.5, 1.2).astype(float)), 0, 1) if False else \
        ndi.gaussian_filter((ndi.gaussian_filter(m, s) > 0.5).astype(float), 1.0)
def arcband(cx, cy, r0, r1, a0, a1, n=64):
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n); pts.append((cx + r1 * math.cos(a), cy + r1 * math.sin(a)))
    for i in range(n, -1, -1):
        a = math.radians(a0 + (a1 - a0) * i / n); pts.append((cx + r0 * math.cos(a), cy + r0 * math.sin(a)))
    return poly(pts)
def line(x0, y0, x1, y1, w):
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; nx, ny = -dy / L * w / 2, dx / L * w / 2
    return poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)])
def rot_rect(cx, cy, w, h, ang):
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    return poly([(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts])
def star(cx, cy, r1, r2, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180 / n); r = r1 if i % 2 == 0 else r2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(pts)

# ----------------------------------------------------------------- shading
LIGHT = np.array([-0.45, -0.65, 0.62]); LIGHT /= np.linalg.norm(LIGHT)
def shade(mask, col, R=20, gloss=1.0):
    inside = mask > 0.5
    if not inside.any(): return np.zeros((S, S, 3))
    dist = ndi.distance_transform_edt(inside)
    h = np.sqrt(np.clip(dist / R, 0, 1)); h = ndi.gaussian_filter(h, 3) * R
    gy, gx = np.gradient(h)
    nx, ny, nz = -gx * 1.7, -gy * 1.7, np.ones_like(h)
    n = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2); nx /= n; ny /= n; nz /= n
    diff = np.clip(nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2], 0, 1)
    Hh = LIGHT + np.array([0, 0, 1.0]); Hh /= np.linalg.norm(Hh)
    nh = np.clip(nx * Hh[0] + ny * Hh[1] + nz * Hh[2], 0, 1)
    ys = np.where(inside.any(axis=1))[0]
    t = np.clip((np.arange(S)[:, None] - ys[0]) / max(1, ys[-1] - ys[0]), 0, 1)[..., None]
    base = np.broadcast_to(np.asarray(col, float), (S, S, 3))
    c = base * (1.14 - 0.26 * t) * (0.64 + 0.60 * diff[..., None])
    rim = np.clip(1 - nz, 0, 1) ** 1.5
    c = c * (1 - 0.22 * rim[..., None])
    c = c + (np.clip(nx * 0.5 + ny * 0.6, 0, 1) ** 2)[..., None] * 0.14
    c = c + gloss * (nh ** 60)[..., None] * 0.95 + gloss * (nh ** 14)[..., None] * 0.20
    return np.clip(c, 0, 1)

class Canvas:
    def __init__(self): self.rgb = np.zeros((S, S, 3)); self.a = np.zeros((S, S))
    def add(self, mask, col, R=20, glossy=True, gloss=1.0):
        c = shade(mask, col, R, gloss) if glossy else np.broadcast_to(np.asarray(col, float), (S, S, 3))
        a = mask; A = self.a; oa = a + A * (1 - a)
        self.rgb = (c * a[..., None] + self.rgb * (A * (1 - a))[..., None]) / np.maximum(oa, 1e-6)[..., None]
        self.a = oa
    def flat(self, mask, col): self.add(mask, col, glossy=False)
    def shadow(self, mask, dy=7, alpha=0.30, blur=4):
        s = ndi.shift(ndi.gaussian_filter(mask, blur), (dy, 0)) * alpha * (self.a > 0.5)
        self.rgb = self.rgb * (1 - s[..., None])
    def finish(self, rim='#333333', white=True, outline=True, trim=True, pad=6):
        inside = self.a > 0.5
        out = np.zeros((S, S, 4)); out[..., :3] = self.rgb; out[..., 3] = self.a
        if outline:
            d = ndi.distance_transform_edt(~inside)
            r1 = (d > 0) & (d <= 3); r2 = ((d > 3) & (d <= 9)) if white else np.zeros_like(r1)
            out[r2, :3] = 1; out[r2, 3] = 1
            out[r1, :3] = np.asarray(rgb(rim) if isinstance(rim, str) else rim); out[r1, 3] = 1
            out[..., 3] = ndi.gaussian_filter(out[..., 3], 0.8)
        img = Image.fromarray((np.clip(out, 0, 1) * 255).astype('uint8'), 'RGBA')
        if trim:
            bb = img.getbbox()
            if bb: img = img.crop((max(0, bb[0] - pad), max(0, bb[1] - pad), min(S, bb[2] + pad), min(S, bb[3] + pad)))
        return img

SAVED = {}
def save(name, img):
    img.save(os.path.join(OUT, name + '.png')); SAVED[name] = img

# ================================================================= 1. LOWERCASE LETTERS
FONT = r'C:\Windows\Fonts\ariblk.ttf'
COL = {'A': '#FF4D4D', 'B': '#FFC400', 'C': '#2FB8FF', 'D': '#3DDC55', 'E': '#FF8A1F', 'F': '#FF6FB5', 'G': '#9B59FF', 'H': '#9BE000',
       'I': '#FFAA00', 'J': '#00D3C8', 'K': '#E0299F', 'L': '#E8343C', 'M': '#FFD500', 'N': '#2F6BFF', 'O': '#10C57A', 'P': '#B58CFF',
       'Q': '#FF7A66', 'R': '#FF9A1A', 'S': '#18C5B5', 'T': '#8E3BFF', 'U': '#5FE0A0', 'V': '#4B4FD6', 'W': '#FFA94D', 'X': '#B8E01A',
       'Y': '#FF4F8B', 'Z': '#1F7BFF'}
B = 1024
def big_star(d, cx, cy, r, fill=(255, 224, 70, 255)):
    pts = []
    for k in range(8):
        a = math.pi / 4 * k - math.pi / 2; rr = r if k % 2 == 0 else r * 0.28
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill, outline=(255, 255, 255, 255))

def render_big(m, base_hex):
    m = ndi.gaussian_filter(m, 7); m = (m > 0.5).astype(float); m = ndi.gaussian_filter(m, 2.0)
    inside = m > 0.5
    dist = ndi.distance_transform_edt(inside); R = 52.0
    h = np.sqrt(np.clip(dist / R, 0, 1)); h = ndi.gaussian_filter(h, 6) * R
    gy, gx = np.gradient(h); nx, ny = -gx * 1.7, -gy * 1.7; nz = np.ones_like(h)
    n = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2); nx /= n; ny /= n; nz /= n
    diff = np.clip(nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2], 0, 1)
    Hh = LIGHT + np.array([0, 0, 1.0]); Hh /= np.linalg.norm(Hh)
    nh = np.clip(nx * Hh[0] + ny * Hh[1] + nz * Hh[2], 0, 1)
    base = rgb(base_hex); yy = np.linspace(0, 1, B)[:, None, None]
    light = np.clip(base * 1.15 + 0.16, 0, 1); dk = np.clip(base * 0.92, 0, 1)
    grad = light[None, None, :] * (1 - yy) + dk[None, None, :] * yy
    rim = np.clip(1 - nz, 0, 1) ** 1.5
    col = grad * (0.62 + 0.62 * diff[..., None]); col = col * (1 - 0.22 * rim[..., None])
    col += (np.clip(nx * 0.5 + ny * 0.6, 0, 1) ** 2)[..., None] * light[None, None, :] * 0.18
    col += (nh ** 60)[..., None] * 1.0 + (nh ** 14)[..., None] * 0.22
    streak = ndi.gaussian_filter(((dist > R * 0.55) & (dist < R * 1.1)).astype(float), 6)
    col += (np.clip(streak * np.clip(-ny, 0, 1), 0, 1) * 0.22)[..., None]
    col = np.clip(col, 0, 1)
    d_out = ndi.distance_transform_edt(~inside)
    ring1 = (d_out > 0) & (d_out <= 6); ring2 = (d_out > 6) & (d_out <= 16)
    out = np.zeros((B, B, 4))
    out[ring2, :3] = 1; out[ring2, 3] = 1; out[ring1, :3] = base * 0.62; out[ring1, 3] = 1
    out[inside, :3] = col[inside]; out[inside, 3] = 1
    out[..., 3] = ndi.gaussian_filter(out[..., 3], 1.1)
    return Image.fromarray((out * 255).astype('uint8'), 'RGBA'), inside

def do_lowercase():
    letters = 'abcdefghijklmnopqrstuvwxyz'
    size = 900
    while size > 300:
        f = ImageFont.truetype(FONT, size); im = Image.new('L', (B, B)); d = ImageDraw.Draw(im)
        bbs = [d.textbbox((0, 0), c, font=f, anchor='ls') for c in letters]
        top = min(b[1] for b in bbs); bot = max(b[3] for b in bbs)
        if bot - top <= 800 and max(b[2] - b[0] for b in bbs) <= 840: break
        size -= 20
    base_y = (B - (bot - top)) / 2 - top
    renders = []
    for c in letters:
        im = Image.new('L', (B, B), 0); d = ImageDraw.Draw(im)
        bb = d.textbbox((0, 0), c, font=f, anchor='ls')
        d.text(((B - (bb[2] - bb[0])) / 2 - bb[0], base_y), c, font=f, anchor='ls', fill=255)
        img, inside = render_big(np.asarray(im, float) / 255, COL[c.upper()])
        dd = ImageDraw.Draw(img)
        ys, xs = np.where(inside)
        big_star(dd, xs.max() - 6, ys.min() + 6, 40); big_star(dd, xs.min() + 14, ys.max() - 8, 26)
        renders.append((c, img))
    y0 = min(i.getbbox()[1] for _, i in renders); y1 = max(i.getbbox()[3] for _, i in renders)
    scale = 480 / (y1 - y0)
    for c, img in renders:
        bb = img.getbbox(); crop = img.crop((bb[0], y0, bb[2], y1))
        crop = crop.resize((max(8, int(crop.width * scale)), 480), Image.LANCZOS)
        save('lc_' + c, crop)
    print('lowercase done, font size', size)

# ================================================================= 2. TRAFFIC LIGHTS + SPEED BUMP
def traffic_light(name, lit):
    cv = Canvas()
    cv.add(rrect(238, 330, 274, 495, 10), dark('#9AA3B2', 1.0), R=14)           # pole
    cv.add(ell(256, 494, 70, 16), dark('#6B7280', 1.0), R=10)                    # base
    cv.add(rrect(170, 12, 342, 360, 40), rgb('#2E3440'), R=36)                  # housing
    lamps = [('red', 92, '#FF3B30'), ('yellow', 186, '#FFD60A'), ('green', 280, '#30D158')]
    glows = []
    for nm, cy, hx in lamps:
        cv.add(circ(256, cy, 48), rgb('#1B1F27'), R=14, glossy=False)           # socket
        on = (nm == lit)
        col = rgb(hx) if on else dark(hx, 0.22)
        cv.add(circ(256, cy, 38), col, R=26, gloss=1.4 if on else 0.35)
        if on: glows.append((cy, hx))
    img = cv.finish(rim='#15181E', white=False, trim=False)
    arr = np.asarray(img).astype(float) / 255
    for cy, hx in glows:                                                         # soft glow around the lit lamp
        g = np.zeros((S, S)); yy, xx = np.mgrid[0:S, 0:S]
        g = np.exp(-(((xx - 256) ** 2 + (yy - cy) ** 2) / (2 * 62 ** 2)))
        c = rgb(hx)
        a0 = arr[..., 3]; ga = g * 0.55
        arr[..., :3] = (arr[..., :3] * a0[..., None] + c * (ga * (1 - a0))[..., None] + c * (g * 0.25 * a0)[..., None]) / np.maximum(a0 + ga * (1 - a0), 1e-6)[..., None]
        arr[..., 3] = a0 + ga * (1 - a0)
    img = Image.fromarray((np.clip(arr, 0, 1) * 255).astype('uint8'), 'RGBA'); bb = img.getbbox()
    save(name, img.crop((max(0, bb[0] - 4), max(0, bb[1] - 4), min(S, bb[2] + 4), min(S, bb[3] + 4))))

def do_lights():
    for nm in ('red', 'yellow', 'green', 'off'): traffic_light('prop_light_' + nm, nm)
    # speed bump: striped dome
    cv = Canvas()
    dome = SUB(ell(256, 360, 238, 150), rrect(0, 360, S, S, 0))
    yy, xx = np.mgrid[0:S, 0:S]
    stripe = (((xx * 0.85 + yy * 0.55) // 52) % 2)[..., None]
    colr = stripe * rgb('#FFD21F') + (1 - stripe) * rgb('#2B2B2B')
    cv.add(rrect(18, 352, 494, 392, 14), rgb('#3A3A44'), R=10)
    cv.add(dome, colr, R=60, gloss=0.7)
    save('prop_speed_bump', cv.finish(rim='#222222', white=False))
    print('lights + bump done')

# ================================================================= 3. UI ICONS
def button(base_hex):
    cv = Canvas(); cv.add(circ(256, 256, 226), rgb(base_hex), R=60, gloss=1.2)
    cv.add(SUB(circ(256, 256, 226), circ(256, 256, 206)), dark(base_hex, 0.8), R=8, glossy=False); return cv
def glyph(cv, mask, col='#FFFFFF', R=9):
    cv.shadow(mask, dy=7, alpha=0.28); cv.add(mask, rgb(col), R=R, gloss=0.8)

def do_ui():
    def btn(name, base, build, rim=None):
        cv = button(base); build(cv); save('ui_' + name, cv.finish(rim=dark(base, 0.55), white=True, trim=False))
    btn('pause', '#FFAA1A', lambda c: [glyph(c, rrect(168, 146, 226, 366, 16)), glyph(c, rrect(286, 146, 344, 366, 16))])
    btn('play', '#3DDC55', lambda c: glyph(c, soft(poly([(196, 136), (196, 376), (392, 256)]), 9)))
    def home(c):
        body = SUB(rrect(166, 240, 346, 380, 12), rrect(230, 296, 282, 380, 10))
        glyph(c, U(soft(poly([(256, 120), (122, 252), (390, 252)]), 5), body))
    btn('home', '#2F9BFF', home)
    def replay(c):
        a1 = 320; e = (256 + 118 * math.cos(math.radians(a1)), 256 + 118 * math.sin(math.radians(a1)))
        t = (-math.sin(math.radians(a1)), math.cos(math.radians(a1))); n = (math.cos(math.radians(a1)), math.sin(math.radians(a1)))
        head = poly([(e[0] + t[0] * 62, e[1] + t[1] * 62), (e[0] + n[0] * 52, e[1] + n[1] * 52), (e[0] - n[0] * 52, e[1] - n[1] * 52)])
        glyph(c, U(arcband(256, 256, 88, 146, 20, a1 - 4), soft(head, 4)))
    btn('replay', '#FF8A1F', replay)
    btn('next', '#3DDC55', lambda c: glyph(c, U(rrect(136, 222, 290, 290, 14), soft(poly([(282, 160), (394, 256), (282, 352)]), 8))))
    def spk(c, waves=True):
        s = soft(poly([(138, 212), (200, 212), (270, 152), (270, 360), (200, 300), (138, 300)]), 4)
        glyph(c, s)
        if waves:
            glyph(c, arcband(272, 256, 56, 80, -48, 48), R=7); glyph(c, arcband(272, 256, 104, 128, -52, 52), R=7)
    btn('sound_on', '#2F9BFF', spk)
    def spk_off(c):
        spk(c, False); glyph(c, line(300, 170, 392, 342, 26), '#FFFFFF'); glyph(c, line(392, 170, 300, 342, 26), '#FFFFFF')
    btn('sound_off', '#8A93A6', spk_off)
    def gear(c):
        teeth = [rot_rect(256, 256, 54, 232, a) for a in (0, 45, 90, 135)]
        g = SUB(U(circ(256, 256, 104), *teeth), circ(256, 256, 44)); glyph(c, g, R=12)
    btn('settings', '#8A93A6', gear)
    def parent(c):
        glyph(c, U(circ(206, 182, 44), SUB(rrect(150, 236, 262, 372, 50), rrect(0, 330, S, S, 0))))
        glyph(c, U(circ(326, 236, 30), rrect(286, 274, 366, 372, 34)))
    btn('parent', '#9B59FF', parent)
    # ---- object icons (no round base)
    def obj(name, parts, rim='#6B4A00', white=True):
        cv = Canvas()
        for m, col, R, *g in parts: cv.add(m, rgb(col) if isinstance(col, str) else col, R=R, gloss=(g[0] if g else 1.0))
        save('ui_' + name, cv.finish(rim=rgb(rim), white=white))
    obj('lock', [(U(arcband(256, 214, 62, 96, 180, 360), rrect(160, 214, 194, 270, 4), rrect(318, 214, 352, 270, 4)), '#C9D1DB', 18),
                 (rrect(130, 250, 382, 440, 40), '#F5B800', 40), (U(circ(256, 330, 24), rrect(244, 340, 268, 392, 6)), '#7A5200', 8, 0.2)])
    obj('trophy', [(U(arcband(138, 190, 34, 60, 90, 270), arcband(374, 190, 34, 60, -90, 90)), '#FFB300', 12),
                   (soft(poly([(144, 96), (368, 96), (346, 250), (300, 316), (212, 316), (166, 250)]), 10), '#FFC21A', 44),
                   (rrect(232, 312, 280, 380, 8), '#FFB300', 14), (rrect(168, 376, 344, 430, 18), '#E69500', 22),
                   (star(256, 190, 46, 20), '#FFF2A8', 12, 0.5)])
    obj('timer', [(rrect(222, 66, 290, 112, 10), '#8A93A6', 14), (rrect(242, 100, 270, 150, 6), '#8A93A6', 10),
                  (circ(256, 292, 168), '#FF4D4D', 60), (circ(256, 292, 130), '#FFFFFF', 30, 0.4),
                  (line(256, 292, 256, 196, 18), '#333B4D', 6, 0.1), (line(256, 292, 322, 326, 16), '#333B4D', 6, 0.1), (circ(256, 292, 17), '#FF4D4D', 8)],
        rim='#8A1F1F')
    obj('star_grey', [(soft(star(256, 262, 224, 100), 6), '#A7AFBD', 50, 0.5)], rim='#6C7380')
    obj('sticker_book', [(rrect(118, 84, 396, 436, 28), '#FF6B6B', 50), (rrect(118, 84, 164, 436, 14), '#C94545', 14),
                         (rrect(386, 108, 408, 412, 8), '#FFFFFF', 6, 0.2), (soft(star(272, 262, 84, 36), 6), '#FFD83A', 22)], rim='#8A2F2F')
    obj('shop', [(arcband(256, 206, 52, 78, 180, 360), '#C77B12', 14),
                 (soft(poly([(138, 196), (374, 196), (402, 436), (110, 436)]), 14), '#FF9A1A', 60), (soft(star(256, 322, 62, 26), 5), '#FFF2A8', 16, 0.4)], rim='#8A4B00')
    obj('garage', [(soft(poly([(256, 70), (50, 214), (462, 214)]), 6), '#E8504B', 40), (rrect(78, 204, 434, 440, 10), '#FFE08A', 40),
                   (rrect(128, 266, 384, 440, 8), '#B0BEC5', 26)] +
        [(rrect(136, 280 + i * 32, 376, 296 + i * 32, 4), '#7C8A93', 4, 0.2) for i in range(5)], rim='#7A3B00')
    print('ui done')

# ================================================================= 4. EFFECTS
def do_fx():
    rnd = random.Random(7)
    cv = Canvas(); cols = ['#FF4D4D', '#FFC400', '#3DDC55', '#2FB8FF', '#9B59FF', '#FF6FB5', '#FF8A1F']
    for i in range(70):
        a = rnd.uniform(0, 360); r = rnd.uniform(40, 235); x = 256 + r * math.cos(math.radians(a)); y = 256 + r * math.sin(math.radians(a))
        cv.flat(rot_rect(x, y, rnd.uniform(14, 26), rnd.uniform(8, 14), rnd.uniform(0, 180)), rgb(rnd.choice(cols)))
    for i in range(8):
        a = rnd.uniform(0, 360); r = rnd.uniform(90, 200)
        cv.flat(arcband(256 + r * math.cos(math.radians(a)), 256 + r * math.sin(math.radians(a)), 10, 16, a, a + 150, 24), rgb(rnd.choice(cols)))
    save('fx_confetti', cv.finish(outline=False, trim=True))
    cv = Canvas()
    for cx, cy, r in [(256, 256, 190), (120, 130, 80), (400, 150, 70), (130, 390, 60), (396, 380, 90)]:
        cv.add(star(cx, cy, r, r * 0.22, 4), rgb('#FFD83A'), R=r * 0.3, gloss=1.2)
        cv.flat(star(cx, cy, r * 0.42, r * 0.12, 4), rgb('#FFFFFF'))
    save('fx_sparkle', cv.finish(outline=False, trim=True))
    yy, xx = np.mgrid[0:S, 0:S]; al = np.zeros((S, S))
    for cx, cy, r in [(256, 290, 120), (160, 310, 80), (352, 310, 84), (210, 220, 78), (310, 215, 74), (256, 170, 64)]:
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
        al = np.maximum(al, np.clip((1.0 - d) / 0.28, 0, 1))
    tt = np.clip((yy - 150) / 260.0, 0, 1)[..., None]
    pc = rgb('#FFFFFF') * (1 - tt * 0.55) + rgb('#C4D4EA') * (tt * 0.55)
    po = np.zeros((S, S, 4)); po[..., :3] = pc; po[..., 3] = al
    pim = Image.fromarray((po * 255).astype('uint8'), 'RGBA'); pim = pim.crop(pim.getbbox())
    save('fx_poof', pim)
    yy, xx = np.mgrid[0:S, 0:S]; g = np.exp(-(((xx - 256) ** 2 + (yy - 256) ** 2) / (2 * 78 ** 2)))
    core = np.exp(-(((xx - 256) ** 2 + (yy - 256) ** 2) / (2 * 22 ** 2)))
    out = np.zeros((S, S, 4)); out[..., :3] = rgb('#CFFF4A')[None, None] * (1 - core[..., None]) + core[..., None]; out[..., 3] = np.clip(g * 0.95 + core, 0, 1)
    save('fx_firefly', Image.fromarray((out * 255).astype('uint8'), 'RGBA'))
    cv = Canvas(); arms = []
    for k in range(6):
        a = k * 60; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        arms.append(line(256, 256, 256 + 215 * ca, 256 + 215 * sa, 16))
        for fr in (0.5, 0.74):
            px, py = 256 + 215 * fr * ca, 256 + 215 * fr * sa
            for s in (-35, 35):
                b = math.radians(a + s); arms.append(line(px, py, px + 62 * math.cos(b), py + 62 * math.sin(b), 12))
    cv.add(U(*arms, circ(256, 256, 24)), rgb('#F2F9FF'), R=8, gloss=0.8)
    save('fx_snowflake', cv.finish(rim=rgb('#5AA9EE'), white=False, trim=True))
    print('fx done')

# ================================================================= 5. STICKER BADGES
def do_stickers():
    def badge(name, theme, emblem):
        cv = Canvas()
        cv.add(circ(256, 256, 236), rgb('#FFC21A'), R=44, gloss=1.2)
        cv.add(circ(256, 256, 204), rgb(theme), R=70, gloss=0.9)
        cv.add(SUB(circ(256, 256, 204), circ(256, 256, 190)), dark(theme, 0.75), R=6, glossy=False)
        emblem(cv); save('sticker_' + name, cv.finish(rim=rgb('#8A5A00'), white=True, trim=False))
    def sun(c):
        rays = [rot_rect(256, 256, 26, 190, a) for a in range(0, 180, 30)]
        c.add(U(*rays), rgb('#FFE14D'), R=10); c.add(circ(256, 256, 78), rgb('#FFD21F'), R=46)
        c.flat(circ(236, 238, 20), rgb('#FFF6B0'))
    badge('w1', '#4CC3FF', sun)
    def barn(c):
        c.add(rrect(160, 262, 352, 392, 10), rgb('#E8504B'), R=26); c.add(soft(poly([(256, 160), (140, 270), (372, 270)]), 6), rgb('#B3342F'), R=30)
        c.add(rrect(226, 312, 286, 392, 8), rgb('#FFFFFF'), R=14); c.flat(line(226, 312, 286, 392, 8), rgb('#E8504B')); c.flat(line(286, 312, 226, 392, 8), rgb('#E8504B'))
    badge('w2', '#FF9A5A', barn)
    def moon(c):
        c.add(SUB(circ(240, 262, 96), circ(284, 236, 84)), rgb('#FFF3B0'), R=36)
        for x, y, r in [(340, 170, 30), (196, 168, 22), (352, 300, 20)]: c.add(star(x, y, r, r * 0.4), rgb('#FFE14D'), R=8)
    badge('w3', '#2B3A8F', moon)
    def snowman(c):
        for cx, cy, r in [(256, 340, 70), (256, 244, 52), (256, 168, 36)]: c.add(circ(cx, cy, r), rgb('#FFFFFF'), R=r * 0.9, gloss=0.4)
        c.flat(poly([(256, 168), (300, 178), (256, 186)]), rgb('#FF8A1F')); c.flat(circ(244, 158, 5), rgb('#222222')); c.flat(circ(270, 158, 5), rgb('#222222'))
        c.add(rrect(222, 196, 290, 214, 8), rgb('#FF4D4D'), R=8)
    badge('w4', '#8FD3FF', snowman)
    def rainbow(c):
        for i, hx in enumerate(['#FF4D4D', '#FF9A1A', '#FFE14D', '#4CD964', '#3AA8FF', '#7A5CFF']):
            c.add(arcband(256, 350, 140 - i * 20, 160 - i * 20, 180, 360), rgb(hx), R=9)
        c.add(U(circ(110, 350, 0.1), ell(130, 360, 50, 26), ell(382, 360, 50, 26)), rgb('#FFFFFF'), R=14, gloss=0.3)
    badge('w5', '#7ED957', rainbow)
    def perfect(c):
        for sgn in (-1, 1):
            for i in range(7):
                a = math.radians(115 + i * 22) if sgn < 0 else math.radians(65 - i * 22)
                x, y = 256 + 148 * math.cos(a), 270 + 148 * math.sin(a)
                c.add(rot_rect(x, y, 22, 52, math.degrees(a) + 90 + sgn * 25), rgb('#2FBF4F'), R=8)
        c.add(soft(star(256, 262, 124, 54), 5), rgb('#FFE14D'), R=34)
    badge('perfect', '#FFB020', perfect)
    badge('speed', '#FF5A7A', lambda c: c.add(soft(poly([(290, 112), (186, 282), (252, 282), (216, 408), (340, 232), (272, 232)]), 4), rgb('#FFE14D'), R=22))
    def words(c):
        c.add(soft(poly([(256, 196), (140, 172), (140, 360), (256, 384)]), 5), rgb('#FFFFFF'), R=30, gloss=0.5)
        c.add(soft(poly([(256, 196), (372, 172), (372, 360), (256, 384)]), 5), rgb('#F1ECFF'), R=30, gloss=0.5)
        c.flat(line(256, 196, 256, 384, 8), rgb('#6B3FC4'))
        for y in (232, 268, 304): c.flat(line(160, y, 238, y + 10, 8), rgb('#B8A2F0')); c.flat(line(274, y + 10, 352, y, 8), rgb('#B8A2F0'))
        c.add(star(372, 150, 30, 12, 4), rgb('#FFE14D'), R=8)
    badge('words', '#9B59FF', words)
    def wheel(c):
        c.add(SUB(circ(256, 256, 124), circ(256, 256, 92)), rgb('#FFFFFF'), R=14)
        c.add(U(line(140, 262, 372, 262, 24), line(256, 262, 256, 372, 24)), rgb('#FFFFFF'), R=10); c.add(circ(256, 256, 38), rgb('#FFE14D'), R=24)
    badge('driver', '#2FA8FF', wheel)
    def smile(c):
        c.add(circ(256, 256, 118), rgb('#FFE14D'), R=70); c.flat(circ(220, 226, 14), rgb('#3A2A00')); c.flat(circ(292, 226, 14), rgb('#3A2A00'))
        c.flat(arcband(256, 252, 62, 78, 25, 155), rgb('#3A2A00')); c.flat(circ(196, 276, 16), rgb('#FF9A9A')); c.flat(circ(316, 276, 16), rgb('#FF9A9A'))
    badge('helper', '#3DDC55', smile)
    def compass(c):
        c.add(SUB(circ(256, 256, 126), circ(256, 256, 104)), rgb('#FFFFFF'), R=10)
        c.add(soft(poly([(256, 128), (226, 256), (286, 256)]), 3), rgb('#FF4D4D'), R=14); c.add(soft(poly([(256, 384), (226, 256), (286, 256)]), 3), rgb('#FFFFFF'), R=14)
        c.add(circ(256, 256, 14), rgb('#FFE14D'), R=8)
    badge('explorer', '#14B8A6', compass)
    def crown(c):
        c.add(soft(poly([(146, 346), (146, 198), (204, 264), (256, 170), (308, 264), (366, 198), (366, 346)]), 8), rgb('#FFD21F'), R=44)
        c.add(rrect(146, 340, 366, 392, 14), rgb('#F5B800'), R=22)
        for x, hx in [(190, '#FF4D4D'), (256, '#3AA8FF'), (322, '#3DDC55')]: c.add(circ(x, 366, 14), rgb(hx), R=10)
    badge('champion', '#E0299F', crown)
    print('stickers done')

if __name__ == '__main__':
    groups = [g for g in (sys.argv[1].split(',') if len(sys.argv) > 1 else ['lc', 'lights', 'ui', 'fx', 'stickers']) if g]
    if 'lc' in groups: do_lowercase()
    if 'lights' in groups or 'bump' in groups: do_lights()
    if 'ui' in groups: do_ui()
    if 'fx' in groups: do_fx()
    if 'stickers' in groups: do_stickers()
    # contact sheets
    def sheet(prefix, out, cols, cell, bg=(120, 180, 235)):
        names = sorted(n for n in SAVED if n.startswith(prefix))
        if not names: return
        rows = (len(names) + cols - 1) // cols
        sh = Image.new('RGB', (cols * cell, rows * (cell + 14)), bg); dr = ImageDraw.Draw(sh)
        for i, n in enumerate(names):
            im = SAVED[n].copy(); im.thumbnail((cell - 8, cell - 8)); x = (i % cols) * cell + 4; y = (i // cols) * (cell + 14) + 2
            sh.paste(im, (x, y), im); dr.text((x, y + cell - 4), n, fill=(0, 0, 0))
        sh.save(os.path.join(REV, out), quality=88)
    sheet('lc_', 'code_lc.jpg', 9, 150); sheet('ui_', 'code_ui.jpg', 6, 210); sheet('fx_', 'code_fx.jpg', 5, 250)
    sheet('sticker_', 'code_stickers.jpg', 6, 210); sheet('prop_', 'code_props.jpg', 5, 260)
    print('saved', len(SAVED), 'images')
