import streamlit as st

import spacy
from spacy.lang.en.stop_words import STOP_WORDS as STE
from spacy.lang.fr.stop_words import STOP_WORDS as STF
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from string import punctuation
from heapq import nlargest

stopwords_en = list(STE)
stopwords_fr = list(STF)
punctuation = punctuation + "\n"


def tokenizer(language, user_input):
    nlp = spacy.load(language)
    doc = nlp(user_input)
    data = ['"Tokens":{} \n"Lemma":{}'.format(token.text, token.lemma_) for token in doc]
    return data


def entitizer(language, user_input):
    nlp = spacy.load(language)
    doc = nlp(user_input)
    data = [(entity.text, entity.label_) for entity in doc.ents]
    return data


def sentimentizer(language, user_input):
    res = ""
    if language == "en":
        blob = TextBlob(user_input)
        x = blob.sentiment.polarity
        if x < 0:
            res = "Negative"
        elif x == 0:
            res = "Neutral"
        else:
            res = "Positive"

    elif language == "fr_core_news_sm":
        blob = TextBlob(user_input, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        x = blob.sentiment[0]
        if x < 0:
            res = "Negative"
        elif x == 0:
            res = "Neutral"
        else:
            res = "Positive"

    return res


def summarizer(doc, word_frequencies, stopwords):
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    # normalize word frequency
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    select_length = int(len(sentence_tokens) * 0.3)  # 30%

    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    return summary


def get_summary(language, user_input):
    nlp = spacy.load(language)
    doc = nlp(user_input)
    word_frequencies = {}
    if language == "en":
        stopwords = stopwords_en
        summary = summarizer(doc, word_frequencies, stopwords)
        final_summary = [word.text for word in summary]
        summary = " ".join(final_summary)
        return summary

    if language == "fr_core_news_sm":
        stopwords = stopwords_fr
        summary = summarizer(doc, word_frequencies, stopwords)
        final_summary = [word.text for word in summary]
        summary = " ".join(final_summary)
        return summary


def main():
    language = "en"
    st.title("NLP Analyzer")
    st.subheader("Natural Language Processing App")
    st.subheader("Select a Language")
    languages_list = ["English", "French"]
    language_choice = st.selectbox("Choose a Language", languages_list)

    if language_choice == "French":
        language = "fr_core_news_sm"

    if st.checkbox("Tokenize"):
        st.write("Tokenize your text")
        user_input = st.text_area("Enter your text here", key="token")
        if st.button("Analyze"):
            tokenizer_result = tokenizer(language, user_input)
            st.json(tokenizer_result)

    if st.checkbox("Entitize"):
        st.write("Extract entities from your text")
        user_input = st.text_area("Enter your text here", key="ent")
        if st.button("Extract"):
            entities_result = entitizer(language, user_input)
            st.json(entities_result)

    if st.checkbox("Sentitize"):
        st.write("Get the sentiment of your text")
        user_input = st.text_area("Enter your text here", key="sent")
        if st.button("Sentitize"):
            sentiment = sentimentizer(language, user_input)
            st.success(sentiment)

    if st.checkbox("Summarize"):
        st.write("Get a summary of your text")
        user_input = st.text_area("Enter your text here", key="sum")
        if st.button("Summarize"):
            summary = summarizer(language, user_input)
            st.write(summary)


if __name__ == "__main__":
    main()
