# Lets import the necessary libraries

import chainlit as cl
import ollama

#Get the username

def getUsername()-> str:
    username = input('Please enter your name below\nUser name :')
    return username

@cl.on_chat_start
async def start_chat():
    cl.user_session.set("interaction",
                        [{"role": "system", "content": "You are a helpful assistant."}],)

    
    start_message = f""" Hi dear {getUsername()},\n
                         I'm your free and alternative to chat gpt, Can I help you with something?"""
                         
    msg = cl.Message(content= '')
    for token in start_chat:
            await msg.stream_token(token)
            
    await msg.send()