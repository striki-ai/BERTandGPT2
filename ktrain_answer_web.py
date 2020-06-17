from ktrain import text
import os
from os import path
import shutil
import streamlit as st


@st.cache(allow_output_mutation=True)
def init():
    INDEX_DIR = "/tmp/index"
    TXT_DIR = "txt"

    if path.exists(INDEX_DIR):
        shutil.rmtree(INDEX_DIR)

    text.SimpleQA.initialize_index(INDEX_DIR)
    file_count = sum((len(f) for _, _, f in os.walk(TXT_DIR)))
    text.SimpleQA.index_from_folder(TXT_DIR, INDEX_DIR, commit_every=file_count)
    qa = text.SimpleQA(INDEX_DIR)

    return qa


@st.cache()
def search(question: str, max_answers=5):
    answers = qa.ask(question)[:max_answers]
    df = qa.answers2df(answers)
    return df


qa = init()

st.markdown('<style>' + open("ktrain_answer_web.css").read() + '</style>', unsafe_allow_html=True)

st.title("To BERT or not to BERT")

question = st.text_input("What is your question?")
max_answers = st.selectbox("How much answers do you want?", options=[5, 10, 15], index=0)

if question != "":
    df = search(question=question, max_answers=max_answers)

    st.markdown("Note: the <strong>bold text</strong> is the answer of the question, and the \
                 surrounding text is the context where the answer was found!", unsafe_allow_html=True)

    for _id in range(df.__len__()):
        context = str(df.loc[_id, "Context"]) \
            .replace("<font color='red'>", "<strong>") \
            .replace("</font>", "</strong>")

        confidence = "{:.5f}".format(df.loc[_id, "Confidence"] * 100) + " %"

        url= "https://" + df.loc[_id, "Document Reference"][:-10].replace("___", "/")

        url_and_confidence = "<a href=\"" + url + "\" target=\"_blank\"> Source Page" \
            + "</a>" + " [Confidence: " + confidence + "]"

        div_content = "<div class=\"answer-content\">" \
            + context \
            + url_and_confidence \
            + "</div>"

        st.markdown(div_content, unsafe_allow_html=True)
