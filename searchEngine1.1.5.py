'''
Indentation in this code was given by 4-spaces, not tabs!
'''
import re
import sys
import os
from datetime import datetime
import time
from shutil import copyfile, rmtree

#*****Define Class Page*****#
class Page:
    ''' Page class
    
    Attributes
    ----------------
    title: str
        string for title of page
    
    contents: str
        multiline string for contents of page
    
    rank: int
        0 by default
        Stores the number of words in search_input that are present in title+contents
        
    Functions
    ----------------
    display_title():
        display the title of the page
        
    display_contents():
        display the contents of the page
        
    display():
        display title followed by two blank lines followed by contents of the page
        
    all(): 
        returns title followed by contents as one string
    '''
    def __init__(Self,title,contents,rank = 0):
        Self.title = title
        Self.contents=contents
        Self.rank = rank
    
    def display_title(Self):
        if len(Self.title)<51:
            print(Self.title)   
        else:
            print(Self.title[0:47]+'...')
        
    def display_contents(Self):
        print(Self.contents)
        
    def display(Self):
        print(Self.title+'\n\n'+Self.contents)
    
    def all(Self):
        return (Self.title+Self.contents)
       
#...............End class Page block...............#


#***************FUNCTIONS***************#

def clrscr():
    '''Clear console screen.
    On windows: os.name is 'nt'
    On Linux & Android: os.name is 'posix'
    '''
    if os.name == 'nt':
        os.system('cls')
    else:
        try:
            os.system('clear')
        except:
            pass
#....................End clrscr()....................#

def read_multiline(objects=''):
    '''Read paragraph
    
    Takes a multiline paragraph input from user.
    To finish typing, the endtext command is used at the end of the line.
    To use the word endtext at the last part of a line as a normal word in your page
    /endtext is used.
    To go to previous line, the command backline is used

    Note:
    backline erases the contents from the screen and again prints the prompt
    and the last lines.
    make sure to include all required details in the objects as previously printed
    data on the screen will be erased when giving the backline command
    '''
    para = ''
    lines = []
    taking = True
    clrscr()
    print(objects)
    while taking:
        line = input()
        taking = not bool(re.search(r'(^endtext$|[^/]endtext$)',line))
        backline = bool(re.search(r'(^backline$|[^/]backline$)',line))
        if backline:
            if len(lines) > 0:
                lines.pop()
            clrscr()
            print(objects)
            for line in lines:
                print(line,end='')
            continue

        #remove ' endtext' from last part of line and reprinting
        if not taking:
            line = line[ :-7]
            clrscr()
            print(objects)
            for l in lines:
                print(l,end='')
            print(line)
            
        #remove '/' from '/endtext' or '/backline'
        if line[-8: ] == '/endtext':
            line = line[ :-8] + 'endtext'
        elif line[-9: ] == '/backline':
            line = line[ :-9] + 'backline'
            
        lines.append(line + '\n')
    for line in lines:
        para += line
    #removing last character from para as it is always an extra '\n'
    para = para[:-1]
    return para

#...............End read_multiline()...............#


def read_pagefiles():
    
    PathOfPages = os.path.join(path,'Pages')
    #Read all files and folders from path\Pages
    for Element in os.listdir(PathOfPages):
        #Only consider files, exclude folders
        if os.path.isfile(os.path.join(PathOfPages,Element)):
            with open(os.path.join(PathOfPages,Element),'r') as f:
                #only consider files with atleast 4 lines
                if len(f.readlines()) < 2:
                    continue
                f.seek(0)
                title = f.readline()[:-1]
                contents = f.read()
                pages.append(Page(title,contents))
    
#...............End read_pagefiles()...............#


def write_newpage(fileobject,title,contents):
    '''This writes the page data in the file in the format...
    First line- title
    Second line onwards- contents 
    '''
    fileobject.write(title+'\n'+contents)
    return True
#...............End write_newpage()...............#


