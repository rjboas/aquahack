import rich
from rich.console import Console
from rich.theme import Theme
from rich.highlighter import RegexHighlighter
from rich.prompt import Prompt
from time import sleep
import sys

theme = Theme({
    'prompt.user': 'bright_white',
    'cmd.output': 'white',
    'prompt.friendly': 'bright_green',
    'prompt.evil': 'bold red',
    'prompt.joke': 'yellow',
    'prompt.error': 'dark_orange',
    'cmd_special.ip': 'magenta',
    'cmd_special.userat': 'cyan',
    'cmd_special.bootloggreen': 'green',
})


class AquahackHighlighter(RegexHighlighter):
    '''Apply style to miscellaneous text outputs'''

    base_style = 'cmd_special.'

    highlights = [
        # IPv4 Address Highlighting
        r'(?P<ip>(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})',
        # xxx@xxx highlighting
        r'(?P<userat>[a-zA-Z][a-zA-Z0-9.-]*\@[a-zA-Z0-9.-]+)',
        # [  OK  ] make green
        r'(?P<bootloggreen>\[  OK  \])',
    ]


console = Console(
    theme=theme,
    highlighter=AquahackHighlighter()
)

speed_control = 1.0
try:
    speed_control = float(sys.argv[1])
except Exception:
    pass

def type_print(text, style='', speed=1):
    speed = ( speed * 0.8 ) / speed_control
    text += '\n'
    for char in text:
        console.print(char, style=style, end='')
        if char == ' ':
            sleep(0.15 * speed)
        elif char == '.':
            sleep(0.4 * speed)
        elif char == ',':
            sleep(0.3 * speed)
        elif char == '\n':
            sleep(0.6 * speed)
        else:
            sleep(0.1 * speed)


class Character:
    def __init__(self, style, speed=1):
        self.style = style
        self.speed = speed

    def print(self, text):
        type_print(text, style=self.style, speed=self.speed)


class StoryText:
    def __init__(self, richtext: str, character: Character):
        self.richtext = richtext
        self.character = character

    def __str__(self):
        return self.richtext

    def print(self):
        self.character.print(self.richtext)


cmd_output = Character('cmd.output', speed=0)
good = Character('prompt.friendly')
evil = Character('prompt.evil')

with open('extra_data/startup.txt', 'r') as file:
    startup = file.read()

with open('extra_data/kpanic.txt', 'r') as file:
    kpanic = file.read()

prompts = {
    0: StoryText(startup, cmd_output),
    1: StoryText('''\
Hi there.
I'm Devn Ul, and I need your help.
There's someone on this network that I need to gain access to.
I'd really appreciate if you could help me out; there's only so much I can do from here.
First we'll need to find their IP address.
We'll need to scan with nmap, so first let's get our network info from ip addr.''', good),
    2: StoryText('''\
Nice work!
Go ahead and run a scan with nmap on 10.0.12.119/19.''', good),
    3: StoryText('''\
Alright, looks like we've found our target.
We won't be able to get anywhere without credentials though, so I've prepared a little script to help.
Just download it from https://github.com/rjboas/aquahack/tree/main/extra_data/script.sh using wget''', good),
    4: StoryText('''\
Don't forget that to make it executable (note: use +x style).''', good),
    5: StoryText('''\
Yep, looks good now. Go ahead and run it.''', good),
    6: StoryText('''\
Ahaha, piece of cake.

We'd best not delay, so go on and ssh into their root user from here...
Oh, it looks like their IP went off screen, I believe it was 10.0.14.87.''', good),
    7: StoryText('''\


Wow, you really though that'd work?
Looks like you'll need to step up your game if you don't want to fall for my little tricks.
I'd love to just leave you be, but that script of yours is a litte troublesome.

So if you could hold on for a moment--

 > rm -rf /''', evil),
    8: StoryText('''\n\n\nWarning: System integrity compromised.''', cmd_output),
    9: StoryText(''' > cat /dev/urandom | sudo tee /proc/sysrq-trigger''', evil),
    10: StoryText(kpanic, cmd_output),
}

correct_commands = {
    0: ('help', ''),
    1: ('ip addr', '''1: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
link/ether dc:a6:32:f6:72:9e brd ff:ff:ff:ff:ff:ff
inet 10.0.12.119/19 brd 10.0.31.255 scope global dynamic noprefixroute wlan0
   valid_lft 42934sec preferred_lft 37534sec
inet6 fe80::4360:be33:9bf7:f1cc/64 scope link
   valid_lft forever preferred_lft forever'''),
    2: ('nmap 10.0.12.119/19', '''Starting Nmap 7.70


Nmap scan report for 10.0.14.87
Host is up (0.000025s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh

Nmap done: 1 host up scanned in 1.00 second'''),
    3: ('wget https://github.com/rjboas/aquahack/tree/main/extra_data/script.sh', '''
Resolving github.com...
Connetcting to github.com... connected.
HTTP request sent, awaiting response... 200 OK
Saving to: 'script.sh'

'script.sh' saved'''),
    4: ('chmod +x ./script.sh', ''),
    5: ('./script.sh', 'Bruteforcing n cases...\n...\n...\n\nPredicting possible permutations...\n...\n...\n\nSatisfying predicate...\n...\n...\n\nPassword found! ********'),
    6: ('ssh root@10.0.14.87', 'root@10.0.14.87\'s password: ********'),
    7: ('exit', '')
}

def do_pass():
    pass

misc_commands = {
    'cat /dev/urandom | sudo tee /proc/sysrq-trigger': (kpanic, exit),
    'cat': ('No pets allowed.', do_pass),
    'sleep': ('No rest for the wicked', do_pass),
    'sudo': ('You are not in the sudoers file.\n This incident will be reported.\n\nsee https://xkcd.com/838/\n', do_pass),
    'cd': ('There\'s nowhere to go.', do_pass),
    'shutdown': ('You can\'t stop the party.', do_pass),
    'PortHack': ('Wrong game.', do_pass),
    'rm -rf /': ('\n\n\n\n\n\n\n\n\nWarning: System integrity compromised.\nRebooting...\n\n\
Error: /boot does not exist\nEntering recovery mode...\
Recovery mode failed. Halting...', exit),
}

def check_and_process_command(command, i):
    command = command.strip()

    sleep(0.4)

    if correct_commands[i][0] == command \
            or correct_commands[i][0].replace('./', '') == command:
        for line in correct_commands[i][1].split('\n'):
            console.print(line, style='cmd.output')
            if line.endswith('...') or line == '':
                sleep(0.5)
        return True

    command = command.split(' ')[0] if command not in misc_commands else command
    if command in misc_commands:
        text, function = misc_commands[command]
        console.print(text, style='prompt.joke')
        function()
    else:
        console.print('Error: command not found.', style='prompt.error')

    sleep(0.2)

    return False


def main():
    try:
        for i, line in prompts.items():
            sleep(1)
            line.print()
            if i > 6: # If we are past the point where the evil person takes control
                continue
            command = Prompt.ask(prompt='[blinking white] user@aquahack ~ ')
            while check_and_process_command(command, i) != True:
                command = Prompt.ask(
                    prompt='[blinking white] user@aquahack ~ ')

    except KeyboardInterrupt as e:
        return


if __name__ == '__main__':
    main()
