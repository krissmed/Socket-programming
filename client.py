import socket
import os
import random
from jinja2 import Undefined
import argparse

# Response messages
responses = ["I love {verb}ing! Let's do it :)",
             "I would love to {verb}!",
             "That's great idea! Let's {verb}!",
             "I'm glad you want to {verb}! Let's do it today :)",
             "Excellent! Let's {verb}!",
             "Really? Let's {verb}!",
             "That's great! Let's {verb}!",
             ]

no_response = ["I'm sorry, I don't understand what you mean...",
               "Really? I don't understand what you mean...",
               "Oh, I'm sorry, I don't understand what you mean...",
               "Are you sure you're not trying to make me say something stupid?",
               "Really? Are you sure you're not trying to make me say something stupid?",
               "That's a bit too complicated for me...",
               "Please try to make me understand what you mean...",
               "What do you mean by that?",
               "Can you repeat that?",
               "Excuse me?",
               "My brain is not working...",
               ]

verbs = ["hug",
         "walk",
         "run",
         "fish",
         "count",
         "shop",
         "buy",
         "sell",
         "eat",
         "drink",
         "sleep",
         "play",
         "talk",
         ]

parse = argparse.ArgumentParser(description="Host for the chat")  # Create the parser
parse.add_argument("-d", "--debug", help="Prints debug messages", action="store_true")  # Add the debug argument
parse.add_argument("-i", "--ip", help="IP adress of the server", default="", required=True)  # Add the ip argument
parse.add_argument("-p", "--port", help="Port of the server", default="", required=True)  # Add the port argument
args = vars(parse.parse_args())  # Get arguments from command line and set variables accordingly

HEADER = 1024  # Max length of the message
PORT = vars["port"]  # Port
FORMAT = "utf-8"  # Format of the messages
DISCONNECT_MESSAGE = "!DISCONNECT"  # Message that disconnects the client
SERVER = vars["ip"]  # The IP address of the server
ADDR = (SERVER, int(PORT))  # IP and Port number of the server


def bot(username):  # Create the bots
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create the socket
    client.connect(ADDR)  # Connect to the server
    send(username, client)  # Send the username to the server
    receive(client)  # Receive the response from the server
    print(f"You joined the chatroom")  # Print the message that the client joined the chatroom
    msgRecv = receive(client)  # Receive the message from the server
    verb = find_verb(msgRecv)  # Find the verb in the message
    phrase = response(verb)  # Formats a response
    send(phrase, client)  # Send the response to the server
    for conn in range(4):  # Recieves the other clients responses
        msgRecv = receive(client)
        print(msgRecv)  # Print the other clients responses
    disconnect(client)  # Disconnects the client


def send(msg, client):  # Send a message to the server
    message = msg.encode()  # Encodee the message
    debug(f"Sending message \"{msg}\" with length {len(msg)}")  # Log the message that is sent
    client.send(message)  # Send the message to the server
    debug("\"{msg}\" sent to server")  # Log that the message is sent


def disconnect(client):  # Disconnects the client
    send(DISCONNECT_MESSAGE, client)  # Send the disconnect message to the server
    client.close()  # Close the client
    debug(f"Client disconnected")  # Log that the client disconnected
    os._exit(1)  # Exit the program


def find_verb(recvMsg):  # Finds the verb in the message from the server
    debug(f"Message received: \"{recvMsg}\"")  # Log the message that was received
    recievedMsg = recvMsg  # Set the message to a variable
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''  # All punctionation characters
    for char in recievedMsg:  # Remove all punctionation characters from the message
        if char in punctuation:
            recievedMsg = recievedMsg.replace(char, "")
            debug(f"Removed {char} from string")  # Log that the character was removed
    debug(f"Removed all punctuation. New string is \"{recievedMsg}\"")  # Log the new string
    recievedMsg = recievedMsg.lower()  # Convert the message to lowercase
    debug(f"Message before split: {recievedMsg}")  # Log the message before the message is split
    verb = Undefined  # Initialize the verb variable
    recievedMsg = recievedMsg.split(" ")  # Split the message into a list
    for i in range(len(recievedMsg)):
        if recievedMsg[i] in verbs:  # If the word is in the verbs list
            verb = recievedMsg[i]  # Set the verb to the word
            debug(f"Found one verb in the message: {verb}")  # Log the verb that was found
    return verb


def receive(client):  # Receive a message from the server
    msgRecv = client.recv(2048).decode(FORMAT)  # Receive the message from the server
    if str(msgRecv) == "!USERNAME_ALREADY_TAKEN":  # If the username is already taken
        print("This user already active. Try another one")  # Print the message that the username is already taken
        disconnect(client)  # Disconnect the client
    debug(f"Revieved message {msgRecv}")  # Log the message that was received
    return msgRecv  # Return the message that was received


def response(verb):  # Formats a response
    response = ""  # Initialize the response variable
    if verb == Undefined:  # If the verb is undefined
        debug("No verb was found in the message. Sending default response")  # Log that the verb was not found
        response = random.choice(no_response)  # Choose a random response from the no_response list
        response = response.format(verb=verb)  # Format the response
        debug(f"Responding with {response}")  # Log the response
    else:  # If the verb is defined
        debug(f"One verb was found({verb}). Sending response")  # Log that the verb was found
        response = random.choice(response)  # Choose a random response from the response list
        response = response.format(verb=verb)  # Format the response
        debug(f"Responding with {response}")  # Log the response
    print(f"Me: \x1B[3m{response}\x1B[0m")  # Print the response
    return(response)  # Return the response


def setup():  # Setup the client. This is called when the client is started
    print("Choose which bot to start:")
    print("1: Alice")
    print("2: Bob")
    print("3: Eric")
    print("4: Jonathan")
    bot = input("Choose bot: ")
    if(str(bot) == "1"): # If the input is 1 then start Alice
        debug(f"{bot} is input. Alice is starting")
        bot("Alice")
    elif(str(bot) == "2"): # If the input is 2 then start Bob
        debug(f"{bot} is input. Bob is starting")
        bot("Bob")
    elif(str(bot) == "3"): # If the input is 3 then start Eric
        debug(f"{bot} is input. Eric is starting")
        bot("Eric")
    elif(str(bot) == "4"): # If the input is 4 then start Jonathan
        debug(f"{bot} is input. Jonathan is starting")
        bot("Jonathan")
    else:
        print("You have to choose a bot. Type a number between 1 and 4")
        debug(f"{bot} is input. No bot is starting")
        setup()
        os.system("CLS")


def debug(string):  # If -d is passed as an argument, this is used print debug messages
    if args["debug"]:
        print(f"[DEBUG] {string}")

debug(f"Maxium message length is {HEADER}")  # Log the maxium message length
setup()
