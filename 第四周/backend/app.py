from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/get', methods=['GET'])
def handle_get():
    params = request.args.to_dict()
    return jsonify({'message': f'接收到的参数是 {params}'})

@app.route('/api/post', methods=['POST'])
def handle_post():
    body_data = request.json
    param = request.args.get('param')
    return jsonify({
        'body_param': f'body中的参数是 {body_data["body_param"]}',
        'query_param': f'param中的参数是 {param}'
    })

if __name__ == '__main__':
    app.run(port=5000)