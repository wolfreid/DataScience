#окно с параметрами которые потом будут вложены в excel
#зацыклить запуск корреляции
PATH = r"\\ent\root\HQ\Departments\NaturalGas\Диспетчерская УК\ЦДУ\Методика прогнозування\расчет населения ПАТ\Прогнозирование\IT\RGC-lib" 
ROOT = r"\\Sho-fs02\hq\Departments\NaturalGas\Диспетчерская УК\ЦДУ\Методика прогнозування\расчет населения ПАТ\Прогнозирование\IT"
from distutils import extension
from opcode import hasconst
from ssl import OP_CIPHER_SERVER_PREFERENCE
from turtle import update
from matplotlib.pyplot import connect
import pandas as pd
import os
import pyodbc
import win32com.client 
import pathlib
import sys
import os.path
from os import name, path
import re
import inspect as insp
# from RGClib.sqlmaneger import Structure

sys.path.insert(1, PATH ) 
# import rgcsql

class Test :
    count = 0
    def __init__(self, value) :
        if self.__class__.count > 0 :
            raise Exception
        else :
            self.__class__.count += 1
            self.value = value          #for the sake of the example SINGLETONE

class Source:
    def __init__(self,lib = None,name=None,path = None ,ext = 'sql',encoding = 'utf-8'):
        self.name  = name 
        self.path = path 
        self.ext = ext
        self.encoding  = encoding
        # self.source = '

    def is_exist(self):
        return print(self.path)

    def __setattr__(self, __name: str, __value) -> None:
        if __name =='lib':
            super(Source, self).__setattr__('path', ROOT+'\\'+__value)
        if __name  == 'path': 
            if not hasattr(self,'lib'):   
                if __value is None:
                    __value = None
                else:
                    __value = [__value] + [''] if type(__value) is str else __value + [''] 
        super(Source, self).__setattr__(__name, __value)
    def add_new_attribute(self,**attribute):
        attribute = list(attribute.items())[0]
        if not hasattr(self,attribute[0]):
            setattr(self,attribute[0],attribute[1])
    # def update_attribute():


    def args(self):
        return (self.name, self.path,self.ext)
    
    def get_info(self):
        return list(map(lambda x: x[:-1*(len(self.ext)+1)], os.listdir(self.path[0])))
    
    def count(self):
        return len(self.get_info())

    def __repr__(self) -> str:
        return self.args()
    

class SQL(Source): 
    test = None
    # блок для дочерних мета обьектов
    Network_core = "Driver"
    Network_system = "Server"
    Network_agent = "Database"
    Network_trust = "Trusted_Connection"
    Driver = "SQL Server"
    Trusted_Connection = 'yes'
    def __init_subclass__(cls,default_server,trusted,**kwargs):
        super().__init_subclass__(**kwargs)
        cls.Driver = default_server
        cls.Trusted_Connection = trusted
        
    def __init__(self, lib = None, server_name = None, DB = None,**kwargs):
    # def __init__(self, name =None, path =None, ext = None ,server_name = None, DB = None):
        super(SQL,self).__init__(**kwargs)
        self.lib = lib
        self.Server = server_name
        self.Database = DB
        self.exe_file = self.read_source()
        self.conn = self.connect_sql()
    @classmethod
    def keep_super_cont(cls):
        class_cont = cls.__dict__
        vars_cont = {}
        members= dict(insp.getmembers(cls,predicate=insp.isroutine))
        for key in class_cont.keys(): 
            if key not in members.keys() and not(key.startswith('__') and key.endswith('__')):
                vars_cont[key] = class_cont[key]               
        return vars_cont 
    
    def connect_sql(self):
        cont = self.keep_super_cont()
        cont.update(self.__dict__)
        core = '='.join([self.Network_core,'{'+cont[self.Network_core]+'}'])
        system = '='.join([self.Network_system,cont[self.Network_system]])
        agent = '='.join([self.Network_agent,cont[self.Network_agent]])
        trust = '='.join([self.Network_trust,cont[self.Network_trust]])
        dsn = f"{core};{system};{agent};{trust}"
        self.add_new_attribute(dsn=dsn)
        conn = pyodbc.connect(dsn)
        # cur= conn.cursor()
        return conn
    def read_source(self,name = None,change = False,lines = False):
        # global test 
        name = name if name  is not None else self.name 
        if name is None:
            return# для теста переменная
        if  self.lib is None:
            source = '\\'.join(self.path) + '.'.join([name,self.ext])
        else:
            source = self.path +'\\'+ '.'.join([name,self.ext])
            print(source)            
        self.source = source if change else self.add_new_attribute(source=source)
        exe_file = open(source,'r',encoding = self.encoding)
        # test = exe_file.readlines()
        return  exe_file.readlines() if lines else exe_file.read()
    def args(self):
        return (self.__dict__)

#если обьект не вызывается
class SQL_Query(SQL,default_server = "SQL Server" ,trusted ="yes" ):
    count = 0
    all_queries = []
    def __init__(self,counter = None, **kwargs):
        super(SQL_Query,self).__init__(**kwargs)
        # self.counter =  0 if counter is None else len(rgcsql.query_coll.keys() )
        self.call_names = set()
        self.first_query = self.name if len(self.call_names) == 0 else self.call_names[0]
        self.last_query = self.name if len(self.call_names) == 0 else  self.call_names[-1]
        SQL_Query.all_queries.append(self.name)
        if self.__class__.count > 0 :
            self.initialized:bool = True
        else :
            self.__class__.count += 1
    def get_sql_df(self,name = None,conn=None):
        if name  is not None: 
            print(name)
            self.name = name
            self.call_names.add(name)
            self.exe_file = self.read_source(change = True) 
        return pd.read_sql_query(self.exe_file,self.conn)
    # def get_sql_query(df):
    #     source = self.path + self.name + self.ext
    @staticmethod
    def ParentObject(struct):
        return SQL_Query(*struct.args())
        


class File(Source):
    pass
class File_Query(Source):
    pass


# для примера когда нужно будет создавать суперкласс
# # defining a SuperClass
# class SuperClass:

#      # defining __init_subclass__ method
#     def __init_subclass__(cls, **kwargs):
#         cls.default_name ="Inherited Class"
  
# # defining a SubClass
# class SubClass(SuperClass):
  
#      # an attribute of SubClass
#     default_name ="SubClass" 
#     print(default_name)
  
# subclass = SubClass()
# print(subclass.default_name)

# new_data.__dict__