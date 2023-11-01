print("Starting script...")  # Debugging print statement
import sys
import time
from dotenv import load_dotenv
import pickle
import os

print("Imported required modules...")  # Debugging print statement

# Load environment variables
load_dotenv()

api_key = os.getenv('OPEN_API_KEY')
# TODO: Consider passing this API key where needed or set it in the ChatOpenAI.

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

print("Loaded environment variables and models...")  # Debugging print statement



# Define shared context here:
all_header = """
Roll for Shoes: Cyberpunk Edition

In the neon-soaked streets of 2020, amidst the towering megacorps and digital shadows, players navigate the matrix of intrigue and tech.

1. State your action and roll a number of D6s, based on the relevant skill's level.
2. If your roll's sum is higher than the challenge or opponent's roll, your action succeeds.
5. Gain 1 XP for failed attempts. The neon world is harsh, but every failure is a lesson.
6. Use XP to make one die a 6, but only at the GMs allowance to further the story. 
Characters evolve based on choices, leading to unexpected talents in this cybernetic sprawl.
"""
#class SummarizationAgent:
#    def __init__(self):
#        self.chat = ChatOpenAI(streaming=True,
#                               callbacks=[StreamingStdOutCallbackHandler()],
#                               temperature=0.7,
#                               model="gpt-4",)

#    def summarize(self, conversation):
#        summary_prompt = f"Please provide a truncation of the following conversation: {conversation}. Ensure that the truncation has the same style and feel as the content, so as not to feel like a summary."
#        resp = self.chat([HumanMessage(content=summary_prompt)])
#        return resp.content



class Agent:
    def __init__(self, name, prompt, history_file=None): #param text_filename="conversation.txt"
        print(f"Initializing agent: {name}")  # Debugging print statement

        self.name = name
        self.history_file = history_file
        self.text_filename = text_filename
        self.chat = ChatOpenAI(streaming=True,
                               callbacks=[StreamingStdOutCallbackHandler()],
                               temperature=1.0,
                               model="gpt-4",)
        self.message_history = self.load_conversation() if history_file else []
        self.message_history.insert(0, SystemMessage(content=prompt))
        print(f"Agent {name} initialized.")  # Debugging print statement


    def message(self, message):
        self.message_history.append(HumanMessage(content=message))
        resp = self.chat(self.message_history)
        print("\n")
        self.message_history.append(resp)
        self.save_conversation()
        save_to_text_file(self.text_filename, [self])
        return resp

    def save_conversation(self):
        if not self.history_file:
            return
        try:
            with open(self.history_file, 'wb') as f:
                pickle.dump(self.message_history, f)
            #print(f"Conversation saved to {self.history_file}")
        except Exception as e:
            print(f"Error saving conversation: {e}")

    def load_conversation(self):
        if not self.history_file or not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return []
        
    def word_count(self):
        return sum(len(message.content.split()) for message in self.message_history)
    
def save_to_text_file(filename):
    with open(filename, 'w') as f:
        for agent in [gm, player]:
            for message in agent.message_history:
                f.write(f"{agent.name}: {message.content}\n")


TARGET_WORD_COUNT = 50000 
ENDING_MESSAGE = "Ok, it's late, and we have work tomorrow. Let's stop it here and continue next weekend?"

#summarizer = SummarizationAgent()

print("Defined shared context and classes...")  # Debugging print statement

def initialize_agents():
    print("Initializing agents...")  # Debugging print statement

    # Delete history files before creating agents
    gm_history_path = "gm_history.pkl"
    player_history_path = "player_history.pkl"
    
    if os.path.exists(gm_history_path):
        os.remove(gm_history_path)
    
    if os.path.exists(player_history_path):
        os.remove(player_history_path)
        

    with open("gm_header.txt") as f:
        gm_header = all_header + f.read()
        gm = Agent("GM", gm_header, gm_history_path)

    with open("player_header.txt") as f:
        player_header = all_header + f.read()
        player = Agent("Player", player_header, player_history_path)
    
    print("Agents initialized.")  # Debugging print statement

    return gm, player



def run_conversation(session_word_limit, gm, player):
    print("Running conversation...")  # Debugging print statement

    message = "What is your character's name, class, and what do they look like?"
    current_agent = player
    session_word_count = 0
    
    try:
        while session_word_count < session_word_limit:
            print(f"{current_agent.name}:")
            print(f"TOTAL WORD COUNT {gm.word_count + player.word_count}")
            print(f"SESSION WORD COUNT {session_word_count}")

            resp = current_agent.message(message)
            message = resp.content
            new_words = len(message.split())
            session_word_count += new_words

            # Check if we're reaching the session or total word limit
            if session_word_count >= session_word_limit or (gm.word_count + player.word_count) >= TARGET_WORD_COUNT:
                print("Word limit reached. Ending session.")
                break

            if current_agent == player:
                current_agent = gm
            else:
                current_agent = player
        
    except KeyboardInterrupt:
        print("Chat session interrupted.")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("Conversation ended.")  # Debugging print statement
