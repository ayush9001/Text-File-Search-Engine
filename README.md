# Text-File-Search-Engine
A software tool, allowing you to quickly and easily search text in files on your computer. It was inspired by search engines like Google, Bing and YouTube. User inputs search query and the program goes through all files and checks if any matches found. Then it displays the titles of all files that match the searched term in order of relevance (page rank). 
--------------------------------------------------
The following files are mandatory for the program to function:-
- "searchEngine[version_number].py" is the main application file.  
- "common words.txt" is a file containing the 100 most used words in English according to wikipedia.
- "help.txt" is the help manual which can be displayed in the terminal while running the program.
- "commands.txt" is a documentation for all working commands that can be used in the program and it can be displayed in the terminal while running the program.
- Lastly, the "Pages" folder contains text files which can be retrieved from the search engine.
Note: A text file in the Pages is treated as a document to be retrieved. The first line of the file is the Title of the document while the rest of the lines are its contents.
--------------------------------------------------
User Flow:-
- Create a new user account by entering name.
- Get familiar with the program by typing "help" which will load up some basic info and commands.
- Type the "search" command to start the search operation.
- On the prompt, type the search query. The query will be broken down into words.
- Titles of relevant documents are displayed in order of relevance numbered from 1,2,3..., 1 being the most relevant. (Relevancy depends on factors such as the frequency of occurence of words matched from the query to the document.)
- On entering the number of the desired document the contents of the document will load up. 
- Entering 0 will close the search operation.
--------------------------------------------------
Cool stuff:-
- On typing the command "developer", user can turn on the developer mode! This mode allows the user to view extra details during the search operation such as page rank, relevancy, frequency of occurence of each word, etc.
- There are some interesting features such as showing command history, quick last command, changing username, changing path, etc.
--------------------------------------------------
This was my first major software project which took me around 10 days to develop. It helped me practically understand concepts of information retrieval, file handling, exception handling and object oriented programming.
