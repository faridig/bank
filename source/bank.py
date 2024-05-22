from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.orm import declarative_base



Base = declarative_base()

class Account(Base):
    #nom de la table:
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True)
    balance = Column(Float, index=True)
    transactions = relationship("Transaction", back_populates="account") #relation avc la classe Transaction

    def __init__(self, balance):
        self.balance = balance

    def get_balance(self):
        return self.balance

class Transaction(Base):
    #nom de la table:
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.account_id')) #clé étrangère pour lier la table transactions à la table account
    montant = Column(Float)
    type = Column(String) #peu contenir deposit, withdraw ou transfer
    timestamp = Column(DateTime)
    account = relationship("Account") #Ceci définit une relation avec la classe Account. Cela signifie qu'une transaction est associée à un compte. SQLAlchemy utilise cette relation pour gérer les opérations entre les deux tables.

    def __init__(self, account):
        self.account = account

    def deposit(self, amount):
        if amount <= 0:
            return
        self.account.balance+=amount
        self.timestamp = datetime.datetime.now().date()
        self.type = 'deposit'

    def withdraw(self, amount):
        if amount > self.account.balance or amount <= 0:
            return
        self.account.balance-=amount
        self.type = 'withdraw'

    def transfer(self, from_account, to_account, amount):
        if amount > from_account.balance or amount <= 0:
            return
        from_account.balance -= amount
        self.account = from_account
        self.type = 'transfer'
        self.timestamp = datetime.datetime.now().date()

        to_account.balance += amount
        to_transfer = Transaction(to_account)
        to_transfer.type = 'transfer'
        to_transfer.timestamp = datetime.datetime.now().date()


