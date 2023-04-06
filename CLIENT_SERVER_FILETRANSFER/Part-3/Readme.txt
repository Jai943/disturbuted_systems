Code is done in Python 3.9.7
__________________________________________________________________________________________________
Instructions for execution:

Note :- Since we are giving input as command line arguments using parser. Please use input as follows 

Use the following commands in the command prompt to run the code.

to start server - server.py in first terminal
>python server.py

to start client - client.py in second terminal (run it parallel when server.py is running)
>python client.py -rpc [sync/async] -add [number1,number2] -sort [number1,number2,number3,number4]
___________________________________________________________________________________________________

example for execution

in first terminal

>python server.py 

and in second terminal run client when server connection is open

For asynchronous RPC, please enter the below command

>python client.py -rpc async -add 3,4 -sort 5,6,2,1,5

For synchronous RPC, please enter below command 

>python client.py -rpc sync -add 8,6 -sort 15,6,7,1,3

___________________________________________________________________________________________________


