___________________________________________________________________________________________________
Code is done in Python 3.9.7
___________________________________________________________________________________________________
We have to import some libraries to python before compiling

to import libraries on server side:
>pip install pyftpdlib

to import libraries on server side:
>pip install ftpsync 
___________________________________________________________________
Instructions for execution:

Use the following commands in the command prompt to run the code.

to start server - server.py
>python server.py

to start client - client.py in second terminal (run it parallel when server.py is running)
>python client.py
___________________________________________________________________________________________________

Now that we established sync using bi-directional synchronizer, we can try all file operations and it will be synced between sync folders of sync and client

Server-data/server-sync

Client-data/client-sync


we establised a sleep time of 4 secs ,,, it might take 4-5 secs to sync 


