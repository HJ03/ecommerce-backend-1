from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, Product, User
from security import create_access_token, decode_token, hash_password, verify_password

# Create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS (tighten allow_origins in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # e.g. ["https://your-frontend.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- DB Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Schemas ----------
class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ---------- Helpers ----------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    # Extract username from token
    from jose import JWTError
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User no longer exists")
    return user

# ---------- Auth Endpoints ----------
@app.post("/auth/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    db_user = User(username=user.username, password_hash=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}

@app.post("/auth/login", response_model=TokenResponse)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        # user does not exist
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(user.password, db_user.password_hash):
        # password incorrect
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token({"sub": db_user.username})
    return TokenResponse(access_token=token)

# ---------- Protected Products ----------
@app.get("/products")
def get_products(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Product).all()

# ---------- Optional: a quick health/ping ----------
@app.get("/")
def root():
    return {"status": "ok"}
