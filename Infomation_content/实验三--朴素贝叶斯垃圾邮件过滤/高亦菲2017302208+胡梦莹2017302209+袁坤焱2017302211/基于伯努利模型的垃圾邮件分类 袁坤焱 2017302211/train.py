# -*- coding: utf-8 -*-

# from fwalker import fun
# from reader import readtxt
import os


def readtxt(path):
    with open(path, 'r',encoding='ISO-8859-15') as f:
        lines = f.readlines()
    return lines

def fileWalker(path):
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            eachpath = str(root+'\\'+fn)
            fileArray.append(eachpath)
    #print(fileArray)
    return fileArray

def email_parser(email_path):
    punctuations = """,.<>()*&^%$#@!'";~`[]{}|、\\/~+_-=?"""
    #print(email_path)
    content_list = readtxt(email_path)
    content = (' '.join(content_list)).replace('\r\n', ' ').replace('\t', ' ')
    clean_word = []
    for punctuation in punctuations:
        content = (' '.join(content.split(punctuation))).replace('  ', ' ')
        clean_word = [word.lower()
                      for word in content.split(' ') if len(word) > 2]
    #print(clean_word)
    return clean_word


def get_word(email_file):
    word_list = []
    word_set = []
    email_paths = fileWalker(email_file)
    for email_path in email_paths:
        clean_word = email_parser(email_path)
        word_list.append(clean_word)
        word_set.extend(clean_word)
    return word_list, set(word_set)


def count_word_prob(email_list, union_set):
    word_prob = {}
    for word in union_set:
        counter = 0
        for email in email_list:
            if word in email:
                counter += 1
            else:
                continue
        prob = 0.0
        if counter != 0:
            prob = counter/len(email_list)
        else:
            prob = 0.01
        word_prob[word] = prob
    #print(word_prob)
    return word_prob


def filter(ham_word_pro, spam_word_pro, test_file):
    test_paths = fileWalker(test_file)
    for test_path in test_paths:
        email_spam_prob = 0.0
        spam_prob = 0.5#垃圾邮件概率
        ham_prob = 0.5#正常邮件概率
        file_name = test_path.split('\\')[-1]
        prob_dict = {}
        words = set(email_parser(test_path))
        for word in words:
            Psw = 0.0
            if word not in spam_word_pro:
                Psw = 0.4
            else:
                Pws = spam_word_pro[word]
                Pwh = ham_word_pro[word]
                Psw = spam_prob*(Pws/(Pwh*ham_prob+Pws*spam_prob))
            prob_dict[word] = Psw
        #print(prob_dict)
        numerator = 1
        denominator_h = 1
        for k, v in prob_dict.items():
            numerator *= v
            denominator_h *= (1-v)
        #print(numerator,denominator_h)
        email_spam_prob = numerator/(numerator+denominator_h)#联合概率
        #print(email_spam_prob)
        if email_spam_prob > 0.9:
            print(file_name, 'spam', email_spam_prob)
        else:
            print(file_name, 'ham', email_spam_prob)
        #print(prob_dict)
        #print('******************************************************')
        # break

def main():
    ham_file = r'.\email\ham'
    spam_file = r'.\email\spam'
    test_file = r'.\test'
    ham_list, ham_set = get_word(ham_file)#正常邮件词汇
    spam_list, spam_set = get_word(spam_file)#垃圾邮件词汇
    union_set = ham_set | spam_set#总训练样本不重复词汇集
    ham_word_pro = count_word_prob(ham_list, union_set)#词汇在正常邮件中出现的概率
    spam_word_pro = count_word_prob(spam_list, union_set)#词汇在垃圾邮件中出现的概率
    filter(ham_word_pro, spam_word_pro, test_file)

if __name__ == '__main__':
    main()
