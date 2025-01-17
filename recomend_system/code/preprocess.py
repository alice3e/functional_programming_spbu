import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import pickle

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')



stop_words = set(stopwords.words('english'))
# Функция для предобработки текста
def preprocess_text(text):
    # Приводим текст к нижнему регистру
    text = text.lower()
    # Убираем пунктуацию
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Токенизация текста
    words = word_tokenize(text)
    # Убираем стоп-слова
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

# Загрузка CSV файла с метаданными книг
df = pd.read_csv('./dataset/cleaned_books.csv')
df.head()

# Применяем предобработку к каждому столбцу
df['processed_title'] = df['Title'].apply(preprocess_text)
df['processed_category'] = df['Category'].apply(preprocess_text)
df['processed_description'] = df['Description'].apply(preprocess_text)
df['processed_authors'] = df['Authors'].apply(preprocess_text)
df.head()

# Инициализируем один и тот же векторизатор для всех признаков
vectorizer = TfidfVectorizer()

# Преобразуем названия, категории и описания в векторы
title_vectors = vectorizer.fit_transform(df['processed_title'])
category_vectors = vectorizer.transform(df['processed_category'])  # используем transform, а не fit_transform
description_vectors = vectorizer.transform(df['processed_description'])
author_vectors = vectorizer.transform(df['processed_authors'])

with open('./dataset/processed_books.pkl', 'wb') as f:
    pickle.dump(df, f)
    pickle.dump(title_vectors, f)
    pickle.dump(category_vectors, f)
    pickle.dump(description_vectors, f)
    pickle.dump(author_vectors,f)
    pickle.dump(vectorizer, f)
    


