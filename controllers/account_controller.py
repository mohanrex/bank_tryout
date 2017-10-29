from flask import Blueprint, jsonify, request

from models import account as MODEL

ACCOUNT_V1 = Blueprint("account_v1", __name__)


@ACCOUNT_V1.route("/v1/account/", methods=["GET"])
def get_accounts():
    """ Get All Accounts
    """
    return jsonify(MODEL.get_accounts())

@ACCOUNT_V1.route("/v1/account/", methods=["POST"])
def add_account():
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None:
        result, error = MODEL.add_account(request.json)
        if result:
            return jsonify(result)
    return jsonify(error), 400    

@ACCOUNT_V1.route("/v1/account/<string:idx>/", methods=["PUT"])
def update_account(idx):
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None:
        result, error = MODEL.update_account(request.json, idx)
        if result:
            return jsonify(result)
    else:
        return jsonify(error), 400    

@ACCOUNT_V1.route("/v1/account/total-balance/", methods=["GET"])
def get_total_balance():
    return jsonify({'sum':MODEL.get_total_balance()})

@ACCOUNT_V1.route("/v1/account/total/", methods=["GET"])
def get_total_accounts():
    return jsonify({'count':len(MODEL.get_accounts())})

@ACCOUNT_V1.route("/v1/account/taxation/", methods=["POST"])
def deduce_taxation():
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None:
        result, error = MODEL.taxation(request.json)
        if result:
            return jsonify(result)
    return jsonify(error), 400  

@ACCOUNT_V1.route("/v1/account/authenticate/", methods=["POST"])
def authenticate():
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None and request.json.get('idx') and request.json.get('password'):
        result, error = MODEL.authenticator(request.json.get('idx'), request.json.get('password'))
        if result:
            return jsonify(result)
    else:
        return jsonify(error), 400  

@ACCOUNT_V1.route("/v1/account/withdraw/", methods=["POST"])
def withdraw():
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None and request.json.get('idx') and request.json.get('password') and request.json.get('amount'):
        result, error = MODEL.withdraw(request.json.get('idx'), request.json.get('password'), request.json.get('amount'))
        if result:
            return jsonify(result)
    return jsonify(error), 400  

@ACCOUNT_V1.route("/v1/account/lowest/", methods=["GET"])
def lowest_account():
    error = 'Bad Request'
    result, error = MODEL.lowest_account()
    if result:
        return jsonify(result)
    else:
        return jsonify(error), 400

@ACCOUNT_V1.route("/v1/account/highest/", methods=["GET"])
def highest_account():
    error = 'Bad Request'
    result, error = MODEL.highest_account()
    if result:
        return jsonify(result)
    else:
        return jsonify(error), 400

@ACCOUNT_V1.route("/v1/account/filter/", methods=["POST"])
def filter_account():
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None and request.json.get('amount') and (isinstance(request.json.get('amount'), int) or isinstance(request.json.get('amount'), float)):
        return jsonify(MODEL.filter_account(request.json.get('amount')))
    return jsonify(error), 400
