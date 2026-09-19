import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
)


async def main():

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("\nCalling Neo4j Knowledge Graph MCP tool...\n")

            result = await session.call_tool(
                "query_knowledge_graph",
                {
                    "operation": "vehicle_claims",
                    "entity_id": "VEH001",
                },
            )

            print("RESULT:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())