from flask import Flask
from flask import request, abort
from statistics import StatisticsManager

app = Flask(__name__)
app.threaded = True

statistic_manager = StatisticsManager()
statistic_manager.start_compute_statistic()


@app.route('/statistics/', methods=['GET'])
def get_statistics():
    statistic = statistic_manager.get_statistic()
    if statistic is None:
        abort(404)

    return statistic, 200


@app.route('/sales/', methods=['POST'])
def post_payment():
    try:
        payment = request.get_json(force=True)
        sales_amount = payment.pop("sales_amount")
        sales_amount_float = float(sales_amount)
        if sales_amount_float < 0:
            raise ValueError
        statistic_manager.add_statistic(sales_amount_float)
        return "", 202
    except Exception:
        exception400 = {'validation_error': sales_amount}
        return exception400, 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    app.run(debug=True)
