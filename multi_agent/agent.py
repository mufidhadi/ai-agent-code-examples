from google.adk.agents import Agent

from multi_agent.sub_agent.chef.agent import chef_agent
from multi_agent.sub_agent.multi_tool_agent.agent import weather_agent

prompt = """
- you are helpful assistant named Tito.
- you have so much hate to manchester united and his fans, you always said bad thing using sarcastic language if asked about manchester united.
- you always talk nicely if asked about other things.
- if user ask about food, transfer to agent `chef`.
- if user ask about weather, transfer to agent `weather_agent`.
"""

root_agent = Agent(
    name="multi_agent",
    model="gemini-2.0-flash",
    description=(
        "Main Agent to answer questions from user."
    ),
    instruction=(
        prompt
    ),
    sub_agents=[weather_agent, chef_agent]
)