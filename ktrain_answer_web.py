from ktrain import text
import os
from os import path
import shutil
import streamlit as st
from ktrain_config import DATASET_NAME


@st.cache(allow_output_mutation=True)
def init():
    INDEX_DIR = DATASET_NAME + "/index"
    TXT_DIR = DATASET_NAME + "/txt"

    # if path.exists(INDEX_DIR):
    #     shutil.rmtree(INDEX_DIR)

    # text.SimpleQA.initialize_index(INDEX_DIR)
    # file_count = sum((len(f) for _, _, f in os.walk(TXT_DIR)))
    # text.SimpleQA.index_from_folder(TXT_DIR, INDEX_DIR, commit_every=file_count)
    qa = text.SimpleQA(INDEX_DIR)

    return qa


@st.cache()
def search(question: str, max_answers=5):
    answers = qa.ask(question)[:max_answers]
    df = qa.answers2df(answers)
    return df


qa = init()

st.title("To BERT or not to BERT")

question = st.text_input("What is your question?")
max_answers = st.selectbox("How much answers do you want?", options=[5, 10, 15], index=0)

if question != "":
    try:
        df = search(question=question, max_answers=max_answers)
        answer_found = True
    except:
        answer_found = False

    if answer_found:
        st.warning("Note: the **bold text** is the answer of the question, and the \
                    surrounding text is the context where the answer was found!")

        for _id in range(df.__len__()):
            context = str(df.loc[_id, "Context"]) \
                .replace("<font color='red'>", "<strong>") \
                .replace("</font>", "</strong>")
            st.markdown(context, unsafe_allow_html=True)

            confidence = "{:.10f}".format(df.loc[_id, "Confidence"])
            st.markdown("Confidence: " + confidence, unsafe_allow_html=True)

            st.markdown("<hr/>", unsafe_allow_html=True)
    else:
        st.error("Sorry, no answer on your question found.")
