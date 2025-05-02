from flask import Flask, jsonify
from flask_cors import CORS
import random
import json
from chart_routes import chart_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 注册蓝图
app.register_blueprint(chart_bp)

if __name__ == '__main__':
    app.run(debug=True)