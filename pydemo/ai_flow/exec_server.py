# from pylib.ai.utils.executor.server import run as run_server
import io, sys
import traceback

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP Server")

@mcp.tool()
async def execute_code(code: str) -> dict:
    try:
        # 创建一个安全的执行环境
        restricted_globals = {}# {"__builtins__": {}}
        # result = {}

        output = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = output
        exec(code, restricted_globals)
        sys.stdout = original_stdout
        output_content = output.getvalue()
        output.close()
        return {'stdout': output_content}
    except Exception as e:
        error_msg = f"代码执行出错：{traceback.format_exc()}"
        print(error_msg)
        # raise HTTPException(status_code=400, detail=error_msg)
        # raise {'stderr': traceback.format_exc()}
        return {'stderr': error_msg}


if __name__ == "__main__":
    # 初始化并运行 server
    mcp.run(transport='sse')


