from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def home():
    return "hello World!"

@app.get("/{number}")
def return_double(number: int):
    return get_double(number)

def get_double(number: int):
    return number * 2
