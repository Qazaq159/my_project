from fastapi import FastAPI
from app.students.router import router as router_students
from app.majors.router import router as router_majors
from app.users.router import router as router_users


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(router_students)
app.include_router(router_majors)
app.include_router(router_users)
