import streamlit as st
import py_avataaars as pa
from PIL import Image
import base64
import os
import matplotlib.pyplot as plt

# Helper function to create the avatar safely
def create_avatar(options):
    try:
        avatar = pa.PyAvataaar(
            style=getattr(pa.AvatarStyle, options['style']),
            skin_color=getattr(pa.SkinColor, options['skin_color']),
            top_type=getattr(pa.TopType, options['top_type']),
            hair_color=getattr(pa.HairColor, options['hair_color']),
            mouth_type=getattr(pa.MouthType, options['mouth_type']),
            eye_type=getattr(pa.EyesType, options['eye_type']),
            eyebrow_type=getattr(pa.EyebrowType, options['eyebrow_type']),
            accessories_type=getattr(pa.AccessoriesType, options['accessories_type']),
            clothe_type=getattr(pa.ClotheType, options['clothe_type']),
            clothe_graphic_type=getattr(pa.ClotheGraphicType, options['clothe_graphic_type'])
        )
        return avatar
    except Exception as e:
        st.error(f"Error creating avatar: {str(e)}")
        return None

# Helper function to allow image downloads
def imagedownload(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as image_file:
            b64 = base64.b64encode(image_file.read()).decode()
            href = f'<a href="data:image/png;base64,{b64}" download={filename}>Download Avatar</a>'
            return href
    else:
        st.error("Image file not found!")
        return ""

# Function to plot personality traits
def plot_personality(traits):
    labels = list(traits.keys())
    values = list(traits.values())
    fig, ax = plt.subplots()
    ax.bar(labels, values, color='skyblue')
    ax.set_title("Personality Traits")
    ax.set_ylabel("Scores")
    ax.set_ylim(0, 100)
    st.pyplot(fig)

# Page title
st.markdown("""
# Advanced Avatar & Personality Insights

Design a custom avatar, and get accurate insights into your personality traits using modern frameworks.

---
""")

# Sidebar customization
st.sidebar.header("Customize Your Avatar")

# Avatar options
avatar_options = {
    "style": st.sidebar.selectbox("Style", ("CIRCLE", "TRANSPARENT")),
    "skin_color": st.sidebar.selectbox("Skin Color", ["TANNED", "YELLOW", "PALE", "LIGHT", "BROWN", "DARK_BROWN", "BLACK"]),
    "top_type": st.sidebar.selectbox("Head Top", ["NO_HAIR", "LONG_HAIR_BOB", "SHORT_HAIR_THE_CAESAR", "HIJAB"]),
    "hair_color": st.sidebar.selectbox("Hair Color", ["AUBURN", "BLACK", "BLONDE", "BROWN", "RED", "SILVER_GRAY"]),
    "clothe_type": st.sidebar.selectbox("Clothing Type", ["BLAZER_SHIRT", "GRAPHIC_SHIRT", "HOODIE"]),
    "clothe_graphic_type": st.sidebar.selectbox("Clothing Graphic", ["BAT", "DIAMOND", "HOLA", "SKULL"]),
    "mouth_type": st.sidebar.selectbox("Mouth Type", ["DEFAULT", "SMILE", "TONGUE", "SERIOUS"]),
    "eye_type": st.sidebar.selectbox("Eye Type", ["DEFAULT", "HAPPY", "SURPRISED", "WINK"]),
    "eyebrow_type": st.sidebar.selectbox("Eyebrow Type", ["DEFAULT", "RAISED_EXCITED", "FROWN_NATURAL"]),
    "accessories_type": st.sidebar.selectbox("Accessories", ["DEFAULT", "SUNGLASSES", "PRESCRIPTION_01"])
}

# Create and render avatar
st.subheader("Your Customized Avatar")
avatar = create_avatar(avatar_options)
if avatar:
    avatar.render_png_file("avatar.png")
    image = Image.open("avatar.png")
    st.image(image, caption="Your Avatar")
    st.markdown(imagedownload("avatar.png"), unsafe_allow_html=True)

# Personality analysis section
st.markdown("---")
st.header("Advanced Personality Insights")
st.write("**Describe yourself briefly by selecting your traits below:**")

# Personality traits
traits = {
    "Extraversion": st.slider("Extraversion (Outgoing vs. Reserved)", 0, 100, 50),
    "Agreeableness": st.slider("Agreeableness (Compassionate vs. Critical)", 0, 100, 50),
    "Conscientiousness": st.slider("Conscientiousness (Organized vs. Careless)", 0, 100, 50),
    "Neuroticism": st.slider("Neuroticism (Sensitive vs. Confident)", 0, 100, 50),
    "Openness": st.slider("Openness (Creative vs. Practical)", 0, 100, 50)
}

# Analyze personality traits
if st.button("Analyze Personality"):
    st.subheader("Your Personality Profile")
    st.write("Based on your self-assessment, here are your insights:")

    # Detailed breakdown
    if traits["Extraversion"] > 70:
        st.write("- **Extraverted:** You enjoy socializing and feel energized by interacting with people.")
    elif traits["Extraversion"] < 30:
        st.write("- **Introverted:** You prefer solitary activities and value introspection.")
    
    if traits["Agreeableness"] > 70:
        st.write("- **Empathetic:** You are highly compassionate and enjoy helping others.")
    elif traits["Agreeableness"] < 30:
        st.write("- **Critical Thinker:** You value rationality and may come across as straightforward.")

    if traits["Conscientiousness"] > 70:
        st.write("- **Highly Organized:** You are disciplined and reliable, often planning ahead.")
    elif traits["Conscientiousness"] < 30:
        st.write("- **Spontaneous:** You prefer flexibility over structure in your life.")

    if traits["Neuroticism"] > 70:
        st.write("- **Emotionally Sensitive:** You experience emotions intensely and may need mindfulness practices.")
    elif traits["Neuroticism"] < 30:
        st.write("- **Emotionally Resilient:** You maintain calm and confidence even under pressure.")

    if traits["Openness"] > 70:
        st.write("- **Highly Creative:** You enjoy exploring new ideas and experiences.")
    elif traits["Openness"] < 30:
        st.write("- **Practical and Grounded:** You prefer tried-and-tested methods.")

    st.write("**Summary:** These traits can help you identify areas for growth and improvement.")

    # Show visualization
    plot_personality(traits)

st.markdown("---")
st.markdown("**App Built with Streamlit and Python**")
