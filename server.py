import socket
import re
import json
import datetime

ip_voted = dict()
email_password = dict()
votes = dict()
Vote_start = datetime.datetime(2021, 5, 3, 7, 50, 0).strftime("%H:%M:%p")
Vote_end = datetime.datetime(2021, 5, 3, 20, 20, 0).strftime("%H:%M:%p")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating a socket
print("Server Socket is starting...")

server.bind((socket.gethostname(), 5545))  # binding the socket with a port number and ip address
server.listen(3)
print("waiting for the connection")

# loop function is used to accept the connection of many clients again and again

def check_email(email):
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email): return(False, "Invalid Email")
    if email.split('@')[1] != 'ashoka.edu.in': return(False, "Invalid Ashoak Email")
    return(True, "Valid Email")


#saving all emails, passwords, votes and ip address of each canddidat's voting
try:
    with open('email_password.json',"r") as f:
        email_password = json.load(f)
    with open('ip_voted.json',"r") as f:
        ip_voted = json.load(f)
    with open('votes.json',"r") as f:
        votes = json.load(f)
except FileNotFoundError:
    pass   


#sarting voting
def start_voting(email, address):

    if (str(address) in ip_voted):
        
        conn.send("You have already voted ".encode())
        return False

    message = f"""
    Welcome {email} to Ashoka Voting System
    Here are the candidates:
    (Respond with the number of the candidate)
    1. Rakesh
    2. Deepak
    3. Mahesh
    4. Kuldeep
    """
    conn.send(message.encode())

    recv_data = conn.recv(1024).decode()

    if int(recv_data) < 1 or int(recv_data) > 4:
        conn.send("Invalid Candidate Number".encode())
        return False

    votes[recv_data]["votes"] += 1
    ip_voted[str(address)] = True

    # Save the data to the file
    with open('votes.json',"w") as f:
        json.dump(votes, f, indent=4)
    with open('ip_voted.json',"w") as f:
        json.dump(ip_voted, f, indent=4)

    return True


Connected = True
while Connected:
    (conn, address_port) = server.accept()
    address = address_port[0]
    userPrompt =  f"""
    Welcome! You can participant in the vote by presenting your password.
    Reply with a ”1” if you want to participate now; with a ”2” if you want to see the results; and with ”3” other wise.
    Put your choice: 1 | 2 | 3
    PS: You can only vote from {Vote_start} to {Vote_end} and can't see the result between this time.
    """
    curr_time = datetime.datetime.now().strftime("%H:%M:%p")
    conn.send(userPrompt.encode())
    choice = int(conn.recv(1024).decode())

    if choice == 1:

        conn.send("Enter your email: ".encode())
        email = conn.recv(1024).decode()
        print(email)
        
        #validation of email
        email_validation_result = check_email(email)
        if not email_validation_result[0]:
            conn.send(f"{email_validation_result[1]}\n Closing Connection".encode())
            conn.close()
            continue
        
        # check if email already exsists
        if email in email_password:
            conn.send(f"Please Enter the password".encode())
            password = conn.recv(1024).decode()

            if password != email_password[email]:
                conn.send(f"Invalid Password\n Closing Connection".encode())
                conn.close()
                continue
            
            # Start Voting
            result = start_voting(email=email, address=address)
            if result:
                message = f"Thank you for participating. Your response is registered against your IP address - {str(address)}"
                conn.send(message.encode())
                conn.close()
                continue
            else:
                conn.close()
                continue

            
        else:
            # if email doesn't excists
            # Generate a random password
            # Store the email and password in a dictionary
            # Save the dictionary in a file
            import random
            import string
            password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
            email_password[email] = password
            with open('email_password.json',"w") as f:
                json.dump(email_password, f, indent=4)
            conn.send(f"Password Generated: {password}\n Please Store this password in a secure place.\n Closing Connection".encode())
            conn.close()
            continue               

    if choice == 3:
        conn.send("connection is closed".encode())
        conn.close()

    if choice == 2:
        conn.send("Enter your email: ".encode())
        email = conn.recv(1024).decode()
        print(email)

        email_validation_result = check_email(email)
        if not email_validation_result[0]:
            conn.send(f"{email_validation_result[1]}\n Closing Connection".encode())
            conn.close()
            continue
        
        # check if email already excists
        if email in email_password:
            conn.send(f"Please Enter the password".encode())
            password = conn.recv(1024).decode()

            if (password != email_password[email]) or Vote_start <= curr_time <= Vote_end:
                conn.send(f"Error\n Closing Connection".encode())
                conn.close()
                continue
            
            else:
                 # Presents the voting results
                 Results = f"""
                 The results are:
                 1. Rakesh: {votes[str(1)]["votes"]}
                 2. Deepak: {votes[str(2)]["votes"]}
                 3. Mahesh: {votes[str(3)]["votes"]}
                 4. Kuldeep: {votes[str(4)]["votes"]}
                 """
                 conn.send(f"{Results}\n The number of responses each candidate has received." .encode())
                 conn.close()
                 
                 