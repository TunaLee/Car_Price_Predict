import pandas as pd
from sklearn.linear_model import LinearRegression
from tqdm.notebook import tqdm
import re

def run():
    cars = pd.read_csv('./convert_cars.csv', engine = 'python')
    testset = pd.read_csv('./testset.csv')
    car_list = pd.read_csv('./CARLIST.csv', engine = 'python')

    cars_data = cars.iloc[:,:-1]

    cars_target = cars.iloc[:,-1:]

    lr = LinearRegression()
    lr.fit(cars_data,cars_target)
    predictions = lr.predict(cars_data)


    car_type = testset.TYPE[0]
    model = testset.MODEL[0]
    fuel = testset.FUEL[0]
    year = testset.YEAR[0]
    drivekm = testset.DRIVEKM[0]


    def replace_test_name(a,b):
        testset.FUEL.replace(a,b,inplace = True)
        testset.MODEL.replace(a,b,inplace = True)
        testset.TYPE.replace(a,b,inplace = True)
    #Testset의 fueltype 숫자변환
    replace_test_name('디젤','1')
    replace_test_name('가솔린','2')
    replace_test_name('LPG(일반인 구입)','3')
    replace_test_name('가솔린+LPG','4')
    replace_test_name('전기','5')
    replace_test_name('가솔린+전기','6')
    replace_test_name('가솔린+CNG','7')
    replace_test_name('LPG+전기','8')
    replace_test_name('수소','9')

    #Testset의 cartype 변환
    replace_test_name('경차','1')
    replace_test_name('소형차','2')
    replace_test_name('준중형차','3')
    replace_test_name('중형차','4')
    replace_test_name('대형차','5')
    replace_test_name('스포츠카','6')
    replace_test_name('SUV','7')
    replace_test_name('RV','8')
    replace_test_name('경승합차','9')
    replace_test_name('승합차','10')
    replace_test_name('화물차','11')

    #testset의 model이름 숫자 변환
    for i in tqdm(range(0,len(car_list)-1)):
        if re.search(car_list.CARLIST[i],testset.MODEL[0]) != None:
            testset.MODEL[0]=str(i)

    i = lr.predict(testset)
    i = int(i)
    print('Car type :{0}  Model : {1} Fuel type : {2} Model year :{3} Mileage : {4} 의 예측가격은 {5}'.format(car_type,model,fuel,year,drivekm,i))
    return i