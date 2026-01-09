import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ---------------- CONFIG ----------------
CARD_WIDTH_IN = 3
CARD_HEIGHT_IN = 4
DPI = 300
WIDTH = CARD_WIDTH_IN * DPI
HEIGHT = CARD_HEIGHT_IN * DPI

BG_COLOR = "#F8F1E7"     # Cream
TEXT_COLOR = "#4A2C2A"   # Dark brown

FONT_REG = "fonts/DejaVuSerif.ttf"
FONT_BOLD = "fonts/DejaVuSerif-Bold.ttf"

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Shree Jaslok – Thank You Card Generator",
    layout="centered"
)

st.title("🍬 Shree Jaslok Sweets – Thank You Card Generator")
st.caption("3 × 4 inch | Print-ready | Editable | Swiggy & Zomato")

st.divider()

# ---------------- INPUTS ----------------
st.subheader("🔧 Front Side Settings")

logo_file = st.file_uploader(
    "Upload Logo (PNG preferred)",
    type=["png", "jpg", "jpeg"]
)

logo_size = st.slider(
    "Logo Size (recommended 140–180)",
    min_value=100,
    max_value=260,
    value=150
)

thank_you_line = st.text_input(
    "Thank You Line (leave blank space for customer name)",
    "Thank You __________ 🙏"
)

shop_name = st.text_input(
    "Shop Name",
    "Shree Jaslok Sweets Corner"
)

tagline = st.text_input(
    "Tagline",
    "Made Fresh • Made with Love"
)

st.divider()

st.subheader("🔧 Back Side Settings")

review_line = st.text_input(
    "Review Line",
    "Enjoyed our sweets & snacks?"
)

instagram = st.text_input(
    "Instagram Handle",
    "@shreejasloksweets"
)

whatsapp = st.text_input(
    "WhatsApp Number",
    "9987906814"
)

# ---------------- GENERATE BUTTON ----------------
if st.button("🎨 Generate Card"):
    # ========== FRONT SIDE ==========
    front = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw_f = ImageDraw.Draw(front)

    font_big = ImageFont.truetype(FONT_BOLD, 60)
    font_mid = ImageFont.truetype(FONT_REG, 44)
    font_small = ImageFont.truetype(FONT_REG, 34)

    y = 50

    # Logo
    if logo_file:
        logo = Image.open(logo_file).convert("RGBA")
        logo = logo.resize((logo_size, logo_size))
        front.paste(logo, ((WIDTH - logo_size) // 2, y), logo)
        y += logo_size + 35

    # Thank you
    draw_f.text(
        (WIDTH // 2, y),
        thank_you_line,
        fill=TEXT_COLOR,
        font=font_mid,
        anchor="mm"
    )
    y += 80

    draw_f.text(
        (WIDTH // 2, y),
        "For Choosing",
        fill=TEXT_COLOR,
        font=font_small,
        anchor="mm"
    )
    y += 55

    draw_f.text(
        (WIDTH // 2, y),
        shop_name,
        fill=TEXT_COLOR,
        font=font_big,
        anchor="mm"
    )
    y += 80

    draw_f.text(
        (WIDTH // 2, y),
        tagline,
        fill=TEXT_COLOR,
        font=font_small,
        anchor="mm"
    )

    # ========== BACK SIDE ==========
    back = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw_b = ImageDraw.Draw(back)

    yb = 120

    draw_b.text(
        (WIDTH // 2, yb),
        review_line,
        fill=TEXT_COLOR,
        font=font_mid,
        anchor="mm"
    )
    yb += 70

    draw_b.text(
        (WIDTH // 2, yb),
        "Please rate us on",
        fill=TEXT_COLOR,
        font=font_small,
        anchor="mm"
    )
    yb += 50

    draw_b.text(
        (WIDTH // 2, yb),
        "Zomato / Swiggy",
        fill=TEXT_COLOR,
        font=font_big,
        anchor="mm"
    )
    yb += 90

    draw_b.text(
        (WIDTH // 2, yb),
        f"Tag us on Instagram\n{instagram}",
        fill=TEXT_COLOR,
        font=font_small,
        anchor="mm",
        align="center"
    )
    yb += 90

    draw_b.text(
        (WIDTH // 2, yb),
        f"For festive & bulk orders\nWhatsApp: {whatsapp}",
        fill=TEXT_COLOR,
        font=font_small,
        anchor="mm",
        align="center"
    )

    # ---------------- PREVIEW ----------------
    st.subheader("👀 Preview")
    col1, col2 = st.columns(2)
    col1.image(front, caption="Front Side")
    col2.image(back, caption="Back Side")

    # ---------------- DOWNLOAD ----------------
    st.subheader("⬇ Download for Printing")

    f_buf = io.BytesIO()
    front.save(f_buf, format="PNG", dpi=(300, 300))

    b_buf = io.BytesIO()
    back.save(b_buf, format="PNG", dpi=(300, 300))

    col1.download_button(
        "Download Front (PNG)",
        f_buf.getvalue(),
        file_name="thank_you_card_front.png",
        mime="image/png"
    )

    col2.download_button(
        "Download Back (PNG)",
        b_buf.getvalue(),
        file_name="thank_you_card_back.png",
        mime="image/png"
    )
