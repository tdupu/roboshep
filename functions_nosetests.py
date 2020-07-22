import sys
#sys.path.append('/Library/Python/3.7/site-packages/zulip_bots/bots/roboshep/table_functions')
#sys.path.append('/Library/Python/3.7/site-packages/zulip_bots/bots/roboshep/table_editor')
sys.path.append('/Library/Python/3.7/site-packages/zulip_bots/bots/roboshep')

from mod_functions import *
#import mod_functions

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
