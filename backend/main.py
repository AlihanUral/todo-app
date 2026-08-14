from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import engine, SessionLocal, Base
from models import Todo
from schemas import TodoCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Backend çalışıyor!"}


@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()


@app.post("/todos")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(text=todo.text)

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo is None:
        return {"message": "Todo bulunamadı"}

    db.delete(todo)
    db.commit()

    return {"message": "Todo silindi"}