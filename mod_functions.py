"""
Notes on Zulip Objects:

user_groups -- dictionaries with 'users', 'name'
streams -- dictionaries with 'name', 'description' (https://zulipchat.com/api/get-streams)
principals -- list of user_id's or zulip_email's

"""

import re

def match_key(list_of_dicts, my_key, my_value):
    """
    my_key needs to be a string
    my_value is anything
    """
    possibles =[]
    for dict0 in list_of_dicts:
        if dict0[my_key] == my_value:
            possibles.append(dict0)
    return possibles
    
    
def make_inclusive_search_key(words):
    """
    >>> words = ['apple','banana','c']
    >>> key=make_inclusive_search_key(words)
    "^(apple|banana|c)"
    >>> re.search(key,"copper")
    True
    
    we could have also used "starts with"
    """
    search_key = "("
    n = len(words)
    for i in range(n-1):
        search_key = search_key + words[i]+ "|"
    search_key = "^"+search_key+words[n-1]+")"
    return search_key


#######################
        
def subscribe_usergroup_to_stream(my_user_group,my_stream):
    """
    Takes the Zulip format of user groups and users
    """
    my_users = my_user_group['users'] #returns user id
    return client.add_subscriptions(my_stream,myusers)
    
    
def get_usergroup_from_groupname(groupname):
    """
    group_name needs to be a string for the group.
    """
    some_weird_dictionary = client.get_user_groups() #maybe this should only be run once and we keep track of the dictionary
    list_of_dicts = some_weird_dictionary['user_groups']
    return list_of_dicts
    
    
def get_stream_from_streamname(mystreamname):
    some_weird_dictionary = client.get_streams()
    list_of_streams = weird_dictionary['streams']
    my_list_of_streams = match_key(list_of_streams,'name',mystreamname)
    return my_list_of_streams
    
    
def mod_subscribe_usergroup_to_stream(mygroupname,mystreamname):
    """
    
    """
    my_user_group = get_users_from_groupname(mygroupname)
    subscribe_usergroup_to_stream(my_user_group,mystreamname)


    

            