def input_newpage():
    '''Accept pages with title and contents
    and add the Page object to the list 'pages'
    '''
    clrscr()
    titleprompt = 'Enter title:\n'
    title = input(titleprompt)
    print()
    contentsprompt = '''Enter contents...
To finish typing, write endtext at the end of the line.
To go to previous line, write backline at the end of the line.'''
    print(contentsprompt)
    objects = titleprompt+title+'\n\n'+contentsprompt
    contents = read_multiline(objects)
    page_number = 1
    
    #----------Create File----------#
    file_created = False
    while not file_created:
        try:
            with open(pagepath+'/pagefile'+str(page_number).zfill(4)+'.txt','r+') as f:
                pass
        except IOError:
            with open(pagepath+'/pagefile'+str(page_number).zfill(4)+'.txt','w') as f:
                file_created = write_newpage(f,title,contents)
        page_number += 1
    #..........File Created..........#
    
    pages.append(Page(title,contents))
    print('page saved!\n')
#...............End input_newpage()...............#
    

def sort_mi(matched_indices):
    '''Sort 'matched_indices' in decending order of rank
    using Bubble Sort algorithm
    '''
    for p in range(1,len(matched_indices)):
        # p -> passes go from 1 to (n-1) for n items
        for c in range(len(matched_indices)-p):
            # c -> no. of comparisons = n-p
            rank1 = pages[matched_indices[c]].rank
            rank2 = pages[matched_indices[c+1]].rank
            if rank1 < rank2:
                matched_indices[c],matched_indices[c+1] = matched_indices[c+1],matched_indices[c]
    return matched_indices

#....................End sort_mi()....................#


def searchOperation():
    #Accept search words:
    objects = ''
    search_input = input('\nSearch: ')
    objects += 'Search: ' + search_input + '\n\n'
    word_pattern = r'[\w+-/#*@]+'
    
    ''' 'matched_indices' contains the index of every page
    within 'pages' list that has at least one match in
    the title or contents with the words in 'search_input'
    '''
    matched_indices = []
    page_i = -1
    
    ''' Take one page from 'pages' and one by one take a
    word from 'search_input'. Check how many times the word
    occurs in the page. Increment rank of that page by following
    the below algorithm and append the index of the page to
    'matched_indices' if not yet done.
    '''
    pageindex=0
    for page in pages:
        pageindex+=1
        if developer:
            print(pageindex)                            #developer edition code
            print(page.title)                           #developer edition code
        page_i += 1
        page.rank = 0
        word_rank = 10 #Latter words in search_input have lesser word_rank
        for word in re.findall(word_pattern,search_input.lower()):
            #Number of times, word appears in the page
            word_quantity = len(re.findall(re.escape(word),page.all().lower()))
            #Number of words in the page
            pagewords_quantity = len(re.findall(word_pattern,page.all()))
            
            if pagewords_quantity > 0:
                word_relevance = word_quantity / pagewords_quantity
            else:
                word_relevance = 0
            if developer:
                print('word:',word)                     #developer edition code
                print('word quantity:',word_quantity)   #developer edition code
                print('pagewords:',pagewords_quantity)  #developer edition code    
            rankplus = 0
            if word_relevance > 0:
                if word_quantity>20:
                    rankplus += word_rank + (word_relevance * 500)
                else:
                    rankplus += word_rank + (word_relevance * 25 * word_quantity)
                if word_quantity < 100:
                    rankplus += word_quantity / 5
                else:
                    rankplus += 20
                if page_i not in matched_indices:
                    matched_indices.append(page_i)
                    rankplus += 25

                if word in common_words:
                    rankplus -= rankplus*(100-common_words.index(word))/100
                    '''
                    example:-
                    rank is 50
                    
                    word = the (0)
                    rank -= 50*(100-0)/100, rank -= 50, rank =0
                    
                    word = when (50)
                    rank -= 50*(100-50)/100, rank -= 25, rank = 25
                    
                    word = us (99)
                    rank -= 50*(100-99)/100, rank -= 0.5, rank =  49.5
                    '''
            page.rank += rankplus
            
            if developer:
                print('rank +'+str(rankplus))           #developer edition code
                print()                                 #developer edition code
                
            #Decrement word_rank until 5
            if word_rank > 5:
                word_rank -= 1
    
    matched_indices = sort_mi(matched_indices)
    
    #Load pages specified by matched_indices
    print()
    load_i = 0
    for matched_i in matched_indices:
        load = pages[matched_i]
        load_i += 1
        print('[ '+str(load_i)+' ] ',end='')
        objects += '[ '+str(load_i)+' ] '
        load.display_title()
        if developer:
            print('rank:',load.rank)                      #developer edition code
        objects += load.title + '\n'
        
    if len(matched_indices) == 0:
        print('No results found for',search_input)
    else:
        while True:
            load_input_prompt = '''\nEnter the number of which page you want to load.
Enter -1 to unload the contents of pages and clear screen from previously displayed objects.
Enter 0 to exit Search:\n'''
            load_input = input(load_input_prompt)
            try:
                load_input = int(load_input)
                if load_input == 0:
                    break
                elif 0 < load_input <= len(matched_indices):
                    load = pages[matched_indices[load_input-1]]
                    print('_'*50+'\n')
                    load.display_contents()
                    print('_'*50)
                elif load_input == -1:
                    clrscr()
                    print(objects)
                else:
                    int('a')
            except ValueError:
                print('\nInvalid Input! Only enter digits specified to the left of the Page titles')

