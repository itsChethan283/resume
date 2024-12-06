import streamlit as st
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import warnings
from PIL import Image, ImageOps, ImageDraw
warnings.filterwarnings("ignore", message="missing ScriptRunContext!")
import requests
from langchain.prompts import PromptTemplate

llm = GoogleGenerativeAI(model="gemini-pro", api_key="AIzaSyCH-FPn68zYhVAeYfepmxt-W5O6iWMrfDQ")

st.set_page_config(layout="wide")
st.title("Chethan S")


def circular_image(image_path, size=(200, 200)):
    img = Image.open(image_path).resize(size, Image.LANCZOS)
    mask = Image.new('L', size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size[0], size[1]), fill=255)
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

image, details, chat = st.columns([1, 2, 3])
with image:
     st.image(circular_image("rounded_pic.jpg"))

with details:
    st.header("Personal Info..")
    detail, ddk = st.columns([15,1])
    # icons = ["📧", "📞", "📅", "🌏", "🔗", "🔗"]
    dets = ["📧 &nbsp; &nbsp; [srichethan283@gmail.com](mailto:srichethan283@gmail.com)", "📞 &nbsp; &nbsp; [6383367510](tel:6383367510)", "📅 &nbsp; &nbsp; 31/08/1999", "🌏 &nbsp; &nbsp; Indian", "🔗 &nbsp; &nbsp; [itsChethan283 (Github)](https://github.com/itsChethan283)", "🔗 &nbsp; &nbsp; [chethans283 (LinkedIn)](https://www.linkedin.com/in/chethans283/)"]
    with st.container():
        for i, de in zip(range(6), dets):
            # with icon:
            #     st.markdown(f"""{ic}""", unsafe_allow_html=True)
            with detail:
                st.markdown(f"""{de}""", unsafe_allow_html=True)
            i = i + 1
def chatting(user_ques):
    embedding_model = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", google_api_key="AIzaSyCH-FPn68zYhVAeYfepmxt-W5O6iWMrfDQ")
    vectorstore = FAISS.load_local("resume_vec", embedding_model, allow_dangerous_deserialization=True)
    relavent_chunks = vectorstore.similarity_search(user_ques)
    # retriver = VectorStoreRetriever(vectorstore=vectorstore)
    prompt_template = """
        You are answering as if you are the owner of the resume and speaking in the first person. Respond only based on the information provided in the resume. If someone appreciates your accomplishments or skills, kindly say, "Thank you!" If a question is unrelated to the resume or offensive, respond politely with, "I’m sorry, but I cannot answer that question."
        Make your responses clear, professional, and aligned with the tone of a resume owner.
        The context and the question asked is given below
                Context: {context}
                Question: {input}
        ---------------------------------------------------
        """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    return chain.invoke({"input":user_ques, "context":relavent_chunks})

with chat:
    cont = st.container(height=400)
    with cont:
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            if message["type"] == "question":
                st.markdown(f'''<p style="color: #000000;  
                            overflow: auto;
                            position: absolute; 
                            right: 0px;  
                            background-color: #ffffff; 
                            display: inline-block; 
                            border-radius: 10px;
                            padding: 5px 15px 5px 15px; 
                            text-align: left">{message["content"]}</p>''', unsafe_allow_html=True)
            if message["type"] == "answer":
                st.markdown(f'''<p style="color: #000000; 
                            overflow: auto;
                            position: relative;
                            margin-top: 5%;
                            margin-bottom: 5%;
                            background-color: #e0eee1; 
                            display: inline-block; 
                            border-radius: 10px;
                            padding: 5px 15px 5px 15px; 
                            text-align: left">{message["content"]}</p>''', unsafe_allow_html=True)
        user_ques = st.chat_input("Know about me")
        if user_ques != None:
            res = chatting(user_ques)
            ress = res.split("\n")
            response_change = ""
            for response in ress:
                response_change = response_change + response + "<BR>"  
            st.markdown(f'''<p style="color: #000000; 
                        position: absolute; 
                        right: 0px;  
                        margin-bottom: 10px; 
                        background-color: #ffffff; 
                        display: inline-block; 
                        border-radius: 10px;
                        padding: 5px 15px 5px 15px; 
                        text-align: left">{user_ques}</p>''', unsafe_allow_html=True)
            st.session_state.messages.append({"type": "question", "content":user_ques})

            st.markdown(f'''<p style="position: relative;
                        background-color: #e0eee1; 
                        margin-top: 5%;
                        margin-bottom: 5%;
                        color: #0f1116; 
                        display: inline-block; 
                        border-radius: 10px; 
                        padding: 5px 15px 5px 15px; 
                        text-align: left">{response_change}</p>''', unsafe_allow_html=True)
            st.session_state.messages.append({"type": "answer", "content":response_change})


st.header("Profile")
st.write("""Detail-oriented data specialist with a knack for turning data into actionable insights. Experienced in spotting opportunities and improving processes to help company grow. Passionate about using data to solve problems and drive innovation""")

