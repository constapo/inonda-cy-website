#!/usr/bin/env python3
"""Build the Inonda LTD presentation video (EL + EN captions) from stock clips.

Usage: python3 make_video.py <clips_dir> <ffmpeg_dir> <out_dir>
Clips: free stock footage from Mixkit (Mixkit License) and Coverr (Coverr License), both free for
commercial use without attribution. Music: Mixkit "Deep Urban" (Mixkit Stock Music Free License).
"""
import os, subprocess, sys, json, unicodedata
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CLIPS, FFDIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FF, FP = os.path.join(FFDIR, "ffmpeg"), os.path.join(FFDIR, "ffprobe")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGO = os.path.join(ROOT, "public", "assets", "logo.png")
W, H, FPS = 1920, 1080, 30
NAVY, AMBER, WHITE = (11, 21, 48), (244, 163, 33), (255, 255, 255)
F = "/usr/share/fonts/truetype/noto/NotoSans-{}.ttf"
def font(w, s): return ImageFont.truetype(F.format(w), s)
def upper(t):  # Greek capitals carry no accent marks
    return unicodedata.normalize("NFC", "".join(ch for ch in unicodedata.normalize("NFD", t.upper()) if ch not in "\u0301\u0342"))
TMP = os.path.join(OUT, "tmp"); os.makedirs(TMP, exist_ok=True)

def C(name):  # clip path by short name
    for f in os.listdir(CLIPS):
        if f.startswith(name) and f.endswith(".mp4"): return os.path.join(CLIPS, f)
    raise SystemExit("missing clip " + name)

