""" Account Controller
    Has all function and api routes related to accounts
"""
from flask import Blueprint, jsonify, request

from models import account as MODEL

ACCOUNT_V1 = Blueprint("account_v1", __name__)


@ACCOUNT_V1.route("/v1/account/", methods=["GET"])
def get_accounts():
    """ Get All Accounts
    """
    accounts = MODEL.get_accounts()
    return jsonify(accounts)

@ACCOUNT_V1.route("/v1/account/", methods=["POST"])
def add_account():
    """ Create New Accounts
    """
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None:
        result, error = MODEL.add_account(request.json)
        if result is not None:
            return jsonify(result)
    return jsonify(error), 400

@ACCOUNT_V1.route("/v1/account/total-balance/", methods=["GET"])
def get_total_balance():
    """ Get Total balance
    """
    return jsonify({'sum':MODEL.get_total_balance()})

@ACCOUNT_V1.route("/v1/account/total/", methods=["GET"])
def get_total_accounts():
    """ Get count of counts
    """
    return jsonify({'count':len(MODEL.get_accounts())})

@ACCOUNT_V1.route("/v1/account/taxation/", methods=["POST"])
def deduce_taxation():
    """ Taxation route for the accounts
    """
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None:
        result, error = MODEL.taxation(request.json)
        if result is not None:
            return jsonify(result)
    return jsonify(error), 400

@ACCOUNT_V1.route("/v1/account/authenticate/", methods=["POST"])
def authenticate():
    """ Authenticate the account
    """
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None and request.json.get('idx') and request.json.get('password'):
        result, error = MODEL.authenticator(request.json.get('idx'), request.json.get('password'))
        if result is not None:
            return jsonify(result)
    else:
        return jsonify(error), 400  

@ACCOUNT_V1.route("/v1/account/withdraw/", methods=["POST"])
def withdraw():
    """ Make withdrawal
    """
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None and request.json.get('idx') and request.json.get('password') and request.json.get('amount'):
        result, error = MODEL.withdraw(request.json.get('idx'), request.json.get('password'), request.json.get('amount'))
        if result is not None:
            return jsonify(result)
    return jsonify(error), 400  

@ACCOUNT_V1.route("/v1/account/lowest/", methods=["GET"])
def lowest_account():
    """ Get lowest balance Accounts
    """
    error = 'Bad Request'
    result, error = MODEL.lowest_account()
    if result is not None:
        if not result:
            return jsonify([])
        return jsonify(result)
    else:
        return jsonify(error), 400

@ACCOUNT_V1.route("/v1/account/highest/", methods=["GET"])
def highest_account():
    """ Get highest Accounts balances
    """
    error = 'Bad Request'
    result, error = MODEL.highest_account()
    if result is not None:
        return jsonify(result)
    else:
        return jsonify(error), 400

@ACCOUNT_V1.route("/v1/account/filter/", methods=["POST"])
def filter_account():
    """ Filter Accounts and get the accounts below the supplied value
    """
    error = 'Bad Request'
    if hasattr(request, "json") and request.json is not None and request.json.get('amount') and (isinstance(request.json.get('amount'), int) or isinstance(request.json.get('amount'), float)):
        return jsonify(MODEL.filter_account(request.json.get('amount')))
    return jsonify(error), 400
