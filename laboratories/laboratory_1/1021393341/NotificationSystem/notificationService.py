import random

from handler import SMSExist, consoleExist, emailExist


def sendNotification(user,message,priority):
    # Channel posibilities
    handlerMap = { "email" : emailExist(),
                    "SMS" : SMSExist(),
                    "console" : consoleExist()
                    }
    
    failures = {"email" : random.choice([True,False]),
                    "SMS" : random.choice([True,False]),
                    "console" : random.choice([True,False])}
    
    orderedChannels = [user["preferred_channel"]] + [ch for ch in user["available_channels"] if ch != user["preferred_channel"]]

    
    
    handlers = [handlerMap[ch] for ch in orderedChannels if ch in handlerMap]

    #ordered Chain
    for i in range(len(handlers) - 1):
        handlers[i].setnext(handlers[i + 1])

    # Chain of responsability
    if handlers:
        handlers[0].handle(orderedChannels, message, priority, failures, user["name"])
    else:
        print("No hay canales válidos para notificación.")
