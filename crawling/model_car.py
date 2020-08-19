import re

class Car:
    def __init__(self, _id, _type, _company, _model, _fuel, _year, _drive_km, _price ):
        self.id = _id
        self.type = _type
        self.company = _company
        self.model = _model
        self.fuel = _fuel
        self.year = _year
        self.drive_km = _drive_km
        self.price = _price 

def car_text(_model_1):
    res = ''
    car_list = ['그랜저', '쏘나타' ]
    for mod in car_list:
        if mod in _model_1:
            res = mod
            break
    
    return res

def price_text(_price_text, _model): #모델에 따른 가격 에외처리
    res = 0
    _price_num = _price_text.replace('만원', '').replace(',','')
    if str.isnumeric(_price_num) == True:
        #res_tf = pricerange(int(_price_num), _model)
        #if res_tf == True:
        res = int(_price_num)
    
    return res


def pricerange(_price, _model):#가격범위가 합리적인지 체크
    res = True 
    model_cheap = ['베르나', '스타렉스', '아반떼', '엑센트', '코나', '클릭', '트라제 XG']
    model_mid =  ['i30, ''i40', '베뉴', '벨로스터', '쏘나타',  '테라칸', '투스카니', '투싼' ]
    model_midhigh =  ['그랜저', '맥스크루즈', '베라크루즈', '싼타페', '아슬란', '아이오닉' ]
    model_high = ['쏠라티', '에쿠스', '제네시스', '팰리세이드' ]
    if _model not in model_cheap + model_mid + model_midhigh + model_high :
        res = False
    elif _model in model_cheap and _price>2000:
        res = False
    elif _model in model_mid and _price>3000:
        res = False
    elif _model in model_midhigh and _price>4000:
        res = False
    
    return res

def fuel_text(_fuel_txt):
    res = ''
    pattern_par = r'([가-힣]+)(\s*)\((.*)\)(.*)'
    pattern_han = r'[가-힣]+' 
    if bool(re.match(pattern_par, _fuel_txt.strip()) ) == True:
        res = re.sub(pattern_par, r'\1', _fuel_txt)
    elif bool(re.match(pattern_han, _fuel_txt)) == True:
        res = _fuel_txt

    return res
    

            


    