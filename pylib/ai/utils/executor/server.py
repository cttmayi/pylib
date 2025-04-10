
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import traceback


app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.post("/execute")
async def execute_code(request: CodeRequest):
    try:
        # 创建一个安全的执行环境
        restricted_globals = {}# {"__builtins__": {}}
        result = {}
        exec(request.code, restricted_globals, result)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        error_msg = f"代码执行出错：{traceback.format_exc()}"
        raise HTTPException(status_code=400, detail=error_msg)


def run(host="0.0.0.0", port=8860):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run()