def dur(p):
    return float(subprocess.check_output([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))

def dims(p):
    o = json.loads(subprocess.check_output([FP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", p]))
    return o["streams"][0]["width"], o["streams"][0]["height"]

# ------------------------------------------------------------------ overlay graphics (PIL)
def logo_block(img):
    lg = Image.open(LOGO).convert("RGBA"); lg.thumbnail((74, 58))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((48, 44, 48 + 96, 44 + 80), 16, fill=(255, 255, 255, 235))
    img.alpha_composite(lg, (48 + (96 - lg.width) // 2, 44 + (80 - lg.height) // 2))
    d.text((160, 50), "INONDA LTD", font=font("ExtraBold", 38), fill=WHITE)
    d.text((161, 96), "inonda.org", font=font("SemiBold", 22), fill=AMBER)
    t = "+357 94 091 616"
    f = font("Bold", 30); tw = d.textlength(t, font=f)
    d.rounded_rectangle((W - 48 - tw - 44, 52, W - 48, 108), 28, fill=(11, 21, 48, 200))
    d.text((W - 48 - tw - 22, 60), t, font=f, fill=WHITE)

def gradient(img, top=False, strength=230, height=520):
    g = Image.new("L", (1, height))
    for y in range(height):
        g.putpixel((0, y), int(strength * (y / height) ** 1.6))
    g = g.resize((W, height))
    if top: g = g.transpose(Image.FLIP_TOP_BOTTOM)
    band = Image.new("RGBA", (W, height), NAVY + (0,)); band.putalpha(g)
    img.alpha_composite(band, (0, 0 if top else H - height))

def caption_png(path, tag, el, en):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gradient(img); gradient(img, top=True, strength=150, height=220); logo_block(img)
    d = ImageDraw.Draw(img); x = 96
    y = H - 300
    if tag:
        f = font("Bold", 26); d.rectangle((x, y + 14, x + 40, y + 18), fill=AMBER)
        d.text((x + 56, y), upper(tag), font=f, fill=AMBER); y += 52
    d.text((x, y), el, font=font("ExtraBold", 68), fill=WHITE); y += 92
    d.text((x, y), en, font=font("SemiBold", 40), fill=AMBER)
    img.save(path)

def card_png(path, num, el, en, sub=None):
    img = Image.new("RGBA", (W, H), NAVY + (165,))
    logo_block(img); d = ImageDraw.Draw(img)
    def ctext(t, f, y, fill):
        d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)
    y = 330
    if num: ctext(num, font("Bold", 34), y, AMBER); y += 70
    ctext(el, font("Black", 104), y, WHITE); y += 140
    d.rectangle((W / 2 - 60, y, W / 2 + 60, y + 5), fill=AMBER); y += 36
    ctext(en, font("SemiBold", 52), y, AMBER); y += 90
    if sub: ctext(sub, font("Medium", 36), y, (225, 230, 242))
    img.save(path)

def outro_png(path):
    img = Image.new("RGBA", (W, H), NAVY + (205,)); d = ImageDraw.Draw(img)
    lg = Image.open(LOGO).convert("RGBA"); lg.thumbnail((150, 118))
    d.rounded_rectangle((W / 2 - 100, 70, W / 2 + 100, 230), 26, fill=(255, 255, 255, 240))
    img.alpha_composite(lg, (int(W / 2 - lg.width / 2), int(150 - lg.height / 2)))
    def ctext(t, f, y, fill):
        d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)
    ctext("Ζητήστε δωρεάν προσφορά", font("Black", 76), 262, WHITE)
    ctext("Request a free quote", font("SemiBold", 44), 362, AMBER)
    people = [("Irina", "Διευθύντρια · Director", "+357 94 091 616", "Русский · Ελληνικά · English"),
              ("Constantin", "Γραμματεία · Τεχνίτης · Εργοδηγός", "+357 94 091 613", "Română · Ελληνικά · English")]
    for i, (n, role, ph, langs) in enumerate(people):
        x0 = 210 + i * 780; y0 = 470
        d.rounded_rectangle((x0, y0, x0 + 720, y0 + 300), 28, fill=(255, 255, 255, 30), outline=(255, 255, 255, 70), width=2)
        d.text((x0 + 40, y0 + 28), n, font=font("ExtraBold", 54), fill=WHITE)
        d.text((x0 + 40, y0 + 100), role, font=font("SemiBold", 28), fill=AMBER)
        d.text((x0 + 40, y0 + 150), ph, font=font("Black", 62), fill=WHITE)
        d.text((x0 + 40, y0 + 238), langs, font=font("Medium", 30), fill=(205, 214, 232))
    ctext("WhatsApp · Viber · inonda2026@outlook.com", font("SemiBold", 38), 820, WHITE)
    ctext("www.inonda.org", font("Black", 64), 890, AMBER)
    ctext("Λευκωσία & όλη η Κύπρος  ·  Nicosia & all of Cyprus", font("Medium", 32), 985, (205, 214, 232))
    img.save(path)

# ------------------------------------------------------------------ scene list
# (kind, clip, start, seconds, texts...)
S = []
def clip(c, st, sec, tag, el, en): S.append(("cap", c, st, sec, tag, el, en))
def card(c, st, sec, num, el, en, sub=None): S.append(("card", c, st, sec, num, el, en, sub))

card("mk47286", 8, 5, "", "Inonda LTD", "Maintain · Repair · Transform", "Συντήρηση · Επισκευές · Ανακαίνιση")
clip("coverr-outdoor-pool-near-a-villa", 4, 5, "Λευκωσία & όλη η Κύπρος · Nicosia & all of Cyprus", "Ένας εργολάβος για όλα", "One contractor for everything")
clip("mk773", 6, 4.5, "Αδειούχοι τεχνικοί · Licensed technicians", "Γραπτές προσφορές, εγγύηση", "Written quotes, workmanship warranty")
# Maintenance
card("coverr-attachments-for-power-tools", 3, 3.5, "01 / 03", "Συντήρηση", "Maintenance")
clip("mk1439", 3, 4.5, "Συντήρηση · Maintenance", "Προγράμματα συντήρησης", "Maintenance plans")
clip("coverr-attachments-for-power-tools", 12, 4, "Συντήρηση · Maintenance", "Τακτικός έλεγχος & σέρβις", "Scheduled checks & servicing")
clip("mk49185", 3, 5.5, "Συντήρηση · Maintenance", "Κλιματισμός", "Air conditioning: install, service, repair")
clip("mk14729", 2, 5, "Συντήρηση · Maintenance", "Στεγάνωση ταράτσας", "Roof waterproofing")
clip("mk45665", 6, 4.5, "Συντήρηση · Maintenance", "Τέλος στις διαρροές & την υγρασία", "Stop leaks, damp & mould")
# Repairs
card("coverr-a-handyman-at-work", 1, 3.5, "02 / 03", "Επισκευές", "Repairs")
clip("mk49024", 1, 5, "Επισκευές · Repairs", "Υδραυλικά", "Plumbing")
clip("mk49023", 2, 4.5, "Επισκευές · Repairs", "Αδειούχοι υδραυλικοί", "Licensed plumbers")
clip("coverr-dripping-faucet", 1, 4, "Επισκευές · Repairs", "Διαρροές, βουλώματα, θερμοσίφωνες", "Leaks, blockages, water heaters")
clip("mk23491", 8, 5, "Επισκευές · Repairs", "Ηλεκτρολογικά", "Electrical works")
clip("coverr-close-up-of-a-dual-power-outlet", 4, 4, "Επισκευές · Repairs", "Πρίζες, πίνακες, φωτισμός", "Sockets, panels, lighting")
clip("coverr-a-handyman-at-work", 4, 4.5, "Επισκευές · Repairs", "Μικροεπισκευές", "Handyman & small repairs")
clip("coverr-assembling-furniture", 2, 4, "Επισκευές · Repairs", "Συναρμολόγηση επίπλων", "Furniture assembly")
clip("coverr-drilling-nails-into-wood", 4, 4, "Επισκευές · Repairs", "Στερέωση & τοποθέτηση", "Fixing & mounting")
clip("mk47071", 5, 4.5, "Επισκευές · Repairs", "Επείγουσες επισκευές", "Urgent repairs, made safe fast")
# Transformation
card("coverr-interior-renovation", 2, 3.5, "03 / 03", "Ανακαίνιση", "Home transformation")
clip("coverr-interior-renovation", 5, 5, "Ανακαίνιση · Transformation", "Ολική ανακαίνιση", "Complete home renovation")
clip("mk1459", 1, 4.5, "Ανακαίνιση · Transformation", "Νέες διαρρυθμίσεις", "New layouts")
clip("mk1437", 4, 4.5, "Ανακαίνιση · Transformation", "Σχεδιασμός & προϋπολογισμός", "Planning & itemised budget")
clip("mk43033", 2, 5.5, "Ανακαίνιση · Transformation", "Ανακαίνιση κουζίνας", "Kitchen renovation")
clip("coverr-bathroom-interior-design", 5, 5, "Ανακαίνιση · Transformation", "Σύγχρονοι χώροι", "Modern living spaces")
clip("coverr-carrying-a-ceramic-toilet", 2, 4, "Ανακαίνιση · Transformation", "Ανακαίνιση μπάνιου", "Bathroom renovation")
clip("mk21766", 6, 5, "Ανακαίνιση · Transformation", "Ντουζιέρες δαπέδου", "Walk-in showers, full waterproofing")
clip("mk2307", 4, 5, "Ανακαίνιση · Transformation", "Βαφές & γυψοσανίδες", "Painting, plaster & gypsum")
clip("coverr-construction-work-on-a-roof", 3, 5, "Ανακαίνιση · Transformation", "Δάπεδα & πλακάκια", "Flooring & tiling")
clip("mk3110", 3, 4, "Ανακαίνιση · Transformation", "Φινιρίσματα που κρατούν", "Finishes that last")
clip("coverr-carpenter-works-with-a-miter-saw", 3, 5, "Ανακαίνιση · Transformation", "Κουφώματα & ξυλουργικά", "Doors, windows & carpentry")
clip("mk44864", 3, 4, "Ανακαίνιση · Transformation", "Κατά παραγγελία", "Made to measure")
clip("mk39692", 2, 4, "Ανακαίνιση · Transformation", "Ντουλάπες & εντοιχισμένα", "Wardrobes & built-ins")
clip("mk47286", 3, 5, "Ανακαίνιση · Transformation", "Εξωτερικοί χώροι", "Outdoor works")
clip("mk4045", 2, 4.5, "Ανακαίνιση · Transformation", "Πέργκολες, βεράντες, πισίνα", "Pergolas, terraces & pool areas")
# Process
card("mk16556", 3, 3.5, "", "Πώς δουλεύουμε", "How we work", "5 βήματα · 5 steps")
clip("mk1439", 9, 3.5, "01", "Πείτε μας τι χρειάζεστε", "Tell us what you need")
clip("mk16556", 8, 3.5, "02", "Αυτοψία & εκτίμηση", "Site visit & assessment")
clip("mk1437", 10, 3.5, "03", "Γραπτή, αναλυτική προσφορά", "Written, itemised quote")
clip("mk777", 10, 3.5, "04", "Σωστή εκτέλεση", "Work done right")
clip("mk3090", 3, 3.5, "05", "Παράδοση & εγγύηση", "Handover & warranty")
card("coverr-outdoor-pool-near-a-villa", 18, 5, "", "Χτισμένη σε δεσμεύσεις", "Built on clear promises",
     "Γραπτές προσφορές · Αδειούχοι τεχνικοί · Εγγύηση · Καθαριότητα")
S.append(("outro", "mk12877", 2, 12))

# ------------------------------------------------------------------ render
def vf_for(c, sec):
    w, h = dims(c)
    push = f"scale={int(W*1.06)}:{int(H*1.06)}:flags=lanczos,crop={W}:{H}:x='(iw-{W})*t/{sec}':y='(ih-{H})/2'"
    if h > w:  # portrait clip: blurred fill behind
        return (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.08[bg];"
                f"[b]scale=-2:{H}:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:0,fps={FPS},setsar=1[v0]")
    return f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{push},fps={FPS},setsar=1[v0]"

segs = []
for i, sc in enumerate(S):
    kind, c, st, sec = sc[0], C(sc[1]), sc[2], sc[3]
    st = max(0, min(st, dur(c) - sec - 0.1))
    png = os.path.join(TMP, f"o{i:02d}.png")
    if kind == "cap": caption_png(png, sc[4], sc[5], sc[6])
    elif kind == "card": card_png(png, sc[4], sc[5], sc[6], sc[7])
    else: outro_png(png)
    out = os.path.join(TMP, f"s{i:02d}.mp4")
    fade = f"fade=in:st=0.15:d=0.5:alpha=1" if kind == "cap" else "fade=in:st=0:d=0.6:alpha=1"
    fc = vf_for(c, sec) + f";[1:v]format=rgba,{fade}[ov];[v0][ov]overlay=0:0:format=auto,format=yuv420p[v]"
    cmd = [FF, "-v", "error", "-y", "-ss", str(st), "-t", str(sec), "-i", c, "-loop", "1", "-t", str(sec), "-i", png,
           "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS), out]
    subprocess.run(cmd, check=True); segs.append(out)
    print(f"scene {i+1}/{len(S)} {kind} {sec}s", flush=True)

lst = os.path.join(TMP, "list.txt")
open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
total = sum(sc[3] for sc in S)
silent = os.path.join(TMP, "silent.mp4")
subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
music = os.path.join(CLIPS, "music623.mp3")
final = os.path.join(OUT, "inonda-presentation-1080p.mp4")
subprocess.run([FF, "-v", "error", "-y", "-i", silent, "-i", music, "-filter_complex",
                f"[1:a]atrim=0:{total},afade=t=in:d=1.5,afade=t=out:st={total-3}:d=3,volume=0.85[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", final], check=True)
web = os.path.join(OUT, "inonda-presentation-720p.mp4")
subprocess.run([FF, "-v", "error", "-y", "-i", final, "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-crf", "26",
                "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", web], check=True)
subprocess.run([FF, "-v", "error", "-y", "-ss", "1.5", "-i", final, "-frames:v", "1", "-q:v", "3", os.path.join(OUT, "inonda-presentation-poster.jpg")], check=True)
print(f"done: {total:.1f}s ->", final)
