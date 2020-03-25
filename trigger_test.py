# import sps

from flask import Flask, current_app, request

app = Flask(__name__)
with app.test_request_context('/anlage_const_req'):
    sps.anlage_const_req()
    print sps.anlage_const_req()