#...............End searchOperation...............#


def commonWords():
    temp = []
    try:
        with open(os.path.join(path,'common words.txt')) as f:
            for line in f.readlines():
                word = re.match(r'\w+',line.lower())
                if word is None:
                    continue
                temp.append(word.group(0))
                if len(temp) == 100:
                    break
        return temp
    except FileNotFoundError:
        print("File not found: 'common words.txt'")
        time.sleep(5)
        sys.exit()
    except:
        print("Error: Cannot read 'common words.txt'")

#...............End commonWords()...............#


def displayCommands():
    try:
        with open(os.path.join(path,'commands.txt'),'r') as commandsfile:
            print(commandsfile.read())
    except FileNotFoundError:
        print("File not found: 'commands.txt'")
    except:
        print("Error: Cannot read 'commands.txt'")
    
#...............End displayCommands()...............#
    
    
def displayHelp():
    try:
        with open(os.path.join(path,'help.txt'),'r') as helpfile:
            print(helpfile.read())
    except FileNotFoundError:
        print("File not found: 'help.txt'")
    except:
        print("Error: Cannot read 'help.txt'")
    
#.................End displayHelp()................#


def inputUser(replaceuser=False):
    global user
    global prompt
    
    while True:
        if replaceuser:
            print("Old user: '" + user + "'")
            newuser = input('Enter new username: ')
        else:
            newuser = input('Enter username: ') 
        newuser = newuser.strip()
        if re.match(r'\w+$',newuser):
            user = newuser
            prompt = user+'>>>'
            break
        else:
            print('Invalid input\nUsername must containt only word characters[a-z,A-Z,0-9,_]')
        if replaceuser:
            break

#...................End inputUser()....................#


def changePath():
    global path
    global pagepath
    
    print('Old path:',path)
    newpath = input('Enter new path: (Changing path will copy all the required files)\n')    
    newpath = os.path.join(newpath,application_name)
    try:
        PathOfPages = os.path.join(newpath,'Pages')
        if not os.path.exists(PathOfPages):
            os.makedirs(PathOfPages)
    except:
        pagepath = os.path.join(path,'Pages')
        print('Invalid path!')
    else:
        #old and new path variables
        oldPathOfProgram = os.path.join(path,os.path.basename(main_file))
        oldPathOfHelp = os.path.join(path,'help.txt')
        oldPathOfCommands = os.path.join(path,'commands.txt')
        oldPathOfWords = os.path.join(path,'common words.txt')
        oldPathOfPages = os.path.join(path,'Pages')
        path = newpath
        PathOfProgram = os.path.join(path,os.path.basename(main_file))
        PathOfHelp = os.path.join(path,'help.txt')
        PathOfCommands = os.path.join(path,'commands.txt')
        PathOfWords = os.path.join(path,'common words.txt')
        pagepath = PathOfPages
        #copy the program file, help.txt and commands.txt from old path to new path
        copyfile(oldPathOfHelp,PathOfHelp)
        copyfile(oldPathOfCommands,PathOfCommands)
        copyfile(oldPathOfWords,PathOfWords)
        copyfile(oldPathOfProgram,PathOfProgram)
        
        #Copy all pagefiles from old path to new path
        for Element in os.listdir(oldPathOfPages):
            #Only consider files, exclude folders
            oldPathOfElement = os.path.join(oldPathOfPages,Element)
            PathOfElement = os.path.join(PathOfPages,Element)
            if os.path.isfile(oldPathOfElement):
                copyfile(oldPathOfElement,PathOfElement)

        print('All files copied successfully to new path.')
        print('You can load the program from the new path.\n')

#...................End changePath()....................#


