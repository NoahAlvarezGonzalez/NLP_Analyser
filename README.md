# NLP_Analyser

https://nlp-analyser-noah.herokuapp.com

# Goal

Analyse text using NPL. 

Four main usage :

* Tokenize
* Extract entities
* Get the general sentiment of a text
* Summaryze a text

# Requirements

* Streamlit : to showcase the app
* Spacy : to tokenize, extract entities and get stopwords in different languagues
* Textblob : to get the sentiment of a text
* Textblob_fr : to do the same in french

# How it works

* The user is presented with four different options corresponding to each usage of the program detailled in the Goal header
* He can select to either use english or french, but it only has an impact on the last two usage (get the sentiment & summaryze a text)
* In the tokenize section, the text entered by the user is return tokenized
* The extract entities extract them from the entered text and show what they correspond to (ex : Google is an ORG, as in organisation)
* Get sentiment inform the user if he entered a positive, neutral or negative text
* Finaly, the summaryze section return a summary of the entered text correspond to 30% of it's length


