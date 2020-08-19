from flask import Flask, render_template, request, url_for

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return '''<h1>중고차 값 측정</h1>
    <a href="/price">중고차 값 모듈 시뮬레이터</a>'''

@app.route('/price')
def price(model=None):
    _model = None
    return render_template('module.html', model=_model )

@app.route('/calculator', methods=['GET', 'POST'])
def calculator(model=None, year ='2020',value_min='0', value_avg='100000', value_max='200000' ):
    if request.method == 'GET':
        _model = request.args.get('model')
        _dr = request.args.get('drivenkm')
        _ye = request.args.get('year')
        _val_list = evaluate(_model,_dr, _ye) # 배열로 출력

        return render_template('module.html',model=_model, year=str(_ye),value_min = str(_val_list[0]), value_avg= str(_val_list[1]), value_max = str(_val_list[2]) )

def evaluate(_model, _dr, _ye):
    _val_list = [0,100000,200000] #초기값 설정
        
    return _val_list

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)