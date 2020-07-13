#
# Author: Taylor Dupuy 7/1/2020, modified default Dropbox bot for Zulip for parser
#
#
#
from typing import Any, Dict, List, Tuple
import zulip



class RoboModHandler:

    def initialize(self, bot_handler: Any) -> None:
           #self.config_info = bot_handler.get_config_info('dropbox_share')
           #self.ACCESS_TOKEN = self.config_info.get('access_token')
           self.client = zulip.Client(config_file="~/zuliprc") # Pass the path to your zuliprc file here.


    def usage(self) -> str:
        return '''
        This is a boilerplate bot that responds to a user query with
        "beep boop", which is robot for "Hello World".

        This bot can be used as a template for other, more
        sophisticated, bots.
        '''

    def handle_message(self, message: Dict[str, Any], bot_handler: Any) -> None:
        command = message['content']
        original_sender = message['sender_email']
        
        if command == "":
            command = "help"
        
        msg = mod_command(self.client, command)
        bot_handler.send_reply(message, msg)
    
        
    def get_help() -> str:
    #FIXME
    return '''
    Example commands:

    ```
    @mention-bot usage: see usage examples
    @mention-bot add: add users to a stream
    @mention-bot rm: remove users from a stream
    ```
    '''
    
    #Not exactly sure what this does.
    REGEXES = dict(
        command='(help|subscribe|usage)',
        streams=r'(\S+)' #this isn't right
        users=r'(\S+)' #this isn't right
    )
    
    def syntax_help(cmd_name: str) -> str:
        commands = get_commands()
        f, arg_names = commands[cmd_name]
        arg_syntax = ' '.join('<' + a + '>' for a in arg_names)
        if arg_syntax:
            cmd = cmd_name + ' ' + arg_syntax
        else:
            cmd = cmd_name
        return 'syntax: {}'.format(cmd)
    
    def get_commands() -> Dict[str, Tuple[Any, List[str]]]:
        return {
            'help': (mod_help, ['command']),
            'usage': (mod_usage, ['command']),
            'subscribe': (mod_subscribe, ['streams', 'users']),
            'unsubscribe': (mod_unsubscribe, ['streams','users'])
        }
    

    def mod_command(client: Any, cmd: str) -> str:
        cmd = cmd.strip()
        if cmd == 'help':
            return get_help()
        cmd_name = cmd.split()[0]
        cmd_args = cmd[len(cmd_name):].strip()
        commands = get_commands()
        if cmd_name not in commands:
            return 'ERROR: unrecognized command\n' + get_help()
        #ELSE, get the function and the arg names
        f, arg_names = commands[cmd_name] #passes the function and how to use it
        #For each argname (list of strings)
        partial_regexes = [REGEXES[a] for a in arg_names]
        regex = ' '.join(partial_regexes)
        regex += '$'
        m = re.match(regex, cmd_args)
        if m:
            return f(client, *m.groups())
        else:
            return 'ERROR: ' + syntax_help(cmd_name)
            
    def mod_subscribe(client: Any, cmd: str) -> str:
        return "I will have added some stuff."
        
        #!/usr/bin/env python3

        # Subscribe to the stream "new stream" https://zulipchat.com/api/subscribe
        #result = client.add_subscriptions(
        #    streams=[
        #        {
        #            'name': 'new stream',
        #            'description': 'New stream for testing',
        #        },
        #    ],
        #)
        # To subscribe other users to a stream, you may pass
        # the `principals` argument, like so:
        #user_id = 25
        #result = client.add_subscriptions(
        #    streams=[
        #        {'name': 'new stream', 'description': 'New stream for testing'},
        #    ],
        #    principals=[user_id],
        #)
        #print(result)
    

    def syntax_help(cmd_name: str) -> str:
        commands = get_commands()
        f, arg_names = commands[cmd_name]
        arg_syntax = ' '.join('<' + a + '>' for a in arg_names)
        if arg_syntax:
            cmd = cmd_name + ' ' + arg_syntax
        else:
            cmd = cmd_name
        return 'syntax: {}'.format(cmd)

    def mod_help(client: Any, cmd_name: str) -> str:
        return syntax_help(cmd_name)

    def mod_usage(client: Any) -> str:
        return get_usage_examples()

handler_class = RoboModHandler


#def handle_message(self, message, bot_handler):
   #original_content = message['content']
   #original_sender = message['sender_email']
   #new_content = original_content.replace('@followup', 'from %s:' % (original_sender,))

   #bot_handler.send_message(dict(
   #    type='stream',
   #    to='followup',
   #    subject=message['sender_email'],
   #    content=new_content,
   #))
