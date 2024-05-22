import sys
sys.path.insert(0, '/home/utilisateur/Documents/dev_ia/bank/source')

from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
import datetime
from setup_db import session
from bank import Account, Transaction
from conftest import account_factory


class TestTransaction(object):
    def setup_method(self, method):
        self.session = UnifiedAlchemyMagicMock() #permet de simuler une session SQLAlchemy pour les tests.
 
#1. Tests pour les Dépôts (Deposit)

    def test_deposit_normal(self):
        '''La fonction create_autospec est une fonction de la bibliothèque unittest.mock de Python. 
        Elle est utilisée pour créer un objet "mock" (ou "faux") qui imite le comportement d'un autre objet.
        instance=True indique que le mock créé doit avoir le même comportement qu'une instance de la classe spécifiée,'''

        account = create_autospec(Account, instance=True)
        
        account.balance = 100

        transaction = Transaction(account)
        transaction.deposit(50)

        #vérification que le solde a été mis à jour
        assert account.balance == 150
        #vérification que le type de transaction est 'deposit'
        assert transaction.type == 'deposit'
        #vérification que le timestamp est correct
        assert transaction.timestamp == datetime.datetime.now().date()
         # vérification que session.commit() n'a été appelé
        self.session.commit.assert_not_called()

    def test_deposit_negative_amount(self):
        account1 = create_autospec(Account, instance=True)
        
        account1.balance = 100

        transaction1 = Transaction(account1)
        transaction1.deposit(-50)

        #vérification que le solde n'a pas été mis à jour
        assert account1.balance == 100
        #verif que depostif n'est pas crée
        assert transaction1.type != 'deposit'
        # vérification que session.commit() n'a été appelé
        self.session.commit.assert_not_called()

    def test_deposit_zero_amount(self, account_factory):
        account = account_factory(100)

        transaction = Transaction(account)
        transaction.deposit(0)

        #vérification que le solde n'a pas été mis à jour
        assert account.balance == 100
        #verif que depostif n'est pas crée
        assert transaction.type != 'deposit'
        # vérification que session.commit() n'a été appelé
        self.session.commit.assert_not_called()



#2. Tests pour les Retraits (Withdraw)

    def test_withdraw_normal(self):
        account = create_autospec(Account, instance=True)
        
        account.balance = 100

        transaction = Transaction(account)
        transaction.withdraw(50)
# vérification que le solde a été mis à jour
        assert account.balance == 50
# vérification que le type de transaction est 'withdraw'
        assert transaction.type == 'withdraw'
# vérification que session.commit() n'a été appelé
        self.session.commit.assert_not_called()


    def test_withdraw_insufficient_funds(self):
        account = create_autospec(Account, instance=True)
        
        account.balance = 100

        transaction = Transaction(account)
        transaction.withdraw(150)

        # vérification que le solde n'a pas été mis à jour
        assert account.balance == 100
        # vérification que le type de transaction n'est pas 'withdraw'
        assert transaction.type != 'withdraw'
        # vérification que session.commit() n'a pas été appelé
        self.session.commit.assert_not_called()

    def test_withdraw_negative_amount(self):
        account = create_autospec(Account, instance=True)
        
        account.balance = 100

        transaction = Transaction(account)
        transaction.withdraw(-100)

        # vérification que le solde n'a pas été mis à jour
        assert account.balance == 100
        # vérification que le type de transaction n'est pas 'withdraw'
        assert transaction.type != 'withdraw'
        # vérification que session.commit() n'a pas été appelé
        self.session.commit.assert_not_called()

