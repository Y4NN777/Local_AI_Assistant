# Lets import the necessary libraries

import chainlit as cl
import ollama



# start_chat() function used to start a chat when the user runs the app
@cl.on_chat_start
async def start_chat():
    
    
    # Setting the interaction history
    cl.user_session.set("interaction",
                        [{"role": "system", "content": "You are a helpful assistant."}],)

    
    # The stream system's intro message tokenizing for the requests
    
    start_message = f""" Hi dear Y4NN ,\n
                         I'm your free and alternative to chat gpt, Can I help you with something?"""
                         
    
    msg = cl.Message(content= "")
    for token in start_chat:
            await msg.stream_token(token)
            
    await msg.send()
    
    
#tool() function that defines how the tool handle interaction
@cl.step(type="tool")
async def tool(input_message, image=None):
    
    # Getting the interaction object
    interaction = cl.user_session.get("interaction")
    
    # Add the current user input to interaction
    if image:
        interaction.append({ 
            "role": "user",
            "content": input_message,
            "images": image
            })
        
    else:
        interaction.append({"role":"user",
                            "content": input_message})
        
    
    # Retrieve response to the user prompt from the model
    response = await ollama.chat(model="llama3.2-vision",
                            messages = interaction)
    
    # Add the response to the interaction history
    interaction.append({
        "role":"assistant",
        "content": response.message.content
    })
    
    return response

# Defining the main function
@cl.on_message
async def main(message: cl.Message):
    
    # Check if the prompt contains image
    images = [file for file in message.elements if "image" in file.mime]

    if images:
        # invoke the lm interaction tool with the prompt with the image
        tool_res = await tool(message.content, [i.path for i in images])
    else:
        
        # invoke the llm interaction tool with the prompt with the image
        tool_res = await tool(message.content)
        
    
    msg = cl.Message(content="")

        # Streaming the llm response
    for token in tool_res.message.content:
        await msg.stream_token(token)
        
    await msg.send()
    
        
    