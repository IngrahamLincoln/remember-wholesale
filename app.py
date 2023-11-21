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
info = client.files.create(
  file=open("info.txt", "rb"),
  purpose="assistants"
)
prag = client.files.create(
  file=open("prag.txt", "rb"),
  purpose="assistants"
)
hist = client.files.create(
  file=open("history.json", "rb"),
  purpose="assistants"
)
#print(f"file object\n\n{info}")

# file_assistant = client.beta.assistants.create(
#     name="File Assistant",
#     instructions="you have access to files to answer questions about them.",
#     tools=[{"type": "retrieval"}],
#     file_ids =[info.id, prag.id, hist.id],
#     model="gpt-4-1106-preview"
# )
file_assistant = client.beta.assistants.retrieve("asst_6zQYOHIKKxI2ocqdzOb7AweF")

#print(f"file_assistant object\n\n{file_assistant}\n\n")

thread = client.beta.threads.create()
print(f"\n\nTHREAD ID\n\n{thread.id}")

completed_statuses = {"requires_action", "cancelled", "failed", "completed", "expired"}

#continuous loop
@cl.on_message

async def main(message: cl.Message):
    #Your logic will be here. 
    #print(f"\n\nHERE IS THE MESSAGE OBJECT\n\n{message}")
    thread_message = client.beta.threads.messages.create(
        thread.id,
        role="user",
        #content=cl.Message.content,
        content = message
    )

    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=file_assistant.id,
    instructions="Please address the user as Ian. The user has a premium account."
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