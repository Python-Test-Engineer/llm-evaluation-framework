from datetime import datetime


from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from rich.console import Console

console = Console()
load_dotenv(find_dotenv())
MODEL = "gpt-4o-mini"
TEMPERATURE = 0
llm = ChatOpenAI(model=MODEL, temperature=TEMPERATURE)


llm.invoke("How will the weather be in munich today?")


def get_time_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def get_weather(location: str):
    """Call to get the current weather."""
    if location.lower() in ["munich"]:
        return "It's 10 degrees Celsius and cold."
    else:
        return "It's 40 degrees Celsius and sunny."


@tool
def check_seating_availability(location: str, seating_type: str):
    """Call to check seating availability."""
    if location.lower() == "munich" and seating_type.lower() == "outdoor":
        return "Yes, we still have seats available outdoors."
    elif location.lower() == "munich" and seating_type.lower() == "indoor":
        return "Yes, we have indoor seating available."
    else:
        return "Sorry, seating information for this location is unavailable."


tools = [get_weather, check_seating_availability]


llm_with_tools = llm.bind_tools(tools)
tools_called = ""

result = llm_with_tools.invoke("How will the weather be in munich today?")

console.print("Tool name: ", result.tool_calls[0]["name"])

console.print("Tool args: ", result.tool_calls[0]["args"])


result = llm_with_tools.invoke(
    "How will the weather be in munich today? Do you still have seats outdoor available?"
)
result


result.tool_calls

tools_called = result.tool_calls

messages = [
    HumanMessage(
        "How will the weather be in munich today? Do you still have seats outdoor available?"
    )
]
llm_output = llm_with_tools.invoke(messages)
messages.append(llm_output)


messages


tool_mapping = {
    "get_weather": get_weather,
    "check_seating_availability": check_seating_availability,
}


llm_output.tool_calls


for tool_call in llm_output.tool_calls:
    tool = tool_mapping[tool_call["name"].lower()]
    tool_output = tool.invoke(tool_call["args"])
    messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))


messages


llm_with_tools.invoke(messages)
INPUT = ""
OUTPUT = ""
for message in messages:
    if isinstance(message, ToolMessage) or isinstance(message, HumanMessage):
        console.print(f"Message Type: {message.type}")
        console.print(f"Message: {message.content}")
        if message.type == "tool":
            OUTPUT += message.content
        if message.type == "human":
            INPUT += message.content


#################### EVALS01 ####################
#
# This can be standardised during development
# DATE|COMPONENT_CODE|MODEL|TEMPERATURE|INPUT|OUTPUT and any optional fields
#

log = f"{get_time_now()}|TOOL_CALLING|{MODEL}|{TEMPERATURE}|{INPUT}|{OUTPUT}|{tools_called}|\n"
console.print(log)

with open("./src/case_study/05_tool_calling.csv", "a") as f:
    f.write(f"{log}\n")
