from dataclasses import dataclass
import nltk
from nltk.tokenize import word_tokenize #좀 오래된 것들
from konlpy.tag import Okt #파스칼표기법, 카멜표기법
from nltk import FreqDist

import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

@dataclass
class Entity:
    context : str
    fname : str
    target : str

    @property
    def context(self)-> str : return self._context

    @context.setter
    def context(self, context): self._context = context

    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def target(self) -> str: return self._target

    @target.setter
    def target(self, target): self._target = target


class Service:
    def __init__(self):
        self.texts = []
        self.tokens = []
        self.noun_tokens = []
        self.okt = Okt()
        self.stopwords = []
        self.freqtxt = []

    def extract_texts(self, payload):
        print('1. corpus 에서 token 추출')
        filename = payload.context + payload.fname
        with open(filename, 'r', encoding='utf-8') as f:
            self.texts = f.read()
        print(f'1단계 결과물 : {self.texts[:300]}')

    def tokenize(self):
        print('2. corpus 에서 한글 추출')
        texts = self.texts.replace('\n',' ')
        tokenizer = re.compile(r'[^ㄱ-힣]')
        # ^ 는 not 과 start 두가지 개념이 있음
        # [^] 은 not, ^[] 은 start 의미로 표현됨
        self.texts = tokenizer.sub(' ', texts)
        # 한글이 아닌 것은 ' ' 처리해서 한글과 띄어쓰기 남겨라
        print(f'2단계 결과물 : {self.texts[:300]}')


    def conversion_token(self):
        print('3. 한글 token 변환')
        self.tokens = word_tokenize(self.texts)
        print(f'3단계 결과물 : {self.tokens[:300]}')

    def compound_noun(self):
        print('4. 복합명사화 ')
        arr_ = []
        for token in self.tokens:
            token_pos = self.okt.pos(token)
            _ = [txt_tags[0] for txt_tags in token_pos
                 if txt_tags[1] == 'Noun']
            if len("".join(_)) > 1:
                arr_.append("".join(_))
        self.noun_tokens = " ".join(arr_)
        print(f'4단계 결과물 : {self.noun_tokens[:300]}')

    def extract_stopword(self,payload):
        print('5. 노이즈 코퍼스에서 토큰 추출')
        fname = payload.context + payload.fname
        with open(fname, 'r', encoding='utf-8') as f:
            self.texts = f.read()
            self.stopwords = self.stopwords.split(' ')
        print(f'1단계 결과물 : {self.texts[:10]}')

    def filtering_text_with_stopword(self):
        print('6. 노이즈 필터링 후 시그널 추출')
        self.noun_tokens = word_tokenize(self.noun_tokens)
        self.noun_tokens = [text for text in self.noun_tokens
                            if text not in self.stopwords]

    def frequent_text(self):
        print('7. 시그널 중에 사용빈도 정렬')
        self.freqtxt = pd.Series(dict(FreqDist(self.noun_tokens))).sort_values(ascending=False)
        print(f'{self.freqtxt[.10]}')

    def wordcloud(self,payload):
        print('8. 시각화')
        fname = payload.context + payload.fname
        wcloud = WordCloud(fname, relative_scaling=0.2, background_color='white')\
                .generate(" ".join(self.texts))
        plt.figure(figsize=(12,12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()


class Controller:
    def __init__(self):
        pass

    def download_dictionary(self):
        nltk.download('all')

    def data_analysis(self):
        entity = Entity()
        service = Service()
        entity.context = './data/'
        entity.fname = 'kr-Report_2018.txt'
        service.extract_texts(entity)
        service.tokenize()
        service.conversion_token()
        service.compound_noun()
        service.extract_stopword()
        service.filtering_text_with_stopword()
        service.frequent_text()
        service.wordcloud()

def print_menu():
    print('0. Exit\n')
    print('1. 사전 다운로드\n')
    return input('메뉴 선택\n')

app = Controller()
while 1:
    menu = print_menu()
    #if menu =='1':
        #app.download_dictionary()
    if menu == '0':
        break
    if menu == '2':
        app.data_analysis()

