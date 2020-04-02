import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from nltk.tokenize import word_tokenize, RegexpTokenizer

label=[]
num=[]
message=[]
def read_mails():#读取邮件类型，名称，内容
    path="D:\PycharmProject\spam filtering\ham"
    path_list=os.listdir(path)
    for filename in path_list:
        label.append('ham')
        num.append(filename)
        f=open(os.path.join(path, filename),'r')
        text = f.read().lower()  # 小写
        token = RegexpTokenizer('[a-zA-Z]+').tokenize(text)  # 过滤符号数字，分词
        message.append(token)
        f.close()
    path = "D:\PycharmProject\spam filtering\spam"
    path_list = os.listdir(path)
    for filename in path_list:
        label.append('spam')
        num.append(filename)
        f = open(os.path.join(path, filename), 'r')
        text=f.read().lower()#小写
        token=RegexpTokenizer('[a-zA-Z]+').tokenize(text)#过滤符号数字，分词
        message.append(token)
        f.close()

def make_panda_list():#将邮件读取与DataFrame形式
    read_mails()
    data = {'label':label,
        'num':num,
        'message':message}
    df=pd.DataFrame(data)
    df['label'] = df['label'].replace(['spam', 'ham'], [1, 0])#spam为垃圾邮件，标记为1
    return df

df = make_panda_list()

# CountVectorizer是一个词频统计的类，可以算出不同的单词在所给的文档中出现的频率,将训练集中单词连成句子
df['message'] = [' '.join(text) for text in df['message']]
# 创建一个CountVectorizer对象
cv = CountVectorizer()
X = cv.fit_transform(df.message)
y = df.label
#划分训练集与测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

# sklearn.naive_bayes.MultinomialNB()函数全称是先验为多项式分布的朴素贝叶斯
# 利用MultinomialNB库直接进行训练与判定
mnb = MultinomialNB()
MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
mnb.fit(X_train, y_train)
y_pred = mnb.predict(X_test)
print("准确率:", accuracy_score(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)
# 输出混淆矩阵
print('混淆矩阵:\n',cm)

#错误预测为spam中的17.txt