import streamlit as st
import pandas as pd
import numpy as np
import os, pathlib, base64
from sklearn.metrics.pairwise import cosine_similarity

# إعداد الصفحة
st.set_page_config(page_title="Luxury Perfume Experience", layout="wide")

# 🌟 تصميم واجهة فاخرة (Gold × Black + Animation)
st.markdown("""
<style>
.stApp {
  background-color:#000;
  color:#f5f5f5;
  font-family:'Cairo',sans-serif;
  overflow-x:hidden;
}
h1, h2, h3 {text-align:center; color:#FFD700;}
.stButton>button {
  width:100%; height:85px;
  font-size:30px; font-weight:bold;
  border-radius:25px; border:none;
  background:linear-gradient(145deg,#d4af37,#b8860b);
  box-shadow:0 0 25px rgba(255,215,0,0.5);
  color:black;
  transition:all 0.3s ease;
}
.stButton>button:hover {
  background:linear-gradient(145deg,#ffd700,#f5c400);
  transform:scale(1.06);
  box-shadow:0 0 35px rgba(255,215,0,0.8);
}

.perfume-card:hover {
  transform:scale(1.03);
  box-shadow:0 0 45px rgba(255,215,0,0.4);
}
img {
  width:100%;
  height:400px;
  object-fit:cover;
  object-position:center;
  border-radius:25px;
  border:2px solid rgba(255,215,0,0.4);
  box-shadow:0 0 25px rgba(255,215,0,0.25);
  transition:transform 0.3s ease, box-shadow 0.3s ease;
}
img:hover {
  transform:scale(1.05);
  box-shadow:0 0 45px rgba(255,215,0,0.4);
}
.glow {
  background:linear-gradient(90deg,#d4af37,#fff8dc,#d4af37);
  background-size:200px 100%;
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  animation:shine 3s linear infinite;
}
@keyframes shine {
  0%{background-position:-200px 0;}
  100%{background-position:200px 0;}
}
</style>
""", unsafe_allow_html=True)

# 🖼️ تحميل الصور
BASE_DIR = pathlib.Path(__file__).parent.resolve()
IMAGES_DIR = BASE_DIR / "Perfume_Image"

def get_image_path(row):
    brand = str(row["brand_name"]).strip()
    image_id = str(row["id"]).strip()
    brand_dir = IMAGES_DIR / brand
    if not brand_dir.exists():
        return None
    for file in brand_dir.iterdir():
        if file.stem.strip().lower() == image_id.strip().lower():
            if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
                return str(file)
    return None

# 📊 تحميل البيانات
df = pd.read_csv(BASE_DIR / "products_with_images_strict1.csv")
df.columns = df.columns.str.strip().str.replace('\ufeff', '')
if "description" not in df.columns:
    df["description"] = "عطر فاخر يتميز بتوليفة متوازنة من المكونات العطرية."

df["image_path"] = df.apply(lambda r: get_image_path(r), axis=1)
default_img = "https://cdn-icons-png.flaticon.com/512/482/482469.png"
notes = ['Woody','Fruity','Floral','Oriental','Citrus','Sweet','Smoky','Amber','Fresh','Musk','Leathery']

# 🏠 شاشة الترحيب
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if st.session_state.page == "welcome":
    st.markdown("<h1 class='glow'>👑 مرحبًا بك في معرض العطور الفاخرة 👑</h1>", unsafe_allow_html=True)
    st.markdown("<h3>✨ استمتع بتجربة فريدة لاختيار عطرك المثالي ✨</h3>", unsafe_allow_html=True)
    st.image("D:\\dhifaf\\icon.jpg", width=220)
    if st.button("ابدأ التجربة 💎"):
        st.session_state.page = "selection"
        st.rerun()

