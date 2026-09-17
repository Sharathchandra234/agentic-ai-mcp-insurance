import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.list_tools()

            print("\nAVAILABLE MCP TOOLS\n")

            for tool in result.tools:

                print(f"Tool: {tool.name}")
                print(f"Description: {tool.description}")
                print(f"Input schema: {tool.input_schema}")
                print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())