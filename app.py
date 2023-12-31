#requirements: pip install chainlit openai dotenv

# Run with "chainlit run app.py -w"


#ignore
# ignoreAlso ensure youre in the openai-env by typing "source openai-env/bin/activate"
# ignoreTo deactivate type "deactivate"

import chainlit as cl
import sys
import os
import time
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()



client = OpenAI(
   api_key = os.getenv('OPEN_API_KEY'),
 )

playerfile = client.files.create(
  file=open("player.txt", "rb"),
  purpose="assistants"
)

#print(f"file object\n\n{info}")
def get_hand() -> str:
    hand = ##
    return hand


tools_list = [{
    "type": "function",
    "function": {

        "name": "get_hand",
        "description": "Retrieve the values of the cards that are in your hand",
        #"parameters": {
        #    "type": "object",
        #    "properties": {
        #        "symbol": {
        #            "type": "string",
        #            "description": "The ticker symbol of the stock"
        #       }
        #    },
        #   "required": ["symbol"]
        #}
    }
}]



Card_shark = client.beta.assistants.create(
     name="Card Shark",
     instructions="You are a blackjack player. you have access to tools that when called give you your blackjack hand. after that function is called you will decide to hit, split, or whatever.",
     tools=tools_list,
     file_ids =[playerfile.id],
     model="gpt-4-1106-preview"
 )

#This way I'm not creating a new assistant every time I run the program. 
#file_assistant = client.beta.assistants.retrieve("asst_kVuy2dCgbwnLIhS2NB252cqM")

print(f"file_assistant object\n\n{Card_shark}\n\n")

thread = client.beta.threads.create()
print(f"\n\nTHREAD ID\n\n{thread.id}")

completed_statuses = {"requires_action", "cancelled", "failed", "completed", "expired"}

#continuous loop
@cl.on_message

async def main(message: cl.Message):
    
    #print(f"\n\nHERE IS THE MESSAGE OBJECT\n\n{message}")
    thread_message = client.beta.threads.messages.create(
        thread.id,
        role="user",
        #content=cl.Message.content,
        content = message.content
    )

    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=Card_shark.id,
    instructions="Please address the user as Ian."
    )


    # Now, we will poll for the status of the run until it is completed.
    completed_statuses = {"requires_action", "cancelled", "failed", "completed", "expired"}
    while True:
        # Retrieve the current state of the thread
        run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )    
        # Find the run's status in the messages
        if (run_status.status in completed_statuses):
                break

        # If not complete, wait for a short time before trying again.
        time.sleep(5)

    # At this point, the run has either completed or failed, so you can print the whole thread.
    thread_messages = client.beta.threads.messages.list(thread.id)

    
    # Iterate over the messages and print based on role
    thread_list = []
    # for message in thread_messages.data:
    #     if message.role == 'user':
    #         thread_list.append(f"User Query: {message.content[0].text.value}")
    #     elif message.role == 'assistant':
    #         thread_list.append(f"Asst Response: {message.content[0].text.value}")

    #send a response back to user
    await cl.Message(
        content=f"{thread_messages.data[0].content[0].text.value}",
    ).send()