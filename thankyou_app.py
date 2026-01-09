import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io

# ---------------- CONFIG ----------------
CARD_W_IN, CARD_H_IN = 3, 4
DPI = 300
W, H = CARD_W_IN * DPI, CARD_H_IN * DPI

BG_COLOR = (248, 241, 231)     # Cream
TEXT_COLOR = (74, 44, 42)     # Dark brown

FONT_REG = "fonts/DejaVuSerif.ttf"
FONT_BOLD = "fonts/DejaVuSerif-Bold.ttf"

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Thank You Card Generator", layout="centered")

# ---------- CSS (PREVIEW CONTROL) ----------
st.markdown("""
<style>
img {
    max-width: 100%;
    height: auto;
}
</style>
""", unsafe_allow_html=True)

st.title("🍬 Shree Jaslok – Thank You Card Generator")
st.caption("Fixed 3 × 4 inch | Print Ready | Editable")

st.divider()

# ---------------- LOGO CLEANER ----------------
def remove_black_bg(img):
    img = img.convert("RGBA")
    data = np.array(img)
    r, g, b, a = data.T
    mask = (r < 40) & (g < 40) & (b < 40)
    data[..., 3][mask] = 0
    return Image.fromarray(data)

# ---------------- INPUTS ----------------
logo_file = st.file_uploader("Upload Logo (black background OK)", ["png", "jpg", "jpeg"])
logo_size = st.slider("Logo Size (recommended 120–160)", 100, 220, 140)

thank_you = st.text_input("Thank You Line", "Thank You __________ 🙏")
shop_name = st.text_input("Shop Name", "Shree Jaslok Sweets Corner")
tagline = st.text_input("Tagline", "Made Fresh • Made with Love")

review_line = st.text_input("Review Line", "Enjoyed our sweets & snacks?")
instagram = st.text_input("Instagram", "@shreejasloksweets")
whatsapp = st.text_input("WhatsApp", "9987906814")

# ---------------- GENERATE ----------------
if st.button("🎨 Generate Card"):
    # ========== FRONT ==========
    front = Image.new("RGB", (W, H), BG_COLOR)
    df = ImageDraw.Draw(front)

    f_big = ImageFont.truetype(FONT_BOLD, 52)
    f_mid = ImageFont.truetype(FONT_REG, 42)
    f_small = ImageFont.truetype(FONT_REG, 32)

    y = 40

    if logo_file:
        logo = Image.open(logo_file)
        logo = remove_black_bg(logo)
        logo = logo.resize((logo_size, logo_size))
        front.paste(logo, ((W - logo_size)//2, y), logo)
        y += logo_size + 35

    df.text((W//2, y), thank_you, fill=TEXT_COLOR, font=f_mid, anchor="mm")
    y += 70

    df.text((W//2, y), "For Choosing", fill=TEXT_COLOR, font=f_small, anchor="mm")
    y += 45

    df.text((W//2, y), shop_name, fill=TEXT_COLOR, font=f_big, anchor="mm")
    y += 70

    df.text((W//2, y), tagline, fill=TEXT_COLOR, font=f_small, anchor="mm")

    # ========== BACK ==========
    back = Image.new("RGB", (W, H), BG_COLOR)
    db = ImageDraw.Draw(back)

    yb = 120

    db.text((W//2, yb), review_line, fill=TEXT_COLOR, font=f_mid, anchor="mm")
    yb += 65

    db.text((W//2, yb), "Please rate us on", fill=TEXT_COLOR, font=f_small, anchor="mm")
    yb += 45

    db.text((W//2, yb), "Zomato / Swiggy", fill=TEXT_COLOR, font=f_big, anchor="mm")
    yb += 80

    db.text(
        (W//2, yb),
        f"Tag us on Instagram\n{instagram}",
        fill=TEXT_COLOR,
        font=f_small,
        anchor="mm",
        align="center"
    )
    yb += 85

    db.text(
        (W//2, yb),
        f"For festive & bulk orders\nWhatsApp: {whatsapp}",
        fill=TEXT_COLOR,
        font=f_small,
        anchor="mm",
        align="center"
    )

    # ---------------- PREVIEW ----------------
    st.subheader("👀 Preview")
    c1, c2 = st.columns(2)
    c1.image(front, caption="Front Side")
    c2.image(back, caption="Back Side")

    # ---------------- DOWNLOAD ----------------
    f_buf, b_buf = io.BytesIO(), io.BytesIO()
    front.save(f_buf, "PNG", dpi=(300, 300))
    back.save(b_buf, "PNG", dpi=(300, 300))

    c1.download_button("⬇ Front (Print PNG)", f_buf.getvalue(), "front.png", "image/png")
    c2.download_button("⬇ Back (Print PNG)", b_buf.getvalue(), "back.png", "image/png")
