from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
import logging

template = ChatPromptTemplate.from_messages([
    SystemMessage(content="...."),
    ("human", "Hello, how are you"),
    ("ai", "I am good thanks!"),
    ("human", "{user_input}"),
])


prompt_value = template.invoke({
    "user_input":"What are regular expressions?"
})


print(prompt_value)