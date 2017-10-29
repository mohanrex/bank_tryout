"""Account Model
    Handles all data related function for the accounts data
"""

import hashlib

from datetime import datetime

from components.TinyDBEngine import ACCOUNTS_DB

def get_accounts():
    """ Get all accounts
        Returns:
        ---------
            Returns a list of accounts present in the system
    """
    return ACCOUNTS_DB.get_records()

def add_account(data):
    """ Create a new account
        Parameters:
        -----------
            data : {'name':'','secret':0,'balance':0}
        Returns:
        ---------
            Returns a list of accounts present in the system
    """
    if validate(data):
        idx = str(int(datetime.now().timestamp())) + data.get('name')
        data['secret'] = hasher(str(data['secret']))
        ACCOUNTS_DB.add_record(idx, data)
        return ACCOUNTS_DB.get_record_by_id(idx), None
    else:
        return False, 'Validation Error'

def get_total_balance():
    """ Get total balance
        Returns:
        ---------
            Returns total balance of all accounts
    """
    return sum(record['values']['balance'] for record in get_accounts())

def taxation(data):
    """ Reduce all accounts balance with the tax percentage given
        Parameters:
        -----------
            data : {'percentile':0}
        Returns:
        ---------
            Returns list of all accounts
    """
    if (
            data.get('percentile') and
            (
                isinstance(data.get('percentile'), float) or
                isinstance(data.get('percentile'), int)
            ) and
            data.get('percentile') <= 100 and
            data.get('percentile') >= 0
        ):
        for record in get_accounts():
            record['values']['balance'] = float(
                str(
                    round(
                        record['values']['balance'] -
                        record['values']['balance'] *
                        data.get('percentile') / 100, 2
                    )
                )
            )
            ACCOUNTS_DB.update_record(record['idx'], record)
        return get_accounts(), None
    return False, 'Validation Error'

def authenticator(idx, password):
    """ Authenticate the account based on the id and password
        Parameters:
        -----------
            idx: account id,
            password: account secret
        Returns:
        --------
            Boolean
    """
    record = ACCOUNTS_DB.get_record_by_id(idx)
    if record:
        if record['values']['secret'] == hasher(str(password)):
            return True
    return False

def withdraw(idx, password, amount):
    """ Withdraw the balance from the account
        Parameters:
        -----------
            idx: account id,
            password: account secret
            amount: amount to be withdraw
        Returns:
        --------
            Boolean
    """
    if (
            authenticator(idx, password) and
            (
                isinstance(amount, int) or
                isinstance(amount, float)
            ) and
            amount > 0
        ):
        record = ACCOUNTS_DB.get_record_by_id(idx)
        if record['values']['balance'] >= amount:
            record['values']['balance'] = record['values']['balance'] - amount
            ACCOUNTS_DB.update_record(record['idx'], record)
            return True, None
        return False, "Insufficient Amount"
    return False, "Invalid Password or name"

def filter_account(amount):
    """ Filter the account based on the amount
        Parameters:
        -----------
            amount: filter value
        Returns:
        --------
            list of account which is below the filter value
    """
    return list([record for record in get_accounts() if record['values']['balance'] <= amount])

def lowest_account():
    """ Get the list of lowest account balance
        Returns:
        -----------
            list of account which has lowest balance
    """
    accounts = get_accounts()
    if len(accounts) > 0:
        # get lowest balance
        lowest = min(accounts, key=lambda account: account['values']['balance'])
        # Returns list of accounts with the matching lowest balance
        return [
            account['values']
            for account in accounts
            if account['values']['balance'] == lowest['values']['balance']
        ], None
    return False, "Validation Error"

def highest_account():
    """ Get the list of highest account balance
        Returns:
        -----------
            list of account which has highest balance
    """
    accounts = get_accounts()
    if len(accounts) > 0:
        # Get the highest balance
        highest = max(accounts, key=lambda account: account['values']['balance'])
        # Returns list of accounts with the matching highest balance
        return [
            account['values']
            for account in accounts
            if account['values']['balance'] == highest['values']['balance']
        ], None
    return False, "Validation Error"

def validate(data):
    """ Validate the input data for account creation
        Parameters:
        ----------
            data:{'name':'', 'secret':0, 'balance':0}
        Returns:
        -----------
            Boolean
    """
    must_keys = ['name', 'secret', 'balance']
    return (
        len(data) == len(must_keys) and
        all(key in data for key in must_keys) and
        len(data.get('name')) > 1 and
        len(str(data.get('secret'))) == 4 and
        isinstance(data.get('secret'), int) and
        (isinstance(data.get('balance'), int) or isinstance(data.get('balance'), float))
    )

def hasher(value):
    """ Provides the hashed value of the given value
        Parameters:
        ----------
            value: value that needs to be hashed
        Returns:
        -----------
            Returns the hashed string
    """
    # MD5 hashing to securely store the password. Password should not be stored in plain text
    return hashlib.md5(value.encode('utf_8') + b"Trukish").hexdigest()
