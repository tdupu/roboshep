#
# Author: Taylor Dupuy 7/1/2020
#
#
#
from typing import Any, Dict, List, Tuple
import zulip
#import python3 #don't do this, it breaks.
import re #https://docs.python.org/3/library/re.html
from openpyxl import * #I had to install this using pip3, this is for excel


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
            zulip_id = message['sender_id']
            email = message['sender_email']
            timestamp = message['timestamp']
            
            workbook = load_workbook(filename='agittoc.xlsx')
            seeking_group_sheet = workbook["seeking_group"]
            #add new entry to with zulip_id and email to sheet
            
        elif command_word == 'get_more_members':
            msg = "NOT IMPLEMENTED, but... this will add you to a list of groups looking for new members"
            stream_id = message['stream_id']
            timestamp = message['timestamp']
            workbook = load_workbook(filename='agittoc.xlsx')
            seeking_members_sheet = workbook["seeking_members"]
            
            
            
        elif command_word == 'this_group_is_dead":
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
                msg = "type %s not allowed! \n No changes made. " % proposed_type
                
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
    
    
    ########################################
    ###Functions to Help With Searches
    ########################################

    def make_inclusive_search_key(self,words):
        """
        >>> words = ['apple','banana','c']
        >>> key=make_inclusive_search_key(words)
        "^(apple|banana|c)"
        >>> re.search(key,"copper")
        True
        
        we could have also used "starts with"
        """
        # search_key = "("
        # n = len(words)
        
        # for i in range(n-1):
        #     search_key = search_key + words[i]+ "|"
        
        # #we do the last one separately to close it off
        # search_key = "^"+search_key+words[n-1]+")"
        
        return f"^({'|'.join(words)})"
        
    def match_key(self, my_list_of_dicts, dictionary_key, myvalues):
        """
        This needs to be debugged
        """
        possibles =[]
        my_search_key = self.make_inclusive_search_key(myvalues)
        for dict0 in list_of_dicts:
            if re.search(my_search_key, dict0[dictionary_key]):
                possibles.append(dict0)
        return possibles

##################################
##################################
##################################

    def notepad_to_streams(self, data, datatype, streamnames):
        
        msg = ''
        
        weird_dict_of_streams = self.client.get_streams()
        list_of_dicts_of_streams = weird_dict_of_streams['streams']
        #print(list_of_dicts_of_streams) #this works
        
        my_streams = []
        mystreamquery = self.make_inclusive_search_key('streamnames')
        
        for dict0 in list_of_dicts_of_streams:
            if re.search(mystreamquery,dict0['name']):
                #print(dict0['stream_id']) #neverprinted
                my_streams.append(dict0)
                msg = msg+'taylor was here' #this was me trying to debug
        
        #if datatype == 'user_groups':
        #    weird_dict_of_user_groups = self.client.get_user_groups()
        #    print(weird_dict_of_user_groups)
        #    list_of_dicts_of_user_groups =weird_dict_of_user_groups['user_groups']
        #
        #    my_user_groups = []
        #    myuserquery = self.make_inclusive_search_key(self.notepad)
        #
        #    for dict0 in list_of_dicts_of_user_groups:
        #        if re.search(myuserquery,dict0['name']):
        #            my_user_groups.append(dict0)
        #
        #    my_principals = [] #this is what Zulip calls lists of user_id's or emails
        #    for dict0 in my_user_groups:
        #        members = dict0['members']
        #        for member in members:
        #            if my_principals.count(member)==0:
        #                my_principals.append(member)
        #
        
        if datatype == 'streams':
            my_streams2 = []
            mystreamquery2 = self.make_inclusive_search_key('streamnames')
            
            for dict0 in list_of_dicts_of_streams:
                if re.search(mystreamquery2,dict0['name']):
                    print(dict0)
                    my_streams2.append(dict0)
                    
            my_principals = [] #this is what Zulip calls lists of user_id's or emails
            for dict0 in my_streams2:
                    members = dict0['members']
                    #msg = msg + "%s" % members never printed
                    for member in members:
                        if my_principals.count(member)==0:
                            my_principals.append(member)
                            
        #final touches
        #print(my_principals) #empty
        #print(my_streams) #empty
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
        my_list_of_streams = self.match_key(list_of_streams,'name',mystreamname)
        return my_list_of_streams
        
        
    def mod_subscribe_usergroup_to_stream(mygroupname,mystreamname):
        """
        
        """
        my_user_group = get_users_from_groupname(mygroupname)
        subscribe_usergroup_to_stream(my_user_group,mystreamname)
        
    #
    # The two function above are REQUIRED by Zulip.
    #

handler_class = RoboModHandler




