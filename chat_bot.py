from langgraph.graph import StateGraph ,START ,END
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage , HumanMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

import os
from requests import Response
load_dotenv()
print(os.getenv("GROQ_API_KEY"))


#llm initilization
llm = ChatGroq(
    model="groq/compound",
    temperature=0
)

# state
class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

# chatnode
def chatMessage(state: ChatState):

    message = state['messages']

    response = llm.invoke(message)

    return {'messages':[response]}
# graph

checkpointer = MemorySaver()

graph = StateGraph(ChatState)

graph.add_node('chatMessage' , chatMessage)

graph.add_edge(START , 'chatMessage')
graph.add_edge('chatMessage',END)

workflow = graph.compile(checkpointer=checkpointer)

stream = workflow.stream(
    {'messages': [HumanMessage(content='What is cricket')]},
    config = {'configurable' : {'threadid' : 'thread-1'}},
    stream_mode='messages'
)
print(type(stream))

initial_state ={
    'messages' : [HumanMessage(content='what is the capital of India')]
}
#result= workflow.invoke(initial_state)['messages'][-1].content
def main ():
    thread_id = '1'
    while True:
    
        user_message = input('Type here:')

        print(user_message)

        if user_message.strip().lower() in ['exit' , 'bye' ,'quit']:
            break

        config = {'configurable': {'thread_id': thread_id}}   
        response = workflow.invoke({'messages': [HumanMessage(content = user_message)]} , config  = config)

        print('AI:',response['messages'][-1].content)
    #print(result)

if __name__ == "__main__":
    main()
