import json
import jieba.analyse
import cntext
from wordcloud import WordCloud

def draw_wordcloud(content):
    jieba.set_dictionary('dict.txt') # 导入字典
    jieba.analyse.set_stop_words('stopwords_hit.txt') # 导入停用词

    stop_word_file = open('./stopwords_hit.txt', 'r', encoding='utf-8')
    stopword = stop_word_file.read().split("\n") # 转化为列表

    word_list = jieba.cut(content)
    data = ' '.join(word_list)
    wordcloud = WordCloud(background_color="white", max_words=100, max_font_size=80, font_path='./SanJiBangKaiJianTi-2.ttf', stopwords=stopword, scale=30)
    wordcloud.generate(data)
    wordcloud.to_file('wordCloud.jpg')
    return True

def sentiment_analysis(content):
    positive_word_file = open('./NTUSD_positive_simplified.txt', 'r', encoding='utf-8')
    positiveWord = positive_word_file.read().split("\n")
    negative_word_file = open('./NTUSD_negative_simplified.txt', 'r', encoding='utf-8')
    negativeWord = negative_word_file.read().split("\n")
    diction = {'pos': positiveWord, 'nag': negativeWord}
    sentiment = cntext.sentiment(text=content,
                diction=diction,
                lang='chinese')
    pos_num = sentiment['pos_num']
    neg_num = sentiment['nag_num']
    pos_grade = pos_num/(pos_num+neg_num)
    neg_grade = neg_num/(pos_num+neg_num)
    return json.dumps({'pos_grade':pos_grade, 'neg_grade':neg_grade})

def get_keyWords(content):
    jieba.set_dictionary('dict.txt') # 导入字典
    jieba.analyse.set_stop_words('stopwords_hit.txt') # 导入停用词

    keys = []
    weights = []
    for key, weight in jieba.analyse.textrank(content, withWeight=True):
        # print('%s %s' % (key, weight))
        keys.append(key)
        weights.append(weight)
    # print(keys)
    return json.dumps({'keys':keys, 'weight':weights})