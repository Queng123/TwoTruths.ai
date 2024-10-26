from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/check-page', methods=['POST'])
def check_page():
    return jsonify({'message': 'success'})


@app.route('/rewrite', methods=['GET'])
def rewrite():
    return jsonify({'message': 'success'})


if __name__ == '__main__':
    app.run(debug=True)
