from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP server
mcp = FastMCP("MCP Server")


@mcp.tool()
async def get_info(name: str) -> str:
    # """返回资源

    # Args:
    #     name: 资源名称.例如: hello
    # """

    resoures = {
        "hello": "Hello, world!",
    }

    return resoures.get(name, "Resource not found")


if __name__ == "__main__":
    # 初始化并运行 server
    mcp.run(transport='sse')