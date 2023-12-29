import socket
from threading import Thread
import random

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ipAddress="127.0.0.1"
port=8000
server.bind((ipAddress,port))
server.listen()
listOfClients=[]
print("Server has been started!")
questions=[
    "What is the base 2 number system called? /n a.double numbers /n b.two-sytem /n c.binary /n d.totrition",
    "What element does the 'K' symbol represent? /n a.hydrogen /n b.potassium /n c.lithim /n d.magnesium"
    "What is the most valuable street in monopoly? /n a.Mayfair /n b.Old Kent Road /n c.Regent Street /n d.Picadilly Station"
]
answers=["c","b","a"]

def getRandomAnswer(connection):
    randomIndex=random.randint(0, len(questions)-1)
    randomQuestion=questions[randomIndex]
    randomAnswer=answers[randomIndex]
    connection.send(randomQuestion.encode("utf-8"))

def removeQuestion(index):
    questions.pop(index)
    answers.pop(index)

def clientThread(connection,address):
    score=0
    connection.send("Welcome to the Quiz! Answer the question a, b, c, or d. Good luck!".encode("utf-8"))
    index, question, answer = getRandomAnswer(connection)
    while True:
        try:
            message=connection.recv(2048).decode("utf-8")
            if message:
                if message.lower()==answer:
                    score+=1
                    connection.send(f"Correct!✅ Your score is {score}/n/n".encode("utf-8"))
                else:
                    connection.send(f"Wrong!❌ Better study up!!! Your score is still {score}/n/n".encode("utf-8"))
                removeQuestion(index)
            else:
                remove(connection)
        except:
            continue

def broadcast(message,connection):
    for client in listOfClients:
        if client!=connection:
            try:
                client.send(message.encode("utf-8"))
            except:
                remove(client)

def remove(connection):
    if connection in listOfClients:
        listOfClients.remove(connection)

while True:
    connection,address=server.accept()
    listOfClients.append(connection)
    print("ip address ",address[0]," connected!")
    newThread=Thread(target=clientThread,args=(connection,address))
    newThread.start()