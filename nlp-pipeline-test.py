from transformers import pipeline
qapipe = pipeline('question-answering')
qapipe({
    'question': """how can question answering service produce answers""",
    'context': """One such task is reading comprehension.  Given a passage of text, we can ask questions about the passage that can be answered by referencing short excerpts from the text.  For instance, if we were to ask about this paragraph, "how can a question be answered in a reading comprehension task" . . . """
})