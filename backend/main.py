from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---

class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    done: bool = False

class Todo(TodoCreate):
    id: int

# --- In-memory store ---

db: dict[int, Todo] = {}
next_id: int = 1

# --- Routes ---

@app.get("/todos", response_model=list[Todo])
def list_todos() -> list[Todo]:
    return list(db.values())

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(payload: TodoCreate) -> Todo:
    global next_id
    todo = Todo(id=next_id, **payload.model_dump())
    db[next_id] = todo
    next_id += 1
    return todo

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int) -> Todo:
    if todo_id not in db:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db[todo_id]

@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoCreate) -> Todo:
    if todo_id not in db:
        raise HTTPException(status_code=404, detail="Todo not found")
    db[todo_id] = Todo(id=todo_id, **payload.model_dump())
    return db[todo_id]

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    if todo_id not in db:
        raise HTTPException(status_code=404, detail="Todo not found")
    del db[todo_id]
