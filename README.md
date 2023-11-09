# remember-wholesale

![Human sitting across from robot and an external brain](./images/Screenshot%202023-10-24%20at%2010.14.37%20AM.png)

pip install transformers - for the tokenizer

I'm reminded of the short story We Can Remember It for You Wholesale by Phillip K. Dick.  

The goal for this project is a dialogue environment between a user and an agent. The agent should be able to read the users input and lnow if it has any relavent memories. A second agent will oversee the conversation and periodically make summaries in order to store those summaries in a vector database. This agent, or combination of agents will also search this database when it is appropriate to refer to past conversations. The goal is to begin building a memory in order to add some nuance and complexity to an agents interactions. 

User:
- talk to agent like you would in vanilla chat

agent:
- has an external memory, short term memory is long-form, long term memory is short form. 
- "thinks" before it speaks. its output to the user should be informed by recent context, memory (long/short), as well as a compressed version of the broader context of the conversation. 
- ideally the memory should be able to serve the same purpose as human memory,in which problem solving for tasks is informed by earlier experiences with solving problems, regardless of context. 
- for example, when i try to code something, the agent may look at my code and see that it's end result would help me to reach a previously stated goal, or perhaps ask a question about a  philosophical, or literary themed conversation, and make suggestions about the code. 

- after this i would be interested in modularly adding functionality through those memories allowing the llm to perform tasks with my data/files/etc but informed by its pre-trained dataset. LLMs are functional, but they don't know my preferences or workflows. 

uses:
- personal assistant
- tutor
- programming assistant
 a memory could be a program, or function. in other words it could, over time, level up a skill tree of abilities that are unique to me. once ive trained it one a task, it stores that workflow and then is able to relagate the details to memory.
- The LLM should be able to help me create larger programs because actively it helps me build them in a modular way. this way it's context window remains clear of large amounts of code, but it can find those sections of code in memory when it needs to dive into the details...
- this way i could keep track of all the new python packages that come up and be loading the ones I want into its memory...



Possible applications:

Spinning up memories for an NPC
Personal assistant with temporal permenency.
Vectorizing an entire syllabus or textbook in order to maximize learning for specific courses. 



## Things I need to learn more about:

- data gathering/preparation
- Embeddings
- Vector databases
- Langchain
- SQl
- Semantic search
- Open source LLMs

- Other Relavent python packages and libraries.

## Intended outcomes.

- familiarity with vector databases, langchain, system prompting. 
- More intuition regarding databases, API calls, chain engineering, etc.


## Tentative plan. 
Week 1 Oct 22 - 28

- Be a sponge. Youtube videos, READMEs, podcasts, blogs, repositories. dive in and familiarize myself with what is out there and what is being done with it. 
- I'll try to document what are the most relavent sources of data. 
- Pseudocode draft

Week 2 Oct 29 - Nov 4th

- Meet with Magda on 31st - discuss her workflow, and code. Ask questions, etc. 
- Begin writing code - aim for MVP

At this point I'll be more knowledgable, I will update this plan with where I'd like the project to take me. 

Week 3 NOV 5th - 11th

- TBD
Nov 1 2023
- added MVP
- initially identified 3 classes that are needed. Agent, memory node, and conversation. 
- goal for next time. use SPR to write system prompt that allows a 


ideas, 
- memory methods that include system prompts.. one for SPR condensing, one for SPR unzipping. in order to get LLM response back and 

- added tokenizer 
- 




dump all output into a funning file, chunk by 4000 (arbitrary) tokens, then loop through each and search. this is intesnsive but will be better at semantically calling up memories via an embedding. 



list of json objects
serialization and deserialization
[{},{"user":"system", message"}]