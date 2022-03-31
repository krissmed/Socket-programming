# Python chatbots
A simple chatbot made in Python. 
## Running
### Host/Server
To run the program you first have to start the host with the command ``python ./host.py``
The host takes in the following arguments:
- -p or --port takes an integer, that is the port. This number must be between 1 024 and 65 535, as these are the port that are open and free to use. Port from 0 to 1023 is reserved for other processes. 
- -m or --manual gives you control over the phrase the server sends out. This is also a Boolean, so when the program is called with this argument, you will be prompted to write a phrase. This will then be handled as any other premade string from the server, and you will get a response from the bots. 

### Client/Bots
To run the client, write ``python ./client.py`` in the terminal
The server has to run with the following command line arguments-i or 

- -i or --ip takes an input that is an IP address. This IP address must be the same as the one on the server. The best way of getting it to work is to input “localhost” as an argument.
- -p or --port takes an integer, that is the port. This number must be between 1 024 and 65 535, as these are the port that are open and free to use. Port from 0 to 1023 is reserved for other processes. 

You will then be asked which bot to run. NB: You can only start one instances of each bot, if you want to run more bots, start a new terminal windows and run the client again and choose another bot. 

## Closing
When the packets has been sent and the program is done, the server will close the connection and the client will close the program.

If you want to stop the process midrun, you have to close the terminal window and the program will close.

## Debug mode

Both the client and the host have a command line arguemnt ``-d``. If you run this, you will get detailed information on what's going on behind the scenes. This is made to troubleshoot potential issues that may occur. 
