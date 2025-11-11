import streamlit as st
from models.caption_model import generate_caption_blip_small
from models.llama_caption import refine_caption_llama

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Image Captioning",
    page_icon="🖼️",
    layout="centered"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fc;
    }
    .title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #2d3748;
    }
    .subtitle {
        text-align: center;
        color: #4a5568;
        margin-bottom: 2rem;
        font-size: 1.05rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #4F46E5;
        color: white;
        font-weight: 600;
        padding: 0.6rem;
        border: none;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #4338CA;
        transform: scale(1.02);
    }
    .result-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        margin-top: 1rem;
    }
    .caption-text {
        font-size: 1.05rem;
        color: #2d3748;
        font-style: italic;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="title">🖼️ Image Captioning — BLIP + LLaMA on Groq</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload an image to generate and refine captions using BLIP and LLaMA models.</p>', unsafe_allow_html=True)

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Preview", use_container_width=True)

    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        with st.spinner("🔍 Analyzing image with BLIP..."):
            blip_caption = generate_caption_blip_small(uploaded_file)
        st.markdown("#### 🧠 Raw Caption (BLIP)")
        st.markdown(f"<div class='result-card'><p class='caption-text'>{blip_caption}</p></div>", unsafe_allow_html=True)

    with col2:
        with st.spinner("🪄 Refining caption with LLaMA..."):
            final_caption = refine_caption_llama(blip_caption)
        st.markdown("#### ✨ Refined Caption (LLaMA)")
        st.markdown(f"<div class='result-card'><p class='caption-text'>{final_caption}</p></div>", unsafe_allow_html=True)

    st.divider()
    st.markdown("✅ *Both captions are generated locally and refined in real-time using Groq’s accelerated LLaMA inference.*")

else:
    st.info("👆 Upload an image above to begin caption generation.")
