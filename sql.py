import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
DB_NAME = "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
@asynccontextmanager
async def lifespan(app: FastAPI):
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        """)
    yield
app = FastAPI(title="To-Do List API", lifespan=lifespan)
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    completed: bool = False
class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    completed: bool
def task_dict(row):
    task = dict(row)
    task["completed"] = bool(task["completed"])
    return task
@app.post("/tasks", status_code=201)
def add_task(task: TaskCreate):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, ?)",
            (task.title, int(task.completed))
        )
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return task_dict(row)
@app.get("/tasks")
def view_tasks():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY id"
        ).fetchall()
        return [task_dict(row) for row in rows]
@app.get("/tasks/{task_id}")
def view_task(task_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(404, "Task not found")

        return task_dict(row)
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    with get_connection() as conn:
        cursor = conn.execute(
            """UPDATE tasks
               SET title = ?, completed = ?
               WHERE id = ?""",
            (task.title, int(task.completed), task_id)
        )
        if cursor.rowcount == 0:
            raise HTTPException(404, "Task not found")
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return task_dict(row)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?", (task_id,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(404, "Task not found")
    return {"message": "Task deleted successfully"}
