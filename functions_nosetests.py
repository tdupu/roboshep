import sys
#sys.path.append('/Library/Python/3.7/site-packages/zulip_bots/bots/roboshep/table_functions')
#sys.path.append('/Library/Python/3.7/site-packages/zulip_bots/bots/roboshep/table_editor')
sys.path.append('/Library/Python/3.7/site-packages/zulip_bots/bots/roboshep')

from mod_functions import *
from table_editor import *

def test_numbers_3_4():
    x = 3*4
    assert x==12
    
def test_make_inclusive_search_key1():
    words = ['apple','banana','c']
    key=make_inclusive_search_key(words)
    print(key)
    assert key =="^(apple|banana|c)"

def test_make_inclusive_search_key2():
    words = ['apple','banana','c']
    key=make_inclusive_search_key(words)
    assert re.search(key,"copper")
    
def test_match_key():
    dicta = {'name':'Cindy', 'hobby':'golf', 'favorite_food':'pizza'}
    dictb = {'name':'Chuck', 'hobby':'sports', 'favorite_food':'fish'}
    dictc = {'name':'Mike', 'hobby':'sports', 'favorite_food':'chocolate'}
    my_list_of_dicts = [dicta,dictb,dictc]
    answer1 = [dictb,dictc]
    output_list=match_key(my_list_of_dicts,'hobby','sports')
    assert output_list == answer1
    
    
def test_sheet_name():
    S = SheetObject('testbook.xlsx','Sheet1')
    name = S.sheetname
    assert name == 'Sheet1'

def test_file_name():
    S = SheetObject('testbook.xlsx','Sheet1')
    name = S.filename
    assert name =='testbook.xlsx'
    
def test_column_dict():
    S = SheetObject('testbook.xlsx','Sheet1')
    column_dict = S.column_dict
    answer = {1:"name",2:"age", 3:"rank"}
    assert column_dict ==answer
    
def test_set_of_keys():
    S = SheetObject('testbook.xlsx','Sheet1')
    set_of_keys = S.set_of_keys
    answer = set(['name','age','rank'])
    assert set_of_keys =='testbook.xlsx'

def test_number_of_keys():
    S = SheetObject('testbook.xlsx','Sheet1')
    n = S.number_of_keys
    assert n==3
    
def test_keys():
    S = SheetObject('testbook.xlsx','Sheet1')
    answer = ['name','age','rank']
    keys = S.keys
    assert keys==answer
    
def test_subsets():
    dict0 ={'name':'Joe', 'age':9, 'rank':'captain' }
    dict1 = {'rank':'noob'}
    keys0 = dict0.keys()
    keys1 = dict1.keys()
    set0 = set(keys0)
    set1 = set(keys1)
    assert (set1.issubset(set0))==True
    
def test_valid_new_entry():
    S = SheetObject('testbook.xlsx','Sheet1')
    new_entry = {'name':'Joe', 'age':9, 'rank':'noob' }
    new_entry2 = {'name':'Joe', 'age':9}
    is_it_ok = S.is_valid_entry(new_entry)
    is_it_ok2 = S.is_valid_entry(new_entry2)
    is_it_ok3 = S.is_valid_entry({'rank':'captain'})
    output = (is_it_ok and is_it_ok2 and is_it_ok3)
    assert (output == True)

    
def test_get_entries1():
    S = SheetObject('testbook.xlsx','Sheet1')
    is_it_ok3 = S.is_valid_entry({'rank':'captain'})
    assert (is_it_ok3 ==True)
    
def test_get_entries2():
    S = SheetObject('testbook.xlsx','Sheet1')
    entries = S.get({'rank':'captain'})
    answer = [{'name':'Joe', 'age':1, 'rank':'captain'}, {'name':'Mary', 'age':4, 'rank':'captain' }]
    assert (entries==answer)
    

def test_get_index():
    assert True
    
def test_row_to_dict():
    assert True
    
def test_save():
    assert True
    
def test_remover():
    assert True
