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
    
    @cl.step(type="tool")
    async def tool_step(input_message, image=None):
        
        interaction = cl.user_session.get("interaction")
        
        if image:
            interaction.append({ 
                "role": "user",
                "content": input_message,
                "images": image
                })
            
        else:
            interaction.append({"role":"user",
                                "content": input_message})
            
        
        response = ollama.chat(model="llama3.2-vision",
                               messages = interaction)
        
        interaction.append({
            "role":"assistant",
            "content": response.message.content
        })
        
        return response
        
        