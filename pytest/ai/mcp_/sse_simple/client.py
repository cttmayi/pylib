import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def run():
    async with sse_client("http://localhost:8000/sse") as (read_streams, write_stream):
        async with ClientSession(read_streams, write_stream) as session:
            await session.initialize()

            response = await session.list_tools()
            tools = response.tools
            print("\n已连接到服务器，工具包括：", [tool.name for tool in tools])


if __name__ == "__main__":
    asyncio.run(run())