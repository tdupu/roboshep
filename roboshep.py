
"""
Authors: Taylor Dupuy and David Kewei Lin, 7/1/2020

INSTRUCTIONS:
To run the bot one needs to go into Zulip and download the zuliprc file.
    zulip-run-bot roboshep --config-file /Users/taylordupuy/Dropbox/computing/dupuy-zulip-bots/zuliprc
I found that I need to run this from the path of the zuliprc file with the full path of the zuliprc file in the name.

"""


import sys
#your need to modify this to your local working directory
sys.path.append('/Library/Python/3.7/site-packages/zulip_bots/bots/roboshep')

from typing import Any, Dict, List, Tuple
import zulip
#import python3 #don't do this, it breaks.
import re #https://docs.python.org/3/library/re.html
from openpyxl import * #I had to install this using pip3, this is for excel
from table_functions import *
from mod_functions import *
from table_editor import *


HELP_MESSAGE = """
            Commands: 

            notepad <some text>
            -- stores text as a list of words in the notepad (to be used later for execution).
            
            notepad_type <mytype>
            -- sets the type of the notepad. To be used later.
            
            print_notepad
            -- shows what is currently on the notepad
            
            notepad_to_group <groups>
            -- moves the whatever is stored in the notepad to the list of groups given.
            
            notepad_to_streams <streams>
            -- moves whatever is stored in the notepad to the designated streams.
            -- streams are matched from the begining of the word so for example if you run
            
                    >notepad_to_streams D
            
            it will convert whatever is in the notepad to users then add those to the streams which have names starting with the letter D.
            
            notepad_to_usergroup <users>
            -- moves whatever is in the notepad to the usergroups described
            
            notepad_to_agittoc_group
            -- converts whatever is in the notepad to users then adds them to both the corresponding group and stream.
            
            """ 


class RoboModHandler:
    '''
    AGITTOC moderator tools
    
    How to implement bots is described here:
        https://zulipchat.com/api/running-bots
    
    The client and API are described here:
        https://zulipchat.com/api/subscribe
    
    Code for existing bots is here (which doesn't use the API):
        https://github.com/zulip/python-zulip-api/tree/master/zulip_bots/zulip_bots/bots
    '''
    
    
