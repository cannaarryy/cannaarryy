"""Genera los GIFs animados del perfil (boot + status dot).

Solo Pillow (pip install pillow). Tipografia Consolas del sistema.
Diseno: sutil, premium, loop infinito, 2-4 s. Sin JavaScript en el README:
GitHub reproduce GIFs de forma nativa.

Uso:
    python assets/make_gifs.py
Salida:
    assets/boot.gif    (~880x300, secuencia de arranque del perfil)
    assets/online.gif  (32x32, punto de estado pulsante, fondo transparente)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = r"C:\Windows\Fonts\consola.ttf"

BG = (10, 10, 10)
WHITE = (245, 245, 245)
MUTED = (138, 138, 138)
ACCENT = (56, 189, 248)
FPS = 10
FRAME_MS = 100


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def base_frame(w, h):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, h - 1], outline=(34, 34, 34))
    return img, d


def to_gif(frames, path):
    pals = [f.convert("P", palette=Image.ADAPTIVE, colors=32) for f in frames]
    pals[0].save(path, save_all=True, append_images=pals[1:],
                 duration=[FRAME_MS] * len(pals), loop=0, optimize=True)
    kb = os.path.getsize(path) // 1024
    print("%s: %d frames, %d KB" % (os.path.basename(path), len(pals), kb))


def make_boot():
    W, H, FS = 880, 330, 22
    F = font(FS)
    LH, X, Y0 = 30, 36, 34
    ok_lines = ["PROFILE", "PROJECTS", "STACK", "ACTIVITY", "CLIENTFLOW", "CONTACT"]
    frames = []

    def text_y(i):
        return Y0 + i * LH

    # 1) comando + cursor parpadeante
    for blink in (True, False, True):
        img, d = base_frame(W, H)
        d.text((X, text_y(0)), "$", font=F, fill=ACCENT)
        d.text((X + 24, text_y(0)), "boot profile --user cannaarryy", font=F, fill=MUTED)
        if blink:
            d.rectangle([X + 24 + F.getlength("boot profile --user cannaarryy") + 8, text_y(0),
                         X + 24 + F.getlength("boot profile --user cannaarryy") + 20, text_y(0) + 22],
                        fill=ACCENT)
        frames.append(img)

    # 2) lineas [ OK ] una a una
    for idx in range(len(ok_lines)):
        for hold in (False, True):
            img, d = base_frame(W, H)
            d.text((X, text_y(0)), "$", font=F, fill=ACCENT)
            d.text((X + 24, text_y(0)), "boot profile --user cannaarryy", font=F, fill=MUTED)
            for j in range(idx + 1):
                d.text((X, text_y(1 + j)), "[ OK ]", font=F, fill=ACCENT)
                d.text((X + 110, text_y(1 + j)), ok_lines[j], font=F, fill=WHITE)
            frames.append(img)

    # 3) barra de progreso
    cells = 20
    for fill in (5, 10, 15, 20, 20):
        img, d = base_frame(W, H)
        d.text((X, text_y(0)), "$", font=F, fill=ACCENT)
        d.text((X + 24, text_y(0)), "boot profile --user cannaarryy", font=F, fill=MUTED)
        for j, name in enumerate(ok_lines):
            d.text((X, text_y(1 + j)), "[ OK ]", font=F, fill=ACCENT)
            d.text((X + 110, text_y(1 + j)), name, font=F, fill=WHITE)
        bar = "█" * fill + "░" * (cells - fill)
        d.text((X, text_y(7)), "[%s] %d%%" % (bar, fill * 5), font=F, fill=WHITE)
        frames.append(img)

    # 4) SYSTEM ONLINE con pulso
    for k in range(14):
        img, d = base_frame(W, H)
        d.text((X, text_y(0)), "$", font=F, fill=ACCENT)
        d.text((X + 24, text_y(0)), "boot profile --user cannaarryy", font=F, fill=MUTED)
        for j, name in enumerate(ok_lines):
            d.text((X, text_y(1 + j)), "[ OK ]", font=F, fill=ACCENT)
            d.text((X + 110, text_y(1 + j)), name, font=F, fill=WHITE)
        d.text((X, text_y(7)), "[%s] 100%%" % ("█" * cells), font=F, fill=WHITE)
        r = 7 + (k % 4)
        d.ellipse([X, text_y(8) + 6 - r, X + 2 * r, text_y(8) + 6 + r], fill=ACCENT)
        d.text((X + 28, text_y(8)), "SYSTEM ONLINE", font=F, fill=WHITE)
        frames.append(img)

    to_gif(frames, os.path.join(HERE, "boot.gif"))


def make_online():
    # Paleta fija: indice 0 = transparente. Sin adaptive para no romper colores.
    S = 32
    palette = [255, 0, 255, 56, 189, 248, 18, 70, 100, 10, 36, 54] + [0] * (768 - 12)
    frames = []
    for k in range(8):
        # Sin fotogramas consecutivos identicos: Pillow los colapsa.
        inset = 3 + k if k < 4 else 10 - k  # 3,4,5,6,4,3,2,1
        img = Image.new("P", (S, S), 0)
        img.putpalette(palette)
        d = ImageDraw.Draw(img)
        d.ellipse([inset, inset, S - inset, S - inset], outline=2 + (k % 2), width=2)
        d.ellipse([S // 2 - 6, S // 2 - 6, S // 2 + 6, S // 2 + 6], fill=1)
        frames.append(img)
    out = os.path.join(HERE, "online.gif")
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=120, loop=0, transparency=0, optimize=True)
    print("online.gif: %d frames, %d bytes" % (len(frames), os.path.getsize(out)))


if __name__ == "__main__":
    make_boot()
    make_online()
