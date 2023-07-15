from sympy import O
from ai_model import BartenderAI, RecommandAI, SummaryPreferenceAI
import chainlit as cl

from langchain import ConversationChain, LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationBufferMemory

@cl.langchain_factory(use_async=True)
def factory():
    # Save the conversation history in the user session
    cl.user_session.set("history", "")
    cl.user_session.set("summary", "")
    bartender = BartenderAI()

    return bartender.get_chain()

@cl.action_callback("Summary Preference!")
async def on_action(action):
    history = cl.user_session.get("history")
    summary_ai = SummaryPreferenceAI()
    summary = summary_ai.run(history)
    
    cl.user_session.set("summary", summary)
    
    # Optionally remove the action button from the chatbot user interface
    await action.remove()
    
    await cl.Message(content=summary).send()

@cl.action_callback("Recommand Drink!")
async def on_action(action):
    summary = cl.user_session.get("summary")
    if not summary:
        history = cl.user_session.get("history")
        summary_ai = SummaryPreferenceAI()
        summary = summary_ai.run(history)
    
    recommand_ai = RecommandAI()
    recommand = recommand_ai.run(summary)
    
    # Optionally remove the action button from the chatbot user interface
    await action.remove()
    
    await cl.Message(content=recommand).send()

@cl.langchain_postprocess
async def postprocess(output: str):
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(name="Summary Preference!", value="example_value", description="Click me!"),
        cl.Action(name="Recommand Drink!", value="example_value1", description="Click me1!"),
    ]
    cl.user_session.set("history", output['history'])
    await cl.Message(content=output['response'], actions=actions).send()