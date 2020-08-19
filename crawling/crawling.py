from selenium import webdriver
import time, os, json 
import datasave #csv 파일, json 파일로 저장하기
from model_car import Car, car_text, price_text, fuel_text


url_text = 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor&searchType=model&wtClick_kor=003&TG.R=A#!%7B%22action%22%3A%22(And.Hidden.N._.CarType.Y._.Category.{}.)%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A{}%2C%22limit%22%3A20%7D'
url_text_2 = 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor&searchType=model&TG.R=A#!%7B%22action%22%3A%22(And.Hidden.N._.CarType.Y._.Category.{}.)%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A{}%2C%22limit%22%3A100%7D'
driver = webdriver.Chrome('../chromedriver.exe')

# conn = datasave.MssqlConnect()
# datasave.MssqlPrepare()
# cursor = conn.cursor()
datasave.CSVHead()
# jsontext = datasave.JSONPrepare()
''' #임시로 비활성화
if os.path.isfile('car_model.csv') == False:
    datasave.CSVHead()
if os.path.isfile('car_model.json') == False:
    jsontext = datasave.JSONPrepare()
else:
    with open('car_model.json', 'r', encoding='utf8') as jsonfile:
        jsontext = json.load(jsonfile)
'''
txt ='경차'
driver.get(url_text_2.format(txt,1))
try:
    driver.find_element_by_xpath('//*[@id="rySch_car"]/div[2]/fieldset/div[1]/h5/a').click()
except:
    pass
time.sleep(0.1)
car_type_list = ['경차', '소형차', '준중형차', '중형차', '대형차', '스포츠카', 'SUV', 'RV', '경승합차', '승합차', '화물차']
car_type_link_list = driver.find_elements_by_xpath('//*[@id="schCategory"]/div/ul/li')
car_type_count_list = []

for num in range(len(car_type_list)):
    car_type_link = car_type_link_list[num]
    car_type_count = car_type_link.find_element_by_xpath('.//em').text
    car_type_count_1 = int(car_type_count.replace(',',''))
    car_type_count_list.append(car_type_count_1)

car_list = []
# cnt = 1

for num in range(len(car_type_list)):
    _type = car_type_list[num]
    page_cnt = (car_type_count_list[num]-1)//100 +1
    for i in range(1,page_cnt+1): #1만개 데이터 가져오기
        driver.get(url_text_2.format(_type, i)) #웹사이트 포맷 가져오기
        try:
            driver.find_element_by_xpath('//*[@id="rySch_car"]/div[2]/fieldset/div[1]/h5/a').click()
        except:
            pass
        time.sleep(1)
        crawl_list = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]/div[3]/div[1]/div[3]/div[3]/table/tbody/tr') #자동차 리스트 xpath 가져오기
        print('자동차 목록 : ',len(car_list))
        for cars in crawl_list:
            _car_a = cars.find_element_by_xpath('.//td[2]/a')
            _a_href = _car_a.get_attribute('href')
            _ampsplit = _a_href.split('&')[2]
            _id = int(_ampsplit.split('=')[1])
            _company = _car_a.find_element_by_xpath('.//span[1]/strong').text
            _model = _car_a.find_element_by_xpath('.//span[1]/em').text
            # _model = car_text(_model_1) #모델명 규격화
            _year_txt = cars.find_element_by_xpath('.//td[2]/span[1]/span[1]').text
            if int(_year_txt[0:2])<=25: _year = int(_year_txt[0:2])+2000  
            else: _year = int(_year_txt[0:2])+1900  #연도 정보만 추출
            _fuel_txt = cars.find_element_by_xpath('.//td[2]/span[1]/span[3]').text
            #_fuel =  fuel_text(_fuel_txt)
            _fuel = _fuel_txt
            _drive_km_txt = cars.find_element_by_xpath('.//td[2]/span[1]/span[2]').text
            _drive_km = int(_drive_km_txt.replace('km','').replace(',','')) #주행거리
            _price_txt = cars.find_element_by_xpath('.//td[3]').text
            _price = price_text(_price_txt, _model) #가격명 규격화
            if _model !='' and _price != 0: #예외처리가 아닐 때
                new_car = Car(_id, _type, _company, _model, _fuel, _year, _drive_km, _price)
                car_list.append(new_car)

                # datasave.MssqlWrite(_id, _company, _model, _fuel, _year, _drive_km, _price, conn)
                datasave.CSVData(_id,_type, _company, _model, _fuel, _year, _drive_km, _price)
                # jsontext = datasave.JSONData(_id, _company, _model, _fuel, _year, _drive_km, _price, jsontext)
                # cnt +=1 #카운트 추가
                # print(new_car.model, end= ' ')
            
            time.sleep(0.1)
        print('\n페이지 '+str(i)+' 가져오기 완료!, 총 데이터: '+str(len(car_list))+'개')


print('총 데이터 수 :', len(car_list))
# datasave.JSONWrite_FIN(jsontext)


    