# 🌸 صفحة اختيار الذوق
elif st.session_state.page == "selection":
    st.title("🌸 اختر المكونات العطرية التي تفضلها")
    selected_notes = st.multiselect("🎨 المكونات المفضلة:", notes)
    col1, col2 = st.columns(2)
    with col1:
        recommend = st.button("💫 اعرض التوصيات")
    with col2:
        restart = st.button("🔄 العودة")

    if restart:
        st.session_state.page = "welcome"
        st.rerun()

    if recommend:
        if not selected_notes:
            st.warning("يرجى اختيار مكون عطري واحد على الأقل.")
        else:
            user_vector = np.zeros(len(notes))
            for n in selected_notes:
                user_vector[notes.index(n)] = 1
            similarities = cosine_similarity([user_vector], df[notes].values)[0]
            df["similarity"] = similarities
            recs = df.sort_values(by="similarity", ascending=False).head(8)

            # 💎 عطرك المميز
            top = recs.iloc[0]
            st.markdown("<h2 class='glow'>💎 عطرك المميز</h2>", unsafe_allow_html=True)

            img_path = top["image_path"] if top["image_path"] and os.path.exists(top["image_path"]) else None

            if img_path:
                with open(img_path, "rb") as f:
                    img_data = f.read()
                img_base64 = base64.b64encode(img_data).decode()
                img_src = f"data:image/jpeg;base64,{img_base64}"
            else:
                img_src = default_img

            # ✅ الإطار الذهبي + لمعان + انعكاس
            st.markdown(f"""
            <div style="display:flex;justify-content:center;align-items:center;margin:30px auto;">
              <div style="
                position:relative;
                width:460px;
                height:460px;
                border-radius:30px;
                border:3px solid rgba(255,215,0,0.6);
                box-shadow:0 0 50px rgba(255,215,0,0.4);
                overflow:hidden;
                background:radial-gradient(circle at center, rgba(255,215,0,0.1), transparent 70%);
              ">
                <img src="{img_src}"
                     style="
                       width:100%;
                       height:100%;
                       object-fit:cover;
                       border-radius:30px;
                       animation:zoomSlow 6s ease-in-out infinite alternate;
                     "/>
                <div style="
                  position:absolute;
                  top:0; left:0; right:0; bottom:0;
                  border-radius:30px;
                  background:linear-gradient(120deg, rgba(255,215,0,0.25), transparent, rgba(255,215,0,0.25));
                  animation:lightmove 6s linear infinite;
                  pointer-events:none;
                "></div>
              </div>
            </div>

            

            <style>
            @keyframes lightmove {{
              0% {{ transform:translateX(-100%) rotate(10deg); }}
              50% {{ transform:translateX(100%) rotate(10deg); }}
              100% {{ transform:translateX(-100%) rotate(10deg); }}
            }}
            @keyframes zoomSlow {{
              0% {{ transform:scale(1); }}
              100% {{ transform:scale(1.05); }}
            }}
            </style>
            """, unsafe_allow_html=True)

            # ✨ نصوص العطر
            st.markdown(f"""
              <h2 style='color:#FFD700;text-align:center;'>{top['product_name']}</h2>
              <p style='font-size:22px; color:#f5f5f5;text-align:center;'>{top['brand_name']}</p>
              <p style='font-size:20px; color:#ccc;text-align:center;'>{top['description']}</p>
            """, unsafe_allow_html=True)

            # 🌟 العطور المشابهة
            st.markdown("<h2 class='glow'>✨ عطور مشابهة تناسب ذوقك ✨</h2>", unsafe_allow_html=True)
            cols = st.columns(4)
            for i, (_, row) in enumerate(recs.iloc[1:5].iterrows()):
                with cols[i]:
                    st.markdown("<div class='perfume-card'>", unsafe_allow_html=True)
                    img_url = row["image_path"] if row["image_path"] and os.path.exists(row["image_path"]) else default_img
                    st.image(img_url, use_container_width=True)
                    st.markdown(f"""
                        <h4 style='color:#FFD700;'>{row['product_name']}</h4>
                        <p style='color:#f5f5f5;'>{row['brand_name']}</p>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            # 🎁 باقتك الخاصة
            st.markdown("<h2 class='glow'>🎁 باقتك العطرية الخاصة</h2>", unsafe_allow_html=True)
            combo = recs.sample(3, random_state=42)
            cols = st.columns(3)
            for i, (_, row) in enumerate(combo.iterrows()):
                with cols[i]:
                    st.markdown("<div class='perfume-card'>", unsafe_allow_html=True)
                    img_url = row["image_path"] if row["image_path"] and os.path.exists(row["image_path"]) else default_img
                    st.image(img_url, use_container_width=True)
                    st.markdown(f"""
                        <h4 style='color:#FFD700;'>{row['product_name']}</h4>
                        <p style='color:#ccc;'>{row['brand_name']}</p>
                    """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<p style='text-align:center; color:#bbb;'>✨ تم إعداد هذه التوصيات خصيصًا لتناسب ذوقك الفريد ✨</p>", unsafe_allow_html=True)

