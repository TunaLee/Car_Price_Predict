import pymssql, csv, json #datasave용

ip = 'localhost'
user = 'sa'
pw = '!mssql1234'
db = 'CAR'

#mssql준비
def MssqlConnect():
    conn = pymssql.connect(server=ip, user=user, password =pw, database =db)
    return conn

def MssqlPrepare():
    conn = MssqlConnect()
    cursor = conn.cursor()
    query = '''IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='CAR_LIST' AND xtype='U')
    CREATE TABLE CAR_LIST 
    (ID INT PRIMARY KEY,
    COMPANY NVARCHAR(20), 
    MODEL NVARCHAR(30), 
    FUEL NVARCHAR(30), 
    YEAR INT, 
    DRIVEKM INT, 
    PRICE INT)
'''
    cursor.execute(query)
    conn.commit()

    return conn

#csv파일 준비
def CSVHead():
    csvfile = open('car_model.csv', 'w', encoding='utf8', newline='')
    wrc = csv.writer(csvfile)
    wrc.writerow(["ID_NUMBER","TYPE","COMPANY", "MODEL","FUEL","YEAR", "DRIVEKM","PRICE"])
    csvfile.close() #오류 방지용.

#json파일 준비
def JSONPrepare():
    jsontext = {'LABEL':[],'DATA':[] } #json에 들어갈 텍스트를 딕셔너리 형태로 정의
    jsontext['LABEL'] = ["ID_NUMBER", "COMPANY", "MODEL", "FUEL", "YEAR", "DRIVEKM", "PRICE"]
    JSONWrite(jsontext)
    return jsontext

def ExistsCheck(cnt, conn):
    cursor = conn.cursor()
    query2 = '''SELECT ID FROM CAR_LIST WHERE ID=%s'''
    res = False
    cursor.execute(query2, cnt)
    row = cursor.fetchone()
    while row:
        res = True
        row = cursor.fetchone()
    
    return res

#한 줄 DB추가
def MssqlWrite(cnt, _company, _model, _fuel, _year, _drive_km, _price, _type, conn = MssqlConnect()):
    cursor = conn.cursor()
    query = '''INSERT CAR_LIST(ID, COMPANY, MODEL, FUEL, YEAR, DRIVEKM, PRICE)
    VALUES(%s, %s, %s, %s, %s, %s, %s)'''
    query3 = '''UPDATE CAR_LIST
    SET COMPANY=%s, MODEL=%s, FUEL=%s, YEAR=%s, DRIVEKM=%s, PRICE=%s
    WHERE ID=%s'''
    res = ExistsCheck(cnt, conn)
    if res == True: #데이터 존재하면 갱신
        cursor.execute(query3,(_company, _model, _fuel, _year, _drive_km, _price, cnt) )
        conn.commit()
    else: #데이터 존재하지 않음
        cursor.execute(query, (cnt, _company, _model, _fuel, _year, _drive_km, _price) )
        conn.commit()

#csvdata 한 줄 채우기
def CSVData(_id, _type, _company, _model, _fuel, _year, _drive_km, _price):
    csvfile = open('car_model.csv', 'a', encoding='utf8', newline='')
    wrc = csv.writer(csvfile)
    wrc.writerow([_id, _type, _company, _model, _fuel, _year, _drive_km, _price])
    csvfile.close() #오류 방지용.

#JSON 데이터 채우기
def JSONData(_id, _company, _model, _fuel, _year, _drive_km, _price, jsontext):
    with open('car_model.json', 'r', encoding='utf8') as jsonfile:
        jsondata = json.load(jsonfile)
    if jsondata == jsontext: #오류 검사를 위해 체크
        jsontext['DATA'].append({"ID_NUMBER":_id, "COMPANY":_company, "MODEL":_model,\
        "FUEL":_fuel, "YEAR":_year, "DRIVEKM":_drive_km, "PRICE":_price}) #json 데이터 추가
        JSONWrite(jsontext)
    return jsontext

#JSON 파일 전송
def JSONWrite(jsontext):
    with open('car_model.json', 'w') as jsonfile:
        json.dump(jsontext,jsonfile)

def JSONWrite_FIN(jsontext):
    with open('car_model_utf8.json', 'w') as jsonfile2:
        json.dump(jsontext, jsonfile2, ensure_ascii=False)

