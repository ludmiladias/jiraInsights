import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import jira_utils as jira_utils
from dotenv import load_dotenv
import ai_utils 

load_dotenv() 

nltk.download('stopwords')
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english') + stopwords.words('portuguese'))

def fetch_bugs(jira, project_key):
    jql = f'project={project_key} AND issuetype=Bug'
    issues = jira.search_issues(jql, maxResults=False)
    return issues

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Zá-úÁ-Ú0-9 ]", " ", text)
    words = [w for w in text.split() if w not in STOPWORDS and len(w) > 2]
    return " ".join(words)

def extract_keywords_with_ia(issues):
    titles = [clean_text(i.fields.summary or "") for i in issues]
    #descriptions = [clean_text(i.fields.description or "") for i in issues]    
    prompt = ai_utils.generate_bug_analisys_prompt(titles)
    response_content = ai_utils.send_request_to_ai(prompt)

    keywords = []
    for key, value in response_content.items():
        keywords.append(key)

    
    return keywords


def extract_keywords(issues):
    qtd_keywords=2
    titles = [clean_text(i.fields.summary or "") for i in issues]

    vectorizer = TfidfVectorizer(stop_words=list(STOPWORDS))
    X = vectorizer.fit_transform(titles)
    terms = vectorizer.get_feature_names_out()

    keywords = []
    for title, row in zip(titles, X.toarray()):
        top_indices = row.argsort()[-qtd_keywords:][::-1]
        top_terms = [terms[i] for i in top_indices]

        # reordena termos conforme a ordem de aparição no título
        ordered_terms = sorted(
            top_terms,
            key=lambda w: title.split().index(w) if w in title.split() else float("inf")
        )

        keywords.append(" ".join(ordered_terms))

    return keywords

def generate_wordcloud(texts):
    full_text = " ".join(texts)
    wc = WordCloud(width=1200, height=800, background_color="white").generate(full_text)

    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":

    try:
        jira = jira_utils.connect_to_jira()
    except Exception as e:
        print("❌ Erro ao conectar no Jira:", e)
    
    issues = jira_utils.fetch_bugs()  


    # Extrair keywords dos títulos
    #compact_titles = extract_keywords(issues)
    compact_titles = extract_keywords_with_ia(issues)

    # Unir descrições + títulos sintetizados
    #all_texts = descriptions + compact_titles


    # Gerar nuvem de palavras
    if len(compact_titles)>0:
        generate_wordcloud(compact_titles)