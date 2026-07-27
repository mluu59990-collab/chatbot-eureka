from fastapi import FastAPI, Depends, HTTPException
from database import engine, get_db, Base
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator
import models
import schemas
import auth
import llm
Base.metadata.create_all(bind = engine)
app = FastAPI()
@app.get("/users/me",response_model = schemas.UserOut)
def read_current_user(current_user:models.User=Depends(auth.get_current_user)):
    return current_user
@app.get("/")
def test():
    return {"Chatbot":"Chatbot is running...."}
@app.get("/users", response_model=list[schemas.UserOut])
def get_user(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
@app.post("/register", response_model=schemas.UserOut)
def register(user:schemas.UserCreate, db:Session = Depends(get_db)):
    # Check email ddaxc ton tai hay chua ktra xem thong tin email user dang ky co trung voi email trong DB khong
    existing_user = db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail = "Email đã được đăng ký")
    hashed_pw = auth.hash_password(user.password)
    new_user = models.User(email = user.email, password_hash= hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@app.get("/health/live")
def health_live():
    """
    Liveness:
    Kieemr tra FastAPI con hoat dong khong
    """
    return{
        "status":"alive",
        "service":"chatbot-backend"
    }
@app.get("/health/ready")
def health_ready():
    """
    Readliness
    Kiem tra backend da san snag nhan request

    """
    return{
        "status":"ready",
        "service":"chatbot-backend"
    }

@app.post("/login",response_model = schemas.Token)
def login(user:schemas.UserCreate,db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email==user.email).first()
    if not db_user or not auth.verify_password(user.password,db_user.password_hash):
        raise HTTPException(status_code = 401, detail=  "Email or password not correct!")
    access_token = auth.create_access_token(data={"sub":db_user.email})
    return{"access_token":access_token, "token_type":"bearer"}
@app.post("/conversation",response_model = schemas.ConversationOut)
@app.post("/conversations", response_model=schemas.ConversationOut)
def create_conversation(
    conv: schemas.ConversationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_conv = models.Conversation(title = conv.title, user_id = current_user.id)
    db.add(new_conv)
    db.commit()
    db.refresh(new_conv)
    return new_conv

@app.get("/conversation",response_model = list[schemas.ConversationOut])
@app.get("/conversations", response_model=list[schemas.ConversationOut])
def list_conversation(
    db:Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)

):
    return db.query(models.Conversation).filter(models.Conversation.user_id == current_user.id).all()

@app.get("/conversation/{conversation_id}", response_model=schemas.ConversationOut)
@app.get("/conversations/{conversation_id}", response_model=schemas.ConversationOut)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.post("/conversation/{conversation_id}/messages", response_model=schemas.MessageOut)
@app.post("/conversations/{conversation_id}/messages", response_model=schemas.MessageOut)
def create_message(
    conversation_id :int,
    msg: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)

):
    conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()
    if not conversation:
        raise HTTPException(status_code = 404, detail = "Conversation not found")
    user_message = models.Message(
        conversation_id = conversation.id,
        role = "user",
        content = msg.content
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    # Lấy toàn bộ lịch sử để gửi cho LLM
    history = db.query(models.Message).filter(
        models.Message.conversation_id == conversation.id
    ).order_by(models.Message.created_at).all()
    chat_history = [{"role":m.role,"content":m.content} for m in history]
    #3 goi LLM
    ai_rep = llm.get_ai_response(chat_history)
    ai_message = models.Message(
        conversation_id = conversation.id,
        role = "assistant",
        content = ai_rep
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)
    return ai_message

@app.get("/conversation/{conversation_id}/messages", response_model=list[schemas.MessageOut])
@app.get("/conversations/{conversation_id}/messages", response_model=list[schemas.MessageOut])
def list_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return db.query(models.Message).filter(
        models.Message.conversation_id == conversation_id
    ).order_by(models.Message.created_at).all()




from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9001",
        "http://127.0.0.1:9001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)