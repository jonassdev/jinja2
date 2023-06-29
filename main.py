from fastapi import FastAPI, Request
from typing import Union
from starlette.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html" , {"request": request})


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