#    def initialize(self, bot_handler: Any) -> None
    def __init__(self):
         '''
         This is how the instantiate a client in the dropbox_share bot.
         I'm assuming this runs at the startup.
         '''
         # self.client = zulip.Client(config_file="/Users/taylordupuy/Dropbox/computing/dupuy-zulip-bots/zuliprc")
         self.client = zulip.Client(config_file="./zuliprc")
         self.notepad = ""
         self.notepad_type = "users"
         self.NOTEPAD_TYPES_ALLOWED = ['users','streams'] #maybe I should put this constant outside?

         self.testing()
    
    def testing(self) -> None:
        """
        For dev-testing without sending messages to the bot
        """
        
        print("ping")

        # # Get all streams
        # # stream fields: ['name', 'stream_id', 'description', 'rendered_description', 'invite_only', 'is_web_public', 'stream_post_policy', 'history_public_to_subscribers', 'first_message_id', 'message_retention_days', 'is_announcement_only']
        # all_streams = self.client.get_streams()["streams"]
        # print(all_streams[0].keys())
        # print("Names of all streams:", [stream["name"] for stream in all_streams])
        

        # # Get all users
        # # user fields: ['email', 'user_id', 'avatar_version', 'is_admin', 'is_owner', 'is_guest', 'is_bot', 'full_name', 'timezone', 'is_active', 'date_joined', 'avatar_url', 'bot_type', 'bot_owner_id']
        # all_users = self.client.get_members()['members']
         
    def usage(self) -> str:
        return '''
        AGITOCC sheep dog. (a bot for sorting)
        
        notepad <some text>
        
        notepad_type <users, streams, groups>  -- sets the type of the notepad.
        
        notepad_to_streams <streams>
        
        '''

    
    def handle_message(self, message: Dict[str, Any], bot_handler: Any) -> None:
        """
        This is the is the main function for message handling.
        
        All of the things you can read off of a message are here:
        https://zulipchat.com/api/get-messages
        
        """

        # stuff in a message: 'id', 'sender_id', 'content', 'recipient_id', 'timestamp', 'client', 'subject', 'topic_links', 'is_me_message', 'reactions', 'submessages', 'sender_full_name', 'sender_short_name', 'sender_email', 'sender_realm_str', 'display_recipient', 'type', 'stream_id', 'avatar_url', 'content_type', 'full_content'

        # Ignore messages from Notification Bot
        if message['sender_full_name'] == 'Notification Bot':
            return

        user_text = message['content']
        user_words = user_text.split()
        command_word = user_words[0]
        user_inputs = user_words[1:]
        
        input_text = ",".join(user_inputs)
            
        msg = ""
        if command_word == 'help':
            msg=HELP_MESSAGE
            
        elif command_word == 'notepad':
            self.notepad = user_inputs
            msg = self.print_notepad()
            
        elif command_word == 'find_me_a_group':
            #
            # This is all untested
            #
            zulip_id = message['sender_id']
            email = message['sender_email']
            timestamp = message['timestamp']
            
            workbook = load_workbook('agittoc.xlsx')
            seeking_group_sheet = workbook["seeking_group"]
            #add new entry to with zulip_id and email to sheet
            
        elif command_word == 'get_more_members':
            #
            # This is all untested
            #
            msg = "NOT IMPLEMENTED, but... this will add you to a list of groups looking for new members"
            stream_id = message['stream_id']
            timestamp = message['timestamp']
            workbook = load_workbook(filename='agittoc.xlsx')
            seeking_members_sheet = workbook["seeking_members"]
            
        elif command_word == 'this_group_is_dead':
            msg = "NOT IMPLEMENTED, but... this will add this stream to a list of inactive streams so new members will not be added to this stream."
            
            #msg = "This stream is no longer accepting new members."
        
        elif command_word == 'resolve_wait_list':
            msg = "NOT IMPLEMENTED YET"
            #we will match people from the lists looking for new members and the list looking for old members.
            
        elif command_word == 'notepad_type':
            proposed_type = user_inputs[0]
            if proposed_type in self.NOTEPAD_TYPES_ALLOWED:
                self.notepad_type = proposed_type
                msg = "notepad type: %s " % self.notepad_type
            else:
                msg = "type %s not allowed! \n No changes made. Only streams, " % proposed_type
                
        elif command_word == 'add_me_to':
            #maybe this should be "subscribe" to go along with their lingo
            stream_name = " ".join(user_inputs)
            user_id = message["sender_id"]
            msg = self.add_sender_to_stream(user_id, stream_name)
            
        elif command_word == 'list':
            if user_inputs[0] == 'streams':
                msg = f"{self.get_all_stream_names()}"
                
        elif command_word == 'print_notepad':
            msg = self.print_notepad()
            
        elif command_word == 'print_notepad_type':
            msg = self.print_notepad_type()
            
        elif command_word == 'notepad_to_streams':
            msg = self.notepad_to_streams(self.notepad, self.notepad_type, user_inputs)
            
        elif command_word == 'ping':
            msg='pong!'
            
        else:
            print("Not a command!")
            msg = "command word: %s" % command_word + "\n" + "input: %s" % input_text + "\n" + "notepad is: %s " % self.notepad
        
        if msg != "":
            bot_handler.send_reply(message,msg)
        
    ########################################
    #### Commands that execute something and return msg
    ########################################
    """
    Zulip has these crazy dictionarys that they return on queries and one of the things they like is a message.
    """
        
    def print_notepad(self):
        return "notepad = %s " % self.notepad
    
    def print_notepad_type(self):
        return "notepad_type = %s" % self.notepad_type

    ########################################
    #### Adding self to stream
    ########################################

    def add_sender_to_stream(self, user_id, stream_name):
        # https://zulipchat.com/api/subscribe
        # returns message

        # validate stream_name
        stream_names = self.get_all_stream_names()
        if stream_name not in stream_names:
            return f"Invalid stream name: '{stream_name}'"
        if not stream_name.startswith("Group"):
            return f"You can only be added to streams starting with 'Group'!"
        result = self.client.add_subscriptions(
            streams=[{'name': stream_name}],
            principals=[user_id])
        print(result)
        return f"Added you to {stream_name}!"

    def get_all_stream_names(self) -> List:
        all_streams = self.client.get_streams()["streams"]
        return [stream["name"] for stream in all_streams]


