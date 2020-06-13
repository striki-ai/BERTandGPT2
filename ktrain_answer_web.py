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
    df.rename({'Document Reference': 'Reference'}, axis=1, inplace=True)
    df.rename({"Candidate Answer": "Answer"}, axis=1, inplace=True)

    for _id in range(df["Context"].size):
        df.loc[_id,'Context'] = df.loc[_id,'Context'] \
            .replace("<div>", "") \
            .replace("</div>", "") \
            .replace("<font color='red'>", "[") \
            .replace("</font>", "]") \
            .strip()

    df.index += 1

    return df


qa = init()

st.title("To BERT or not to BERT")

question = st.text_input("What is your question?")
max_answers = st.selectbox("How much answers do you want?", options=[5, 10, 15], index=0)

if question != "":
    df = search(question=question, max_answers=max_answers)
    # df["Answer"] = df["Candidate Answer"]

    # st.write(df)
    # st.dataframe(df)
    st.table(df)
