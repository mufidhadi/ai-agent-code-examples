import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

from typing import Optional

from openai import OpenAI
import json

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect(self):
        server_params = StdioServerParameters(
            command='uvx',
            args=['mcp-server-fetch'],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()
    
    async def list_tools(self):
        result = await self.session.list_tools()
        return [{
            'name': tool.name,
            'description': tool.description,
            'parameters': tool.inputSchema
        } for tool in result.tools]
    
    async def execute_tool(self, tool_name, parameters):
        result = await self.session.call_tool(tool_name, parameters)
        return '\n'.join([c.text for c in result.content])

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    try:
        oai_client = OpenAI(
            base_url = 'http://localhost:11434/v1',
            api_key='ollama', # required, but unused
        )

        await client.connect()
        tools = await client.list_tools()
        
        _tools = [
            {
                'type':'function',
                'function': t
            } for t in tools
        ]
        messages = [{"role": "user", "content": "kasih tau isi website synapsis.id dong"}]
        response = oai_client.chat.completions.create(
            model="llama3.2:3b",
            messages=messages,
            tools=_tools,
            tool_choice="auto"
        )
        if response.choices[0].finish_reason == "tool_calls":
            messages.append(response.choices[0].message)
            for tool in response.choices[0].message.tool_calls:
                tool_name = tool.function.name
                tool_args = tool.function.arguments
                tool_args = json.loads(tool_args)
                tool_output = await client.execute_tool(tool_name, tool_args)
                messages.append({"role": "function", "name": tool_name, "content": tool_output})
            response = oai_client.chat.completions.create(
                model="llama3.2:3b",
                messages=messages,
                tools=_tools,
                tool_choice="auto"
            )
        print(response.choices[0].message.content)
        print('-------------------')
    except Exception as e:
        # print(e)
        pass
    finally:
        await client.cleanup()

if __name__ == '__main__':
    asyncio.run(main())

