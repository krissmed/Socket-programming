import argparse
import socket
import threading
import random
import time


parse = argparse.ArgumentParser (description="Host for the chat")  # Create the parser
parse.add_argument("-d", "--debug", help = "Prints debug messages", action = "store_true")  # Add the arguments
parse.add_argument("-p", "--port", help = "Port of the server", default = "", required = True)  # Add the port argument
parse.add_argument("-m", "--manual", help = "Option to manually input", default = "", action = "store_true")  # Add the arguments
args = vars(parse.parse_args())  # Parse the arguments


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
         "dance",
         "sing",
         "jump",
         "fly",
         "swim",
         ]  # List of verbs


HEADER = 1024  # Max size of the message
PORT = args["port"]  # Port of the server 
SERVER = "0.0.0.0"  # Server IP
ADDR = (SERVER, int(PORT))  # Create the address
FORMAT = "utf-8"  # Format of the message
DISCONNECT_MESSAGE = "!DISCONNECT"  # Message to disconnect
connections = []  # List of connections
users = []  # List of users


def handle_client(conn):  # Handle the client
    username = check_username(conn)  # Check if the username is already in use
    print(f"{username.capitalize()} joined the chat")  # Print that the user has successfully joined the chat
    msg = (f"{username.capitalize()}: {receive(conn, username)}")  # Receive the response
    print(msg)  # Print the response
    broadcast_to_clients(msg, conn)  # Broadcast the response to all clients except the one who sent the message


def choose_action():
    action = random.choice(verbs)  # Choose a random verb
    debug(f"Action chosen: {action}")  # Print the verb
    return action


def format_initial_phrase(action):  # Automatically format the initial phrase
    phrase = f"Would you guys like to {action} with me"  # Format the initial phrase
    debug(f"Initial phrase: {phrase}")  # Log the initial phrase
    return phrase


def manually_format_initial_phrase():  # Manually format the initial phrase 
    print("Write a phrase to start the chat")  # Print the message
    phrase = input("Host: ")  # Get the input
    return phrase


def send(msg, conn):  # Send the message to the client
    conn.send(msg.encode())  # Encode the message
    debug(f"Sent \"{msg}\" with length of {len(msg)} to client {conn}")  # Log the message
    return


def receive(conn, username):  # Receive the message from the client
    msg = conn.recv(HEADER).decode(FORMAT)  # Receive the message
    debug(f"Recieved message from {username} with length of {len(msg)}")  # Log the message
    if msg == DISCONNECT_MESSAGE:  # Check if the message is the disconnect message
        disconnect(conn, username)  # Disconnect the client
        return
    elif len(msg) == 0:  # Check if the message is empty
        print("500 Internal Server Error")  # Print the error
        disconnect(conn, username)  # Disconnect the client
        return 
    elif len(msg) > 1024:  # Check if the message is too long
        print(f"Message is to large to process. Max capacity is {HEADER} bytes")  # Print the error
        disconnect(conn, username)  # Disconnect the client
        return
    return msg


def disconnect(conn, username):  # Disconnect the client
    print("Client disconnected")  # Print the message
    print(username)  # Print the username
    debug(f"List of active users before removal {users}, {username}")  # Log the list of users
    users.remove(username)  # Remove the username from the list
    debug(f"Remaining users: {users}")  # Log the remaining users
    conn.close()  # Close the connection
    connections.remove(conn)  # Remove the connection from the list
    debug(f"{len(connections)} active connections")  # Log the number of active connections


def check_username(conn):  # Check if the username is already in use
    debug(f"Checking username for client")  # Log that the username is being checked
    username = receive(conn, "")  # Receive the username
    debug(f"Checking if \"{username}\" is already in list \"{users}\"")  # Log checking if the username is already in users[]
    if str(username).lower() in users:  # Check if the username is already in use
        users.append(str(username).lower())  # Add the username to the list
        send("!USERNAME_ALREADY_TAKEN", conn)  # Send the message to the client
        disconnect(conn, username)  # Disconnect the client
        debug(f"Username {username} is already in use. Try again with another username")  # Log the error
    else:  # Username is not in use
        debug(f"Username \"{username}\" is not in use")  # Log the username is not in use
        users.append(str(username).lower())  # Add the username to the list
        send("!USERNAME_OK", conn)  # Send the message to the client
    return username


def listen():  # Listen for connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create the socket
    debug(f"Server is start at IP [{SERVER}] on PORT [{PORT}]")  # Log the server
    server.bind(ADDR)  # Bind the socket to the address
    server.listen()  # Listen for connections
    print(f"[{SERVER}] Host is listening ")  # Print the message
    while len(connections) < 4:  # Check if there are less than 4 connections
        print("Waiting for connections")  # Print the message
        conn, addr = server.accept()  # Accept the connection
        debug(f"connection from {addr} has been established")  # Log the connection
        connections.append(conn)  # Add the connection to the list
        thread = threading.Thread(target=handle_client, args=(conn))  # Create a thread to handle the client
        thread.start()  # Start the thread
        debug(f"{threading.activeCount() - 1} acive connections")  # Log the number of active connections
    debug(f"The chatroom is now full. Starting the chat")  # Log the chatroom is full
    initialize_chat()  # Initialize the chat
    time.sleep(1)  # Sleep for 1 second
    print("Host: Thank you for participating in the chat. Have a nice day! :)")  # Print the message


def initialize_chat():  # Initialize the chat
    if args["manual"]:  # Check if the user wants to manually format the initial phrase
        debug("Manual mode is enabled")  # Log that the user wants to manually format the initial phrase
        initial_phrase = manually_format_initial_phrase()  # Get the initial phrase
    else:  # The user wants to automatically format the initial phrase
        debug("Manual mode is disabled")  # Log that the user wants to automatically format the initial phrase
        action = choose_action()  # Choose a random verb
        initial_phrase = format_initial_phrase(action)  # Format the initial phrase
    broadcast_to_all(initial_phrase)  # Broadcast the initial phrase to all clients


def broadcast_to_all(msg):  # Broadcast the message to all clients
    for conn in connections:  # For each connection
        debug(f"Sending {msg} to {conn}")  # Log the message and connection
        time.sleep(2)  # Sleep for 2 seconds
        send(msg, conn)  # Send the message to the client
    return


def broadcast_to_clients(msg, conn):  # Broadcast the message to all clients except the one who sent the message
    for connection in connections:  # For each connection
        if connection != conn:  # Check if the connection is not the one who sent the message
            connection.send(msg.encode())  # Send the message to the client
    return


def debug(string):  # Print the debug message
    if args["debug"]:  # Check if the user wants to enable debug mode
        print(f"[DEBUG] {string}")


debug(f"[{ADDR}] The host is starting")
listen()
