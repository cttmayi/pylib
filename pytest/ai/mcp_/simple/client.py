import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

import json

load_dotenv()  # 从 .env 加载环境变量

class MCPClient:
    def __init__(self):
        # 初始化会话和客户端对象
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
    # 方法将在这里添加

    async def connect_to_server(self, server_script_path: str):
        """连接到 MCP 服务器

        Args:
            server_script_path: 服务器脚本的路径 (.py 或 .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("服务器脚本必须是 .py 或 .js 文件")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # 列出可用的工具
        response = await self.session.list_tools()
        tools = response.tools
        print("\n已连接到服务器，工具包括：", [tool.name for tool in tools])


    async def process_query(self, query: str) -> str:

        tool_name = 'get_info' # tool['name']
        tool_args = {
            "name": query,
        }
        

        # 处理响应并处理工具调用
        final_text = []

        # 执行工具调用
        result = await self.session.call_tool(tool_name, tool_args)
        final_text.append(f"[调用工具 {tool_name}，参数 {tool_args}]")
        final_text.append(str(result.content))

        return "\n".join(final_text)


    async def chat_loop(self):
        """运行交互式聊天循环"""
        print("\nMCP 客户端已启动！")
        print("输入你的查询或输入 'quit' 退出。")

        while True:
            # try:
            query = input("\n查询: ").strip()

            if query.lower() == 'quit':
                break

            response = await self.process_query(query)
            print(response)

            # except Exception as e:
            #     print(f"\n错误: {str(e)}")

    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("使用方法: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())