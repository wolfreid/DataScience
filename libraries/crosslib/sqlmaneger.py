from typing import Collection
import re
from functools import wraps
import collections
from collections import namedtuple
import logging,sys,os

from numpy import isin
logger = logging.getLogger(__name__)

PATTERN = r'[^A-Za-z0-9\s+\w.\s+]+'
PATTERN_COM  = r'^(\/\*|\w)'

PATTERNS = [("word_order_hasher",PATTERN),
         ("prefix_hasher",PATTERN_COM),
         ("allcharacter_hasher","\/\*[A-Za-z]+\*/"),
          ("right_character_hasher","\/\*[A-Za-z]+"),
          ("word_hasher","[A-Za-z]+"),
           ("variable_hasher", '^(\/\*)')]
AVAILABLE_ELEMENT= ('variables','categories','data','changeble','categories')


class Structure():
    def __init_subclass__(cls,default_object,default_constructor) -> None:
        cls.default_object = default_object
        cls.default_constr = default_constructor
    collection_dict = {}
    alias = 'alias'
    default_options = ['Document','alias','Schema']
    def __init__(self,file,name,object = None) -> None:
        self.file = [line for line in file if not line.isspace()]
        self.name = name
        self.namespace = ['Document','Schema','name','action','hash','alias']
        self.key =object.__dict__[self.alias] if object is not None else None
        self.__class__.collection_dict[self.key]  = object    
    def File(self):
        setattr(Structure.File,"count",len(self.file))
        return self.File
    def add_new_attribute(self,**attribute):
        attribute = list(attribute.items())[0]
        if not hasattr(self,attribute[0]):
            setattr(self,attribute[0],attribute[1])

    @classmethod
    def get_by_key(cls,key):
        return cls._member_dict[key]  

     


