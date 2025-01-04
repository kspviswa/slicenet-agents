import streamlit as st
from prompt import Prompter

st.markdown('# Slicenet Agent 🕵️‍♂️')
st.markdown('Your friendly co-pilot for running slicenet experiments')

if 'prompter' not in st.session_state:  
    st.session_state['prompter'] = Prompter()

prompter : Prompter = st.session_state['prompter'] 
for m in prompter.getMessages():
    if m['role'] != 'system':
        st.chat_message(m['role']).markdown(m['content'])

if prompt:= st.chat_input('how many i help you?'):
    st.chat_message('user').markdown(prompt)
    prompter.appendHistory('user', prompt)
    with st.spinner('Processing...'):
        response = prompter.doLLM()
        st.chat_message('assistant').markdown(response)
