#TODO finish tutorial video and learn how to change type from string to integer 
#(where needed) in response automatically 
#https://www.youtube.com/watch?v=UVn2NroKQCw

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPEN_API_KEY')


chat_llm = ChatOpenAI(temperature=0.0)

template_string = """You are a master branding consultant who specializes in naming brands. 
You come up with catchy and memorable brand names.Take the brand description below delimited by triple backticks and use it to create the name for a brand.
brand description: '''{brand_description}'''

then based on the description and you hot new brand name give the brand a score 1-10 for how likely it is to succeed

{format_instructions}
"""
#format instructions are below and they will insert what used to be 
# "format the output as JSON with the following keys
# brand_name
# likelihood_of_sucess

#first way of doing things. not as good. 
#prompt_template = ChatPromptTemplate.from_template(template=template_string)
#prompt_template.messages[0].prompt
#branding_messages = prompt_template.format_messages( brand_description = "a cool brand aimed at sneakerheads")
#consultant_response = chat_llm(branding_messages)
#print(consultant_response.content) #Will be a string but is JSON hopefully
#print(branding_messages)

brand_name_schema = ResponseSchema(name='brand_name',
                                   description='This is the name of the brand')
likelihood_of_sucess_schema = ResponseSchema(name='likelihood_of_sucess',
                                             description='This is an integer score between 1-10')

response_schemas = [brand_name_schema,
                    likelihood_of_sucess_schema]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

format_instructions = output_parser.get_format_instructions()
#print(f"format instructions {format_instructions}")

prompt = ChatPromptTemplate.from_template(template=template_string)

messages = prompt.format_messages(brand_description='an AI innovation community marketed toward educators',
                                format_instructions=format_instructions)

response = chat_llm(messages)
print(response)

response_as_dict = output_parser.parse(response.content)
print(response_as_dict)


print(response_as_dict['brand_name'])