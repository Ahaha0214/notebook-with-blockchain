from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import blockchain

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class NoteInput(BaseModel):
    content: str

# 前端頁面
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 新增記事
@app.post("/notes")
def add_note(note: NoteInput):
    tx_hash = blockchain.add_note_on_chain(note.content)
    return {"tx_hash": tx_hash}

# 取得所有記事
@app.get("/notes")
def read_notes():
    return blockchain.get_all_notes()