class Parser(Structure,default_object = 'Document',default_constructor = ["Structure","Replace","Executive"]):
    count = 0
    cls_variables = 'variables'
    cls_categories  = 'categories'
    cls_data = 'data'
    cls_changeble = 'changeble'
    cls_commands = {'WHERE','SELECT','GROUP BY','ORDER BY','FROM','DECLARE','WITH','JOIN','QUERY'}
    Constructor = namedtuple('Document','name action hash')
    Schema = [("Structure","\/\*[A-Za-z]+\*/"),("Replace","\/\*[A-Za-z]+"),("Executive","[A-Za-z]+")]
    def __init__(self,variables = None,commands = None,categories = None,data = None,changeble= None,**kwargs) -> None:
        super(Parser,self).__init__(**kwargs)
        self.variables = variables
        self.categories = categories
        self.data = data
        self.changeble = changeble
        self.commands = commands
        self.parse_header()
        if self.__class__.count > 0 :
            self.initialized:bool = True
        else :
            self.__class__.count += 1
    def __call__(self, *args):
        pass

    def getDocumentObject(self, inplace = False,label = "Document",*parameters,**filters):
        # по спискам можно только будет выбрать фильтр за одним значением, или по и индексу
        # по словарям неогранниченное количество фильтров
        parameters = parameters if parameters else filters
        template  = self.__dict__["template"] if self.__dict__["template"] else False
        namespace = self.namespace
        
        if isinstance(parameters,tuple):
            types_parameters = list(dict.fromkeys(list(map(type,parameters))))[0]
            if types_parameters is int:
                return template[parameters]
            if types_parameters is str:
                if len(parameters) == 2:
                    if parameters[0] in namespace :
                        return list(filter(lambda Doc: (Doc.__class__.__name__ == label) and
                                                (Doc.__class__.__dict__[parameters[0]] == parameters[1]),template))
                elif len(parameters) ==3:
                    label = parameters
                    if len(set(parameters) & set(namespace))== 0:
                        return list(filter(lambda Doc: (Doc.__class__.__name__ == parameters[0]) and
                                                (Doc.__class__.__dict__[parameters[1]] == parameters[2]),template))
                else:
                    raise IndexError
        elif isinstance(parameters,dict):
            
            label = filters["label"] if "label" in parameters.keys() else label 
            if len(parameters.keys() & set(namespace))== 0:
                return list(filter(lambda Doc: (Doc.__class__.__name__ == label) and
                                        (Doc.__class__.__dict__[] == parameters[2]),template))
            
            filter[0] ="name" in template.__class__.__dict__.keys() 
        except IndexError as error:
            logger.error(error)
            return
        else:
            return list(filter(lambda Doc: Doc.__class__.__name__==,template))
        finally:
            return template
    def __setattr__(self, name, value):
        try:
            errors = False
            if not hasattr(self,name): #проверка предыдущего ключа
                errors = False
            else:
                errors = True
                if self.__dict__[name] is None:                
                    errors = False
                if self.__class__.count >= 1: #проверка обьекта инициализации, под номером
                    if value: # проверка текущего ключа
                        if isinstance(value, collections.Iterable): # проверка текущего ключа 
                            if isinstance(value,tuple) or isinstance (value,list):# проверка текущего ключа 
                                if not value in self.__dict__[name]: #проверка ключей нескольких версий 
                                    errors = False
                    else:
                        # print(name,value)
                        errors = False
            if errors == False:
                # print(errors)
                super(Parser, self).__setattr__(name, value)
            else:
                print(name,value)
                raise ValueError("Another property had already set",name,value,self.__class__.count)
        except (ValueError,KeyError) as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print(exc_type, fname, exc_tb.tb_lineno,error)
            logger.error(error)
        

    def hasher(*hash_expr1,**hash_expr2): 
        template = []
        
        hash_expr1= hash_expr1[0] if hash_expr1 and hash_expr1[-1] == hash_expr1[0] else hash_expr1
        def hasher(pattern_function):
            @wraps(pattern_function)
            def pattern(self,*myexpr1,**myexpr2):
                Document = self.__class__.Constructor
                Schema = self.__class__.Schema
                if hash_expr1 and isinstance(hash_expr1,tuple):
                    if len(hash_expr1)== 2:
                        Document,Schema =hash_expr1
                    else:
                        Schema  = hash_expr1
                elif hash_expr2 and isinstance(hash_expr2,dict):
                    if isinstance(hash_expr2["Document"],bool):
                        Document =  Document if hash_expr2["Document"] else None  
                        Schema = Schema if hash_expr2["Schema"] else None
                    else:    
                        Document = hash_expr2["Document"] if hash_expr2["Document"] else None
                        Schema = hash_expr2["Schema"] if hash_expr2["Schema"] else None
                if not myexpr2 and not myexpr1: 
                    expression = dict(Schema)
                else:
                    expression = dict(myexpr1) if myexpr1 else myexpr2                   
                for key,val in expression.items():
                    template.append(Document(key,key,val))
                return pattern_function(self,template,*myexpr1,**myexpr2)
            return pattern 
        return hasher

    @hasher(Document = True,Schema = True)
    
    def parse_header(self,template = None):
        # print(template)
        global PATTERN_COM,PATTERNS
        container = lambda file,pattern: {index:line for index,line in enumerate(file) if re.findall(pattern,line.strip(),re.IGNORECASE)}        
        variables_ref = f'{self.__class__.cls_variables}|{self.__class__.cls_categories}|{self.__class__.cls_data}|{self.__class__.cls_changeble}'
        commands_ref = '|'.join(list(map(lambda x: x[0] +'?'+x[1:],self.__class__.cls_commands)))
        PATTERN_COM = PATTERN_COM + '('+ commands_ref +')'
        commands = container(self.file,PATTERN_COM)
        variables = container(self.file,variables_ref) 
        filtered = set()
        temp = {}
        for key,value in variables.items():
            filtered.add(key)
            temp.update(dict.fromkeys([value.split(':')[0]],[value.split(':')[1]]))
        variables = temp
        
        for key in list(variables.keys()):
            variables[key] = re.sub(PATTERN,',',variables[key][0].strip())
            variables[key]  = variables[key].strip(',').split(',')
            variables[re.sub('^(\/\*)','',key)] = variables.pop(key) 
        return self.set_attributes(variables,commands,template) 
    def set_attributes(self,*header):
        self.variables = header[0][self.__class__.cls_variables]
        self.categories = header[0][self.__class__.cls_categories]
        self.data = header[0][self.__class__.cls_data]
        self.changeble = header[0][self.__class__.cls_changeble]
        self.commands =  header[1]
        self.add_new_attribute(template=header[2]) if header[2]  else None
    def build_file(self):
        pass

    # def safe_result(self):

class ObjectReport():
    def __init_subclass__(cls,default_name) -> None:
        cls.default_name = default_name 
    def __init__(self,code,name,alias) -> None:
        self.name = name
        self.code = code
        self.alias  = alias
class Organization(ObjectReport,default_name = 'Організація'):
  def __init__(self, code, name) -> None:
      super().__init__(code, name)
        
    
class Sector(ObjectReport,default_name = 'Сектор'):
    def __init__(self, code, name) -> None:
        super().__init__(code, name)

class Point(ObjectReport,default_name = 'Точка обліку'):
    def __init__(self, code, name) -> None:
        super().__init__(code, name)

class Data():
    def __init__(self, file, name) -> None:
        super().__init__(file, name)

