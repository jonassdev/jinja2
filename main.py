from fastapi import FastAPI, Request, Form, Depends, status

from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session

import models

from database import engine, Sessionlocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory='templates')

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("index.html",
                                      {"request": request, "todo_list": todos})

@app.post("/add")
def add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()
    
    url = app.url_path_for("index")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
