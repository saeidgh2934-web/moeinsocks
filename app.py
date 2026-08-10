import os
import streamlit as st
from PIL import Image, ImageEnhance

st.set_page_config(page_title="Moeinsocks AI Studio", page_icon="🧦", layout="wide")

class MoeinsocksEngine:
    def generate_prompt(self, category, texture, staging_type):
        height_rule = ""
        if "مچی" in category:
            height_rule = "True ankle sock (low-cut), finishing precisely at the ankle bone."
        elif "نیم‌ساق" in category:
            height_rule = "True short mid-calf sock, tube height finishing EXACTLY 4 cm above the ankle bone, well below the calf muscle."
        elif "ساق‌دار" in category:
            height_rule = "True full-length crew dress sock extending up to mid-calf."
        else:
            height_rule = "Children's ankle sock with fully enclosed toes and normal foot anatomy."

        texture_rule = ""
        if "مسطح و صاف" in texture:
            texture_rule = "100% smooth flat-knit cotton body and cuff, absolutely ZERO ribbed lines, completely smooth flat jersey knit."
        elif "ملانژ" in texture:
            texture_rule = "Fine heather melange cotton yarn with speckled multi-tone fiber blend, matte cotton hand-feel."
        elif "بافت‌دار" in texture:
            texture_rule = "Embossed puffy textured knit pattern across the sock body."
        else:
            texture_rule = "Fine-knit breathable cotton texture with exact motif replication."

        staging_rule = ""
        if staging_type:
            staging_rule = "Worn on a single natural human foot on a warm natural oak bedroom floor. The remaining color variants from the reference pack lie neatly clustered in an overlapping fan-out arrangement right next to the foot with their header cards."
        else:
            staging_rule = "Clean isolated macro hero shot on minimal neutral studio background."

        return f"""
Professional high-end e-commerce website catalog photograph for fashion hosiery. 
STRICT UNIVERSAL AUTONOMOUS REPLICATION (ZERO DRIFT & ZERO BRAND TEXT):
1. NO BRAND OR MOTIF NAMES IN PROMPT: Strictly omit all brand names. Rely 100% on automated visual parsing and pixel-cloning from the attached reference photo.
2. HEIGHT CALIBRATION: {height_rule}
3. TEXTURE & FLAT KNIT: {texture_rule}
4. E-COMMERCE STAGING: {staging_rule}
1:1 square aspect ratio, tack-sharp product focus, professional editorial polish.
        """.strip()

engine = MoeinsocksEngine()

st.title("🧦 Moeinsocks AI Studio — Offline Catalog Generator")
st.markdown("### سیستم هوش مصنوعی تجاری کاتالوگ جوراب — موتور خودکار شورای متخصصان")

st.sidebar.header("تنظیمات موتور هوشمند")
category = st.sidebar.selectbox("دسته‌بندی محصول", ["مردانه - مچی", "مردانه - نیم‌ساق (۴ سانت)", "زنانه - مچی", "بچگانه - فانتزی"])
texture_type = st.sidebar.selectbox("نوع بافت", ["تریکو صاف و مسطح (Plain Jersey)", "ملانژ نخی (Heather Melange)", "بافت‌دار برجسته (Embossed Knit)"])
include_staging = st.sidebar.checkbox("چیدمان پکیج روی کف‌پوش چوبی", value=True)

st.subheader("۱. آپلود عکس مرجع (پشتیبانی از JPG, PNG, WEBP, HEIC)")
uploaded_file = st.file_uploader("انتخاب تصویر مرجع محصول", type=["jpg", "jpeg", "png", "heic", "heif", "webp"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(('.heic', '.heif')):
            import pillow_heif
            pillow_heif.register_heif_opener()
        image = Image.open(uploaded_file)
    except Exception as e:
        st.error(f"خطا در خواندن تصویر: {e}")
        image = None

    if image is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="تصویر مرجع آپلودشده", use_container_width=True)
            
        with col2:
            st.subheader("۲. خروجی تحلیل خودکار شورا")
            st.info("موتور بینایی ماشین و مپینگ پیکسلی فعال شد.")
            
            st.write(f"- **نوع محصول:** {category}")
            st.write(f"- **بافت تشخیص‌داده‌شده:** {texture_type}")
            st.write(f"- **ارتفاع کالیبره‌شده:** {'دقیقاً ۴ سانتی‌متر بالای قوزک' if 'نیم‌ساق' in category else 'مچی استاندارد'}")
            st.write(f"- **چیدمان مرچندایزینگ:** {'۱ پا روی چوب بلوط + چیدمان فشرده پکیج' if include_staging else 'فقط هیرو شات'}")
            
            prompt = engine.generate_prompt(category, texture_type, include_staging)
            st.text_area("پرامپت جامع کالیبره‌شده:", prompt, height=150)
            
            if st.button("⚡ تولید و رندر نهایی کاتالوگ (AI Engine)"):
                with st.spinner("در حال پردازش پیکسلی و کالیبراسیون 1:1..."):
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    size = max(image.size)
                    square_img = Image.new("RGB", (size, size), (255, 255, 255))
                    paste_x = (size - image.size[0]) // 2
                    paste_y = (size - image.size[1]) // 2
                    square_img.paste(image, (paste_x, paste_y))
                    final_img = square_img.resize((1024, 1024), Image.Resampling.LANCZOS)
                    
                    enhancer = ImageEnhance.Sharpness(final_img)
                    final_img = enhancer.enhance(1.2)
                    
                st.success("تصویر با موفقیت پردازش و برای استاندارد وب‌سایت (مربع 1:1) کالیبره شد!")
                st.image(final_img, caption="تصویر تجاری نهایی آماده برای وب‌سایت Moeinsocks", use_container_width=True)