#3. Tests pour les Transferts (Transfer)

    def test_transfer_normal(self):
        # Créez deux comptes avec un solde initial
        from_account = create_autospec(Account, instance=True)
        from_account.balance = 100
        to_account = create_autospec(Account, instance=True)
        to_account.balance = 50

        # Créez une transaction
        transaction = Transaction(from_account)

        # Effectuez un transfert d'un montant de 50
        transaction.transfer(from_account, to_account, 50)

        # Vérifiez que les soldes des comptes ont été mis à jour correctement
        assert from_account.balance == 50
        assert to_account.balance == 100

        # Vérifiez que le type de transaction est correct pour chaque compte
        assert transaction.type == 'transfer'

    def test_transfer_insufficient_funds(self):
        from_account = create_autospec(Account, instance=True)
        from_account.balance = 100
        to_account = create_autospec(Account, instance=True)
        to_account.balance = 50

        transaction = Transaction(from_account)
        transaction.transfer(to_account, from_account, 150)

        # vérification que les soldes n'ont pas été mis à jour
        assert from_account.balance == 100
        assert to_account.balance == 50
        # vérification que le type de transaction n'est pas 'transfer'
        assert transaction.type != 'transfer'
        # vérification que session.commit() n'a pas été appelé
        self.session.commit.assert_not_called()


    def test_transfer_negative_amount(self):
        from_account = create_autospec(Account, instance=True)
        from_account.balance = 100
        to_account = create_autospec(Account, instance=True)
        to_account.balance = 50

        transaction = Transaction(from_account)
        transaction.transfer(to_account, from_account, -150)

        # vérification que les soldes n'ont pas été mis à jour
        assert from_account.balance == 100
        assert to_account.balance == 50
        # vérification que le type de transaction n'est pas 'transfer'
        assert transaction.type != 'transfer'
        # vérification que session.commit() n'a pas été appelé
        self.session.commit.assert_not_called()

    def test_transfer_zero_amount(self):
        from_account = create_autospec(Account, instance=True)
        from_account.balance = 100
        to_account = create_autospec(Account, instance=True)
        to_account.balance = 50

        transaction = Transaction(from_account)
        transaction.transfer(to_account, from_account, 0)

        # vérification que les soldes n'ont pas été mis à jour
        assert from_account.balance == 100
        assert to_account.balance == 50
        # vérification que le type de transaction n'est pas 'transfer'
        assert transaction.type != 'transfer'
        # vérification que session.commit() n'a pas été appelé
        self.session.commit.assert_not_called()

#Tests pour la consultation de solde (get_balance)

class TestAccount(object):
    #connexion à la base de données
    def setup_method(self, method):
        self.session = UnifiedAlchemyMagicMock()

    #test pour la consultation de solde
    def test_get_balance_initial(self):
        account = Account(100)
        balance = account.get_balance()
        assert balance == 100
        #test que session.commit() n'a pas été appelé
        self.session.commit.assert_not_called()

    #test pour la consultation de solde après un dépôt
    def test_get_balance_after_deposit(self):
        account = Account(100)
        transaction = Transaction(account)
        transaction.deposit(50)
        balance = account.get_balance()
        assert balance == 150


    #test pour la consultation de solde après un retrait
    def test_get_balance_after_withdraw(self):
        account = Account(100)
        transaction = Transaction(account)
        transaction.withdraw(50)
        balance = account.get_balance()
        assert balance == 50

    #test pour la consultation de solde après un retrait pour solde insuffisant
    def test_get_balance_after_failed_withdraw(self):
        account = Account(100)
        transaction = Transaction(account)
        transaction.withdraw(150)
        balance = account.get_balance()
        assert balance == 100 

    #test pour la consultation de solde après un transfert  
    def test_get_balance_after_transfer(self):
        from_account = Account(100)
        to_account = Account(50)
        transaction = Transaction(from_account)
        transaction.transfer(from_account, to_account, 50)
        balance_from_account = from_account.get_balance()
        balance_to_account = to_account.get_balance()
        assert balance_from_account == 50
        assert balance_to_account == 100
        
    



    # def test_transfer(self, account_factory):
    #     # crée des comptes 
    #     account1 = account_factory(100)
    #     account2 = account_factory(50)

    #     # crée une transaction mock
    #     transaction = Transaction(account1)

    #     # transfère de l'argent
    #     transaction.transfer(account2, 50)

        #  vérifie que les soldes ont été mis à jour
        # assert account1.balance == 50
        # assert account2.balance == 100

    

    



    