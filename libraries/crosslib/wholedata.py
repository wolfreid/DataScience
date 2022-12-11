ROOT_QUERY = r"\\ent\root\HQ\Departments\NaturalGas\Диспетчерская УК\ЦДУ\Методика прогнозування\расчет населения ПАТ\Прогнозирование\IT"
ROOT_FILE = r"\\Sho-fs02\hq\Departments\NaturalGas\Диспетчерская УК\ЦДУ\Методика прогнозування\расчет населения ПАТ\Прогнозирование\BIG Data"
LANG  = 'ua'
from distutils.log import error
from operator import methodcaller
from unicodedata import name
import connections as cons
import pandas as pd
import os
import logging
logger = logging.getLogger(__name__)
import process_tables as tidy
from collections import namedtuple

class Descriptive():
    _instance = None
    _count = 0 #считает число инициализированных классов
    _count_err  = 0
    coll_items= []
    coll_feed = []
    item_names =[]
    feed_names = []
    count =0 #считает число инициализированных обьектов
    table = tidy.Table()
    # Constructor = namedtuple('Stat','name action hash')
    # stat = Stat()
    def __init__(self,*others,**kwothers) -> None:
        self.path:str = None#путь не нужен для обьекта, снять с словаря атриубтов
        self.feed = None #Не нужен для обьекта пока что, снять со словаря атрибутов
        self.stuff = None     #Не нужен для обьекта пока что, снять со словаря атрибутов
        self.method:str = None #нужен для обьекта          
        self.model = None     #нужен для обьекта        
        self.count+=1
        self.parse_date  = False         #нужен для обьекта
        self.separate = False
        self.stat = None
        if LANG == 'ua' and LANG not in others:
            self.reporting  = ['Фактичний','Оперативний']       #нужен для обьекта
        elif 'ru' in others:
            pass
 
        if self.__class__._count > 0 :
            self.initialized:bool = True
        else :
            self.stuff = self.__class__.stuff
            self.parse_date = self.__class__.parse_date
            # self.table = self.__class__.table #для обьектов
            self.__class__._count += 1    
    # @staticmethod
    def add_new_attribute(cls,*arr,**attribute):
        if not attribute:
            attribute = list(arr) 
        else :
            attribute = list(attribute.items())[0]
        if not hasattr(cls,attribute[0]):
            setattr(cls,attribute[0],attribute[1])
    def __repr__ (self): 
      pass
    @classmethod
    def sql_grab(cls,method,feed, model,**kwargs):
        cls.feed = feed #
        engine = cls.feed.Driver
        cls.method = method
        cls.stuff  = list(model.keys())
        cls.parse_date  = kwargs["parse_date"]
        for key,value in kwargs.items():
            cls.add_new_attribute(cls,key,value) 
        if method.lower() in ["корреляція","correlation","corr"]:
            # model = cls.model            
            count_err = 0
            for div in cls.stuff:
                if div in ('feed','items'):                
                    family  = model[div]
                for member in family:
                    try:
                        df = cls.feed.get_sql_df(member)
                        df  = cls.table.readtable(df,engine,parse_date = cls.parse_date)
                        name  = cls.feed.name
                        if div =='items':
                            cls.coll_items.append(df)                        
                            cls.item_names.append(name)
                        else:
                            cls.coll_feed.append(df)
                            cls.feed_names.append(name)
                    except Exception as error:
                        count_err+=1
                        logger.error(logger.error(error,__name__))
                    else:
                        cls._count_err += count_err
            return count_err       
    def create_model(self,union,on,into):
        stuff = self.stuff
        feed = dict(zip(self.feed_names,self.coll_feed))
        items = dict(zip(self.item_names,self.coll_items))
        model = {stuff[1]:feed,stuff[0]:items}
        if union and on and into:
            df = pd.concat([model[on][union[0]],model[on][union[1]]])
            for item in union:#delete old members
                index= self.feed_names.index(item)     
                self.coll_feed.pop(index)
                self.feed_names.pop(index)            
            self.coll_feed.append(df)
            self.feed_names.append(into)
            feed = dict(zip(self.feed_names,self.coll_feed))
            items = dict(zip(self.item_names,self.coll_items))
            model= {stuff[1]:feed,stuff[0]:items}
        self.model = model
    def __new__(cls, *args, **kwargs): #паттерн синглтон, все обьекты имеют одни свойства
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
    @staticmethod
    def isdir(path):        
        if os.path.isdir(path):
            endings = set(map(lambda x:'.'+x.split('.')[1].lower(),os.listdir(path)))
            if {'.json','.xlsx','.xls','.csv'} & endings !=set():
                return True
            else:
                return False
        else:
            return False
        # if lists_with_path = os.listdir(path)
    @classmethod
    # @table.parsed()
    def file_grab(cls,method,model,**kwargs):
        cls.method = method
        cls.stuff  = list(model.keys())
        cls.parse_date = kwargs["parse_date"]
        # try:
        for key,value in kwargs.items():
            cls.add_new_attribute(cls,key,value) 
        if method.lower() in ["корреляція","correlation","corr"]:        
            count_err = 0
            for div in cls.stuff:
                if div in ('feed','items'):                
                    family  = model[div]
                    for member in family:
                        try:
                            dir = cls.isdir(family[member])
                            df = cls.table.readtable(family[member],dir,parse_date = cls.parse_date)
                            name  = member                        
                            if div =='items':
                                cls.coll_items.append(df)                        
                                cls.item_names.append(name)
                            else:
                                cls.coll_feed.append(df)
                                cls.feed_names.append(name)
                        except Exception as error:
                            logger.error(error,__name__)
                            count_err+=1
                        else:
                            cls._count_err += count_err
            return count_err
    
    def validation(self,**args):
        div = args[0]
        if div in ('feed','items'):                
            items  = args[1]
            model = self.model[div]
            feed = filter(lambda item: item in items,model)
    # @classmethod
    def calculate(self,*tables,name,what):
        method = what
        data = self.model['feed'][name]
        stata = self.stata #инициализированный обьект с расчетами
        stata.balance = name
        data  = method(data,name)
         
        
        
        # return stat(methods)
    # метод и обьект создания таблиц
    # @classmethod
    # def auot_grab(cls,method,model,**kwargs):
    #     cls.method = method
    #     cls.stuff  = list(model.keys())
    #     if method in ["корреляція","correlation","corr"]:
    #         for key,value in kwargs.items():
    #             cls.add_new_attribute(cls,key,value)
    #         if hasattr(cls,'table'):
    #             # df = cls.table.
    #             cls.coll_items.append(df)
    #             cls.item_names.append(name)  
                         


# class Stat(Descriptive):
#     def __init__(self, *others, **kwothers) -> None:
#         super().__init__(*others, **kwothers)





print(__name__=='__main__')
