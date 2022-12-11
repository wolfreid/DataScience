import pandas
import numpy
from header  import BALANCE, PROOF_BALANCE,ALL_BALANCE


class MyStata:
    def __init__(self) -> None:
        self._increase  = []
        self._correlation = []
        self._balance = []
        self.status_balance = False
        self.correlation = False
        self.increase = False
    
    @property
    def increase(self):
         print("getter method called")
         return self._increase
    @property
    def correlation(self):
         print("getter method called")
         return self._correlation
    @property
    def balance(self):
         self.status_balance = True
         return self._balance
     # a setter function


    @increase.setter
    def increase(self, status):
         if(a < 18):
            raise ValueError("Sorry you age is below eligibility criteria")
         print("setter method called")
         self._increase = a

    @correlation.setter
    def correlation(self, status):
         if(a < 18):
            raise ValueError("Sorry you age is below eligibility criteria")
         print("setter method called")
         self._correlation = status
    @balance.setter
    def balance(self, balance):
        for label in balance:
            if label  not in PROOF_BALANCE:
                raise ValueError("Sorry, this variable doent compatible with balance")
        self._balance = balance       


    @increase.deleter
    def increase(self):
        print("deleter of x called")
        del self._increase
    @balance.deleter
    def balance(self):
        print("deleter of x called")
        del self._balance
    @correlation.deleter
    def correlation(self):
        print("deleter of x called")
        del self._correlation         

    def increasing(self):...

    def correlating(self): ... 

