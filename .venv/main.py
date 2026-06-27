from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
@app.post("/users")
def create_user(user: dict):
    return user