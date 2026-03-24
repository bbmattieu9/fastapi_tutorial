from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from auth_database import get_db
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


SECRET_KEY = "H1X1ITS6O_IV8IbH6ISfNLDCQ_mXVihJqTiEmHozjYU"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#  Helper function that takes User Data

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()

@app.post("/signup")
def register_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already exist")
    # Hash the password
    hashed_pass = utils.hash_password(user.password)

    # Create new User instance
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password= hashed_pass,
        role= user.role
    )

    # Save User to Db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # return the value excluding password
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "role": new_user.role}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm =Depends(), db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Username")

    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")

    token_data = {'sub': user.username, 'role': user.role}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str =Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    return {"username": username, "role": role}


@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"Message": f"Hello, {current_user['username']} | You accessed a protected route"}

def required_roles(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to access this resource")
        return current_user
    return role_checker