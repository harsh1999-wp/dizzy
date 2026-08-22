from curses import tigetflag
from chat_bot import workflow
import streamlit as st 
st.title("AI Chatbot")
import streamlit as st

st.title("AI Chatbot")

from langchain_core.messages import HumanMessage

CONFIG = {
    'configurable': {
    'thread_id': 'thread-1'
    }
}

if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []
st.write("LLM loaded")
for messages in st.session_state['messages_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])


user_input = st.chat_input('Type')

if user_input:

    st.session_state['messages_history'].append({'role':'user' , 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
   # response = workflow.invoke({'messages': [HumanMessage(content=user_input)]}, config = CONFIG)
    #ai_messages= response['messages'][-1].content
    #st.session_state['messages_history'].append({'role':'assistant' , 'content': ai_messages})
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk , metadata  in workflow.stream(
            {'messages': [HumanMessage(content= user_input)]},
            config = CONFIG,
            stream_mode='messages',
            )
        )
    st.session_state['messages_history'].append({'role' : 'assistant' , 'content': ai_message})

    