##################################
##################################
##################################

    def notepad_to_streams(self, data, datatype, streamnames):
        
        msg = ''
        
        weird_dict_of_streams = self.client.get_streams()
        list_of_dicts_of_streams = weird_dict_of_streams['streams']
        #print(list_of_dicts_of_streams) #this works
        
        weird_dict_of_users = self.client.get_members()
        list_of_dicts_of_users = weird_dict_of_users['members']
        
        my_streams = []
        mystreamquery = make_inclusive_search_key(streamnames)
        print(mystreamquery)
        
        for dict0 in list_of_dicts_of_streams:
            if re.search(mystreamquery,dict0['name']):
                #print("hello")
                #print(dict0['stream_id']) #neverprinted
                my_streams.append(dict0)
                #print(my_streams)
                #msg = msg+'taylor was here' #this was me trying to debug
        
        if datatype == 'streams':
            my_streams2 = []
            mystreamquery2 = make_inclusive_search_key(streamnames)
            
            for dict0 in list_of_dicts_of_streams:
                if re.search(mystreamquery2,dict0['name']):
                    print('you are here')
                    print(dict0)
                    my_streams2.append(dict0)
                    
            my_principals = [] #this is what Zulip calls lists of user_id's or emails
            #someone could take away my PhD for what I'm about to do...
            
            #
            # THIS IS BROKEN. WE NEED A WAY TO COMPARE USERS TO STREAMS.
            #
            for user in list_of_dicts_of_users:
                for dict0 in my_streams2:
                    stream_id = dict0['stream_id']
                    user_id = user['user_id']
                    has_not_been_counted =(my_principals.count(user_id)==0)
                    is_a_member = False
                    if has_not_been_counted and is_a_member:
                        my_principals.append(user_id)
                            
        #final touches
        print(my_principals) #empty
        print(my_streams) #empty
        self.client.add_subscriptions(streams=my_streams, principals=my_principals)
        msg = msg + 'added %s to %s ' % (my_principals, my_streams)
        return msg



##################################
###helper functions for the client
##################################
        
    def subscribe_usergroup_to_stream(self, my_user_group,my_stream):
        """
        Takes the Zulip format of user groups and users
        """
        my_users = my_user_group['users'] #returns user id
        return self.client.add_subscriptions(my_stream,myusers)
        
        
    def get_usergroup_from_groupname(self, groupname):
        """
        group_name needs to be a string for the group.
        """
        some_weird_dictionary = self.client.get_user_groups() #maybe this should only be run once and we keep track of the dictionary
        list_of_dicts = some_weird_dictionary['user_groups']
        return list_of_dicts
        
        
    def get_streams_from_streamnames(self, mystreamname):
        """
        Depends on match_key
        """
        some_weird_dictionary = self.client.get_streams()
        list_of_streams = weird_dictionary['streams']
        my_list_of_streams = match_key(list_of_streams,'name',mystreamname)
        return my_list_of_streams
        
        
    def mod_subscribe_usergroup_to_stream(mygroupname,mystreamname):
        """
        
        """
        my_user_group = get_users_from_groupname(mygroupname)
        subscribe_usergroup_to_stream(my_user_group,mystreamname)
        
    def is_member_of(user_id,stream_name):
        raise NotImplementedError
        

handler_class = RoboModHandler




