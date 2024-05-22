import pytest 
import sys
sys.path.insert(0, '/home/utilisateur/Documents/dev_ia/bank/source')


from bank import Account, Transaction


@pytest.fixture
def account_factory():
    def create_account(balance):
        account = Account(balance)
        return account
    return create_account

       