def execute(command):
    ''' Execute a command.
    Commands l and history have exception handling in case of entering those commands when history is clear
    Declare variables as global so that it can be globally changed when a command is executed.
    '''
    while True:
        global path
        global pagepath
        global user
        global prompt
        global last_command
        global history
        global developer
        
        if command == 'search':                     #1
            searchOperation()
            
        elif command == 'newpage':                  #2
            input_newpage()
            
        elif command == 'help':                     #3
            displayHelp()
            
        elif command == 'commands':                 #4
            displayCommands()
            
        elif command == 'l':                        #5
            try:
                if last_command:
                    command = last_command
                    print(prompt+last_command)
                    continue
                else:
                    1/0
            except (IndexError,ZeroDivisionError):
                print(cmd_na)
            
        elif command == 'version':                  #6
            print(version)
            
        elif command == 'path':                     #7
            print(path)
            
        elif command == 'change path':              #8
            changePath()
                
        elif command == 'change user':              #9
            inputUser(replaceuser=True)
            
        elif command == 'clear':                    #10
            clrscr()
            
        elif command == 'history':                  #11
            if len(history)>0:
                print('since',history_time)
                for c in range(len(history)):
                    print(c+1,history[c])
                print(len(history)+1,'history')
            else:
                print(commands_na)
                
        elif command == 'clear history':            #12
            history = []
            last_command = None
            print('History cleared successfully')
            
        elif command == 'clear all':                #13
            clrscr()
            history = []
            last_command = None 

        elif command == 'developer':                #14
            #Toggle between developer edition and normal mode.
            developer = not developer
            if developer:
                clrscr()
                for i in range(4):
                    print('Welcome to DEVELOPER EDITION!!!')
                    time.sleep(0.3)
                    clrscr()
                    time.sleep(0.3)
                print('Welcome to DEVELOPER EDITION!!!')
            else:
                print('You are back to normal mode...')
                
        elif command == 'exit':                     #15
            sys.exit()
           
        else:
            print("No command named '"+ command +"' found.")
            return (command + ' [invalid command]')
         
        return command
        
#...............End execute(command)...............#


#**************************************************#
#-----------------------MAIN-----------------------#
#**************************************************#

#----------Initialize----------#

application_name = 'Text File Search Engine'
version = 'Text File Search Engine 1.1.5 [python program]'

#'pages' is a list of objects of Page class
pages = []

#Check whether the program is running as a .py or .exe
#Assign name of program file accordingly
if getattr( sys, 'frozen', False ) :
        # running in a bundle (.exe)
        main_file = sys.executable
else :
        # running live (.py)
        main_file = __file__

# path is the directory were this program are stored
path = os.path.dirname(main_file)

# Create a directory for pagefiles
pagepath = os.path.join(path,'Pages')
if not os.path.exists(pagepath):
    os.mkdir(pagepath)

# 'history' is list of entered commands during the session. Can be cleared using 'clear history'
history = []

# Exact time at which program started
start_time = datetime.now()

#Following message is printed when last command entered is seeked though the history is clear.
cmd_na = 'Last command not available in history.'
commands_na = 'Previous commands not available in history.'

#Common words of english language, stored in 'common words.txt'
common_words = commonWords()

#Enter code 'developer edition' to get more features
developer = False

#Input user's name
inputUser()
clrscr()

last_command = None

read_pagefiles()

#Intro
print('Hey,',user)
print('Welcome to',application_name)
print('If this is your first time using this software, enter help on a new line to load up the help manual.')

#***************MAINLOOP***************#

while True:
    #input command
    command = input(prompt)
    
    #Remove spaces from start and end of command
    command = command.strip() 

    #ignore empty command
    if command == '':
        continue
    
    #history_time -> time at which first command was entered during the session.
    #Can be reset by giving the command 'clear history' and entering a new command.
    if len(history) == 1:
        history_time = datetime.now()
    
    #Command Execution:
    #if command is l,
    #then execute(command) returns the last valid command in history
    command = execute(command)
    
    #Add the command to history excluding a few special commands.
    if command not in ['l','clear history','clear all']:
        history.append(command)

    #Set last_command to the latest valid command in history.
    #If no valid command in history, then set last_command to None
    for i in range(len(history)-1,-1,-1):
        if history[i][-18:] == ' [invalid command]':
            last_command = None
        else:  
            last_command = history[i]
            break

#....................End MAINLOOP....................#
