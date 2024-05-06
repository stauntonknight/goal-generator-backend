from flask import Flask, json, request
from flask_cors import CORS, cross_origin
import grant_wishes

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/generatewish', methods = ['GET'])
@cross_origin()
def generate_wish():
    return grant_wishes.getwish(request.args.get('wish'))

app.run()
