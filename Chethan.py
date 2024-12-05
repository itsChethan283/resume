import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
import warnings
from PIL import Image, ImageOps, ImageDraw
warnings.filterwarnings("ignore", message="missing ScriptRunContext!")

# llm = GoogleGenerativeAI(model="gemini-pro", api_key="AIzaSyCH-FPn68zYhVAeYfepmxt-W5O6iWMrfDQ")
# print(llm.invoke("What????"))

st.title("Chethan S")

def circular_image(image_path, size=(200, 200)):
    img = Image.open(image_path).resize(size, Image.LANCZOS)
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size[0], size[1]), fill=255)
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

image, details = st.columns(2)
with image:
     st.image(circular_image("81tzqIckFYL.jpg"))

with details:
    st.header("Personal Info..")
    icon, detail = st.columns([1,7])
    icons = ["📧", "📞", "📅", "🌏", "🔗", "🔗"]
    dets = ["[srichethan283@gmail.com](mailto:srichethan283@gmail.com)", "[6383367510](tel:6383367510)", "31/08/1999", "Indian", "[itsChethan283](https://github.com/itsChethan283)", "[chethans283](https://www.linkedin.com/in/chethans283/)"]
    with st.container():
        for i, ic, de in zip(range(6), icons, dets):
            with icon:
                st.markdown(f"""{ic}""", unsafe_allow_html=True)
            with detail:
                st.markdown(f"""{de}""", unsafe_allow_html=True)
            i = i + 1

m = "[Click here to visit Streamlit!](https://streamlit.io)"
st.markdown(f"{m}")

