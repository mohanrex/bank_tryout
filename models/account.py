
import hashlib

from datetime import datetime

from components.TinyDBEngine import ACCOUNTS_DB

def get_accounts():
    return ACCOUNTS_DB.get_records()

def add_account(data):
    if validate(data):
        idx = str(int(datetime.now().timestamp())) + data.get('name')
        data['secret'] = hasher(str(data['secret']))
        ACCOUNTS_DB.add_record(idx, data)
        return ACCOUNTS_DB.get_record_by_id(idx), None
    else:
        return False, 'Validation Error'

def update_account(data, idx):
    if update_validator(data):
        record = ACCOUNTS_DB.get_record_by_id(idx)
        if record:
            record['values']['balance'] = data.get('balance')
            ACCOUNTS_DB.update_record(idx, record)
            return ACCOUNTS_DB.get_record_by_id(idx), None
    return False, 'Validation Error'

def get_total_balance():
    return sum(record['values']['balance'] for record in get_accounts())

def taxation(data):
    if (
        data.get('percentile') and
        isinstance(data.get('percentile'), float) and
        data.get('percentile') <= 100 and
        data.get('percentile') >= 0
    ):
        for record in get_accounts():
            record['values']['balance'] = float(str(round(record['values']['balance'] - record['values']['balance'] * data.get('percentile') / 100, 2)))
            ACCOUNTS_DB.update_record(record['idx'], record)
        return get_accounts(), None
    return False, 'Validation Error'

def authenticator(idx, password):
    record = ACCOUNTS_DB.get_record_by_id(idx)
    if record:
        if record['values']['secret'] == hasher(str(password)):
            return True
    return False

def withdraw(idx, password, amount):
    if authenticator(idx, password) and isinstance(amount, float) and amount > 0:
        record = ACCOUNTS_DB.get_record_by_id(idx)
        if record['values']['balance'] > amount:
            record['values']['balance'] = record['values']['balance'] - amount
            ACCOUNTS_DB.update_record(record['idx'], record)
            return True, None
        return False, "Insufficient Amount"
    return False, "Invalid Password or name"

def filter_account(amount):
    if isinstance(amount, float):
        return list([record for record in get_accounts() if record['values']['balance'] < amount]), None
    return False, "Validation Error"

def lowest_account():
    accounts = get_accounts()
    if len(accounts) > 0:
        lowest = min(accounts, key=lambda accounts:accounts['values']['balances'])
        return list([account for account in accounts if account['values']['balances'] == lowest['values']['balances']])
    return False, "Validation Error"

def update_validator(data):
    must_keys = ['balance']
    return (
        len(data) == len(must_keys) and
        all(key in data for key in must_keys) and
        isinstance(data.get('balance'), float)
    )

def validate(data):
    must_keys = ['name', 'secret', 'balance']
    return (
        len(data) == len(must_keys) and
        all(key in data for key in must_keys) and
        len(data.get('name')) > 1 and
        len(str(data.get('secret'))) == 4 and
        isinstance(data.get('secret'), int) and
        isinstance(data.get('balance'), float)
    )

def hasher(value):
    return hashlib.md5(value.encode('utf_8') + b"Trukish").hexdigest()