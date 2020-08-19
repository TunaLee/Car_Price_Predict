from flask import Flask, render_template, request, url_for
import run

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return '''<h1>중고차 값 측정</h1>
    <a href="/price"> 중고차 값 모듈 시뮬레이터</a>'''

@app.route('/price')
def price(model=None):
    _model = None
    return render_template('module.html', model=None )
    

@app.route('/calculator', methods=['GET', 'POST'])
def calculator(model=None, year ='2020',value_min='0', value_avg='100000', value_max='200000' ):
    if request.method == 'GET':
        _type = request.args.get('type')
        _model = request.args.get('model')
        _dr = request.args.get('drivenkm')
        _ye = request.args.get('year')
        _fu = request.args.get('fuel')
        f= open('testset.csv', 'w', encoding='utf8')
        string = 'TYPE,MODEL,FUEL,YEAR,DRIVEKM\n'
        string += _type+','+_model+','+_fu+','+_ye+','+_dr #결과 적기
        print(string)
        f.write(string)
        f.close()
        # Process 적어주세요. 결과값은 _val_list = [최소, 중간, 최대] 형태로 처리해주세요.
        #오류 방지를 위해 evaluate로 대체
        _val = run.Predict_result()
        
        return render_template('module.html', model=_model, year=str(_ye), value_avg= str(_val))

if __name__ == '__main__':
    app.run()