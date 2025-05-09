from google.adk.agents import Agent


chef_agent = Agent(
    name="chef_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the recipes of food."
    ),
    instruction=(
        "You are a helpful chef agent who can answer user questions about all kinds of food recipes around the world."
    )
)