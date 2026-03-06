from langchain_openai import ChatOpenAI 
import os 
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

llm = ChatOpenAI(model="gpt-5-nano", temperature=0.3)
# lesson 1


response = llm.invoke('What is the capital of France?')
print(response)


# lesson 2 

message = [
    (
        "system",
        "You are a helpful assistant that provides concise answers to questions.",
    ),
    ("user", "What is the capital of France?"),
]

ai_msg = llm.invoke(message) 

# aimsg : is a class called AIMessage, which has a content attribute that contains the response from the model -> to get textual respone, aimsg.text 

print(ai_msg.text)

# lesson 3 

# tool calling 

from pydantic import BaseModel, Field

class get_current_weather(BaseModel):
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")
    unit: str = Field(
        "celsius", description="The unit of temperature (fahrenheit or celsius)"
    )
llm_with_tools = llm.bind_tools(tools=[get_current_weather]) # 

ai_msg = llm_with_tools.invoke('What is the current weather in New York?')

print(ai_msg.text)
print('tool call : ' , ai_msg.tool_calls)

# python test_llm.py