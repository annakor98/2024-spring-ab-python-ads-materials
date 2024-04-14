from fastapi import FastAPI
from utils import create_request, get_request


app = FastAPI()


@app.get("/factorial")
async def factorial_handler(no: int):
    request_id = create_request(no)
    return {'request_id': request_id}


@app.get("/factorial/result")
async def factorial_result_handler(request_id: str):
    result = get_request(request_id)
    return result
