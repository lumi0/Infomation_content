#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import numpy as np
from collections import Counter
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


def make_dictionary(train_dir):
    emails = [os.path.join(train_dir, f) for f in os.listdir(train_dir)]
    text = ''
    for mail in emails:
        with open(mail) as m:
            f = m.read()
            text += f
    string = re.sub('[^a-zA-Z]', ' ', text)
    string = re.sub(r'\s+', ' ', string).lower()
    stop_words = set(stopwords.words('english'))
    stop_words1 = ['hi', 'x', 'py', 'hl', 'en', 'e', 'mg',  'the', 'be']

    # print(stop_words)
    tokenizer = RegexpTokenizer('[a-z]+')  # 只匹配单词，由于已经全为小写，故可以只写成[a-z]+
    lemmatizer = WordNetLemmatizer()
    token = tokenizer.tokenize(string)  # 分词
    token = [lemmatizer.lemmatize(w) for w in token if lemmatizer.lemmatize(w) not in stop_words]  # 停用词+词形还原
    token = [lemmatizer.lemmatize(w) for w in token if lemmatizer.lemmatize(w) not in stop_words1]
    # print(token)
    dic = Counter(token)
    print(len(dic.values()))
    dic = dic.most_common(400)
    print(dic)
    return dic


def extract_features(mail_dir):
    files = [os.path.join(mail_dir, fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files), 400))
    doc_id = 0
    for file in files:
        with open(file) as f:
            text = f.read()
            string = re.sub('[^a-zA-Z]', ' ', text)
            string = re.sub(r'\s+', ' ', string).lower()
            stop_words = set(stopwords.words('english'))
            stop_words1 = ['hi', 'x', 'py', 'hl', 'en', 'e', 'mg',  'the', 'be']

            tokenizer = RegexpTokenizer('[a-z]+')  # 只匹配单词，由于已经全为小写，故可以只写成[a-z]+
            lemmatizer = WordNetLemmatizer()
            token = tokenizer.tokenize(string)  # 分词

            token = [lemmatizer.lemmatize(w) for w in token if lemmatizer.lemmatize(w) not in stop_words]
            token = [lemmatizer.lemmatize(w) for w in token if lemmatizer.lemmatize(w) not in stop_words1]
            # print(token)
            for word in token:
                for i, d in enumerate(dictionary):
                    if d[0] == word:
                        features_matrix[doc_id, i] = token.count(word)
            doc_id = doc_id + 1
    return features_matrix

# Create a dictionary of words with its frequency


if __name__ == '__main__':
    train_dir = 'train-mails'
    dictionary = make_dictionary(train_dir)
    train_labels = np.zeros(30)
    train_labels[15:30] = 1
    train_matrix = extract_features(train_dir)
    # Training SVM and Naive bayes classifier and its variants
    model = LinearSVC()
    model.fit(train_matrix, train_labels)
    test_dir = 'test-mails'
    test_matrix = extract_features(test_dir)
    test_labels = np.zeros(20)
    test_labels[10:20] = 1
    result = model.predict(test_matrix)
    # print(test_labels)
    print(confusion_matrix(test_labels, result))


