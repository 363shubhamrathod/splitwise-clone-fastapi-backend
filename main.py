from fastapi import FastAPI
from routers import groups, expenses, balances, users
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(groups.router)
app.include_router(expenses.router)
app.include_router(balances.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
