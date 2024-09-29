import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

client = Groq(
    api_key =os.environ["GROQ_API"]
)

# Initialize an empty list to keep track of conversation history
conversation_history = []

# ---------------  HANDLE USER INPUT AND GET RESPONSE FROM LLaMA MODEL --------------

def prompt(content):

    # Add the user's message to the conversation history
    conversation_history.append({"role": "user", "content": content})
    
    # Create the chat completion request
    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="llama-3.1-70b-versatile",
    )
    
    # Get the model's response
    response = chat_completion.choices[0].message.content
    
    # Add the model's response to the conversation history
    conversation_history.append({"role": "assistant", "content": response})
    
    return response

if __name__ == "__main__":

    flag=True
    
    while flag:
        text = input("\nPrompt: ")
        if text.lower() == "exit":  # Exit condition
            print("Conversation ended.")
            flag = False
        else:
            response = prompt(text)
            print(response)