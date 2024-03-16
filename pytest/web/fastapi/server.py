
import os
import threading

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import JSONResponse, Response, StreamingResponse
from fastapi import FastAPI

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

import uvicorn

from contextlib import asynccontextmanager


# 创建一个scheduler实例
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('start')
    scheduler.start()
    yield
    print('end')
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)


knowledges = ["DeepLN致力于提供高性价比的GPU租赁。"]
system_ptompt="你是一个有用的机器人，会根据背景知识回答我的问题。"



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/v1/generateText")
async def generateText(request: Request) -> Response:
    request_dict = await request.json()
    prompt = request_dict.pop("prompt")
    print("prompt:",prompt)
    background = prompt
    print("background:",background)

    return JSONResponse(background)


@scheduler.scheduled_job('interval', seconds=10)
async def cron_job():
    print(f"[{os.getpid()}-{threading.currentThread().ident}]The current time is {datetime.now()}")
 



if __name__ == "__main__":
    print(f"[{os.getpid()}-{threading.currentThread().ident}]The current time is {datetime.now()}")
    uvicorn.run(app, host="0.0.0.0", port=5001)
