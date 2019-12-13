from flask import Flask, request, jsonify

from src.api.rating_report import get_report

app = Flask(__name__)


@app.route('/report')
def generate_report():
    user_id = request.args.get('id')
    report = get_report(user_id)
    return jsonify(report)
