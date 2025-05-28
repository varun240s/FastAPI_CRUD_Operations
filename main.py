from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from SQLAlchemy import get_user_credentials  

app = FastAPI()

class EmailRequest(BaseModel):
    email: str


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/get-user")
async def get_user(request: EmailRequest):
    user = await get_user_credentials(request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname
    }
