import pandas as pd

class Entity:
    context: str
    fname: str
    train: object
    test: object
    id: str
    lavel: str

    @property
    def context(self) -> str: return self._context

    @context.setter
    def context(self, context): self._context = context

    @property
    def fname(self) -> str: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def train(self) -> object: return self._train

    @train.setter
    def train(self, train): self._train = train

    @property
    def test(self) -> object: return self._test

    @test.setter
    def test(self, test): self._test = test

    @property
    def id(self) -> str: return self._id

    @id.setter
    def id(self, id): self._id = id

    @property
    def lavel(self) -> str: return self._lavel

    @lavel.setter
    def lavel(self, lavel): self._lavel = lavel

"""
['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
       'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
"""

"""
['PassengerId', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch',
       'Ticket', 'Fare', 'Cabin', 'Embarked']
"""
class Service:
    def __init__(self):
        self.entity = Entity()

    def new_model(self, payload):
        this = self.entity
        this.context = './data/'
        this.fname = payload
        return pd.read_csv(this.context+this.fname)

"""
PassengerId  고객ID,
Survived 생존여부,
Pclass 승선권 1 = 1등석, 2 = 2등석, 3 = 3등석,
Name,
Sex,
Age,
SibSp 동반한 형제, 자매, 배우자,
Parch 동반한 부모, 자식,
Ticket 티켓번호,
Fare 요금,
Cabin 객실번호,
Embarked 승선한 항구명 C = 쉐브루, Q = 퀸즈타운, S = 사우스햄튼
print(f’결정트리 활용한 검증 정확도 {None}‘)
print(f’랜덤포레스트 활용한 검증 정확도 {None}‘)
print(f’나이브베이즈 활용한 검증 정확도 {None}‘)
print(f’KNN 활용한 검증 정확도 {None}‘)
print(f’SVM 활용한 검증 정확도 {None}’)
"""


class Controller:
    def __init__(self):
        self.entity = Entity()
        self.service = Service()

    def modeling(self, train, test): #entity 속성과 service 기능을 합쳐서 객체(파이썬에서는 모델)을 만든다.
        service = self.service
        this = self.preprocess(train, test)
        this.label = service.create_label(this)
        this.train = service.create_train(this)
        return this

    def preprocess(self,train,test):
        service = self.service
        this = self.entity
        this.train = service.new_model(train)
        #print(f'트레인의 컬럼 : {this.train.columns}') #column을 보여준다. column은 스키마 구조고 객체지향에서는 property가 된다.
        this.test = service.new_model(test)
        print(f'테스트의 컬럼 : {this.test.columns}')
def print_menu():
    print('0.Exit\n')
    print('1.현재 처리 상태')
    return input('메뉴 선택\n')


app = Controller()
while 1:
    menu = print_menu()
    if menu == '0': break
    if menu == '1': app.preprocess('train.csv','test.csv')
