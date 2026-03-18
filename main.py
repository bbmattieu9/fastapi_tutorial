from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def home():
    return {"message": "How fast is FastAPI?"}

@app.get("/greet")
def greet():
    return {"message": "Hey Mattieu Guten Tag"}

@app.get("/greet/{name}")
def greet_name(name: str):
    return {"message": f"Hello {name}"}

# class Student(BaseModel):
#     name:str
#     age:int
#     roll:int