st.header("Languages")
st.markdown("- English")  
st.markdown("- Kannada(ಕನ್ನಡ)")
st.markdown("- Tamil(தமிழ்)") 
st.markdown("- Hindi(हिन्दी)")

#Education
edu, edu_toggle = st.columns([1,6])
with edu:
    st.header("Education")
with edu_toggle:
    edu_table = st.toggle("View as Table")
if edu_table:
    st.markdown("""| Degree | Institute | Duration |
|---|---|---|
| B.E. Robotics and Automation | [PSG College of Technology](https://www.psgtech.edu/) (*Coimbatore, India*) | Aug 2018 – May 2022 |
| 12th State Board(PCCM) | [Ebenezer Matric Hr Sec School](https://ebenezer.ac.in/) (*Tirupathur, India*) | Jun 2016 – Jun 2018 |""")
if edu_table == False:
    # st.write(r"$\textsf{\large B.E. Robotics and Automation}$", "[🔗](https://www.psgtech.edu/)")
    st.write("- **B.E. Robotics and Automation**, [*PSG College of Technology*](https://www.psgtech.edu/)  \nAug 2018 – May 2022 | Coimbatore, India")
    st.write("- **12th State Board(PCCM)**, [*Ebenezer Matric Hr Sec School*](https://ebenezer.ac.in/)  \nJun 2016 – Jun 2018 | Tirupathur, India")

#Certificates
certificates, cert_toggle = st.columns([2,6])
with certificates:
    st.header("Certificates")
with cert_toggle:
    cert_summarize = st.toggle("Summarize")
if cert_summarize:
    cert_summary = chatting("Can you explain in detail about the certificates you have given in your resume.")
    st.markdown(f"""{cert_summary}""")
if cert_summarize == False:
    st.write("**Machine Learning with Python** - *Coursera, IBM*[🔗](https://coursera.org/share/7ab8343745c5b1de658344a897363ac0)")
    st.write("**Dataiku** - *Core Designer and ML Practitioner*")
    st.write("**AZ-900** - *Azure Fundamentals*[🔗](https://learn.microsoft.com/api/credentials/share/en-us/ChethanS-5287/EB9E602281361B5B?sharingId=4DD6323CF8660707)")
    st.write("**Generative AI for Data Scientis** - *Coursera, IBM*[🔗](https://coursera.org/share/a23bdb7385c999a9877bd8864b6b2cc8)")
    st.write("**AI-900** - *Azure AI Fundamentals*[🔗](https://learn.microsoft.com/api/credentials/share/en-us/ChethanS-5287/7E5E3E346EBFFD0A?sharingId=4DD6323CF8660707)")

#Skills
skill, skill_table = st.columns([1,6])
with skill:
    st.header("Skills")
with skill_table:
    skill_toggle = st.toggle("View as Table", key=2)
if skill_toggle:
    st.markdown("""| Programming Proficiencies | Tools | Data Science | Generative AI |
|:---|:---|:---|:---|
| Python | Dataiku | Machine Learning | Azure OpenAI | 
| PySpark | Databricks | Natural Language Processing | Langchain |
| SQL | Azure Data Factory | Deep Learning | HuggingFace |
| | Azure API App | | RAG, Vectorstore, Embeddings |""")
if skill_toggle ==False:
    st.write("**Programming Proficiencies:**  - Python, PySpark, SQL")
    st.write("**Tools:**   Dataiku, Databricks, Azure Data Factory, Azure API App")
    st.write("**Data Science:**  Machine Learning , Natural Language Processing, Deep Learning")
    st.write("**Generative AI:**  Azure OpenAI, Langchain, HuggingFace, RAG, Vectorstore, Embeddings")

st.header("Projects")
st.write("""**RedLab**, *Chatbot Testing*  \n - Built a GenAI chatbot testing framework using Python, a Red Team approach to improve reliability and deployed on AWS.
- Created Red and Green apps for adversarial testing and validation, with detailed reporting.""")
st.write("""**Trade Promotions**, *(POC)*  \n - Built a technical architecture for a RAG-based chatbot with guardrails for secure, accurate responses.
- Created a demo version to showcase its functionality and compliance with the guardrails.""")
st.write("""**Altreryx to Dataiku**, *(POC)*  \n - Extracted data from YXMD files to generate corresponding PySpark functions.
- Developed a Python accelerator replicating Alteryx functions using PySpark in Dataiku.""")
st.write("""**Adobe ColdFusion to .Net**, *(POC)*  \n - Leveraged Azure OpenAI and open-source LLMs to assess conversion accuracy.
- Built a Python accelerator for functions with lower accuracy in the LLM evaluations.""")

st.header("Organisations")
st.write("**Student's Union**, *Core Member*  \n Sep 2019 – Jun 2021 | Coimbatore, India")
st.write("**NCC**, *Cadet Sergeant Major*  \n Sep 2018 – May 2021 | Coimbatore, India")

# st.components.v1.iframe("https://knowyourpdf.streamlit.app/?embedded=true", height=400, scrolling=True)


##Add a questionare bar to ask about him



