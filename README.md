# Simple Chat Application


This is a simple chat application that allows users to register, log in, view contacts, add contacts, connect to other users, and exchange messages in real-time.

## Features
- User Registration: Users can register with a unique username, password, and IP address.
- User Authentication: Registered users can log in using their username and password.
- Contacts Management: Users can view their contacts list and add new contacts.
- Chat Messaging: Users can connect to other users and exchange messages in real-time.
- Server Setup: Users can set up their machine as a server to allow other users to connect to them.
  
## Requirements
- Python 3.x
- SQLite3

## Usage
Register: Choose option 1 to register as a new user. Enter your desired username, password, and IP address.

Log In: Choose option 2 to log in as an existing user. Enter your username and password.

Exit: Choose option 3 to exit the program.

View Contacts: After logging in, choose option 1 to view your contacts list.

Add Contact: Choose option 2 to add a new contact. Enter the contact's username, IP address, and port number.

Connect to User: Choose option 3 to connect to another user. Enter the username of the user you want to connect to. The user must be in your contact.

Set Up as Server: Choose option 4 to set up your machine as a server. This allows other users to connect to you.

Log Out: Choose option 5 to log out.


## Databases
Each user will have their own database that stores all messages that they have sent or received. When first connecting to a user, the chat history with that user will be printed. The database naming scheme is {username}.db. 

There is a user database that stores all the usernames, passwords, and ip addresses of users. It is checked against when a user tries to log in.

There is a contacts database that holds all contacts of all users. Users can add contacts to the database and the option "view contacts" will allow users to display all their contacts.


## Documentation
![image](https://github.com/Erichen294/P2P-System/assets/98416392/2e8d3c8e-3cf8-45b1-8e40-7ac6d182de82)
![image](https://github.com/Erichen294/P2P-System/assets/98416392/f0a9ef81-40e6-4733-9105-d139181a161d)
