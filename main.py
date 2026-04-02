from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv
import os
from database import engine
from models import Base
from database import SessionLocal
from models import User, FinancialData

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    password: str

class FinancialInput(BaseModel):
    user_id: int
    income: int
    expenses: int
    goal: str
    target_amount: int
    savings: int = 0
    investment_type: str = ""
    investment_amount: int = 0


load_dotenv()

api_key = os.getenv("API_KEY")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=api_key)


# Define structure of input data
class UserData(BaseModel):
    age: int
    income: int
    expenses: int
    goal: str
    target_amount: int
    time: int

def ai_explainer(age, income, expenses, savings, goal, target_amount, time):
    print("AI FUNCTION CALLED")

    prompt = f"""
You are a sharp, realistic financial advisor.

User:
- Age: {age}
- Income: {income}
- Expenses: {expenses}
- Savings: {savings}
- Goal: {goal}
- Target: {target_amount}
- Time: {time} months

Your job:
- Analyze behavior (not just math)
- Be honest and slightly critical if needed
- Avoid generic advice
- No calculations in output

Output format:

Financial Personality:
(1 line describing user habit)

Reality Check:
(1–2 lines about whether goal is realistic)

Smart Moves:
- 3 specific, practical suggestions

Trade-off Insight:
(1 powerful line like “If you continue this lifestyle…”)
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
        )

        print("AI RESPONSE RECEIVED")

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR >>>>>>>>>>>>>>>")
        print(e)
        print("<<<<<<<<<<<<<<<<<<<<<<<")
        return "AI advice unavailable"
    
@app.post("/signup")
def signup(user: UserCreate):
    db = SessionLocal()

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        return {"message": "User already exists"}

    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()

    return {"message": "User created"}

@app.post("/login")
def login(user: UserCreate):
    db = SessionLocal()

    existing = db.query(User).filter(
        User.username == user.username,
        User.password == user.password
    ).first()

    if not existing:
        return {"message": "Invalid credentials"}

    return {"message": "Login successful", "user_id": existing.id}

@app.post("/save-financial-data")
def save_data(data: FinancialInput):
    db = SessionLocal()

    existing = db.query(FinancialData).filter(
        FinancialData.user_id == data.user_id
    ).first()

    if existing:
        # update existing
        existing.income = data.income
        existing.expenses = data.expenses
        existing.goal = data.goal
        existing.target_amount = data.target_amount
        existing.savings = data.savings
        existing.investment_type = data.investment_type
        existing.investment_amount = data.investment_amount
    else:
        # create new
        new_data = FinancialData(
            user_id=data.user_id,
            income=data.income,
            expenses=data.expenses,
            goal=data.goal,
            target_amount=data.target_amount,
            savings=data.savings,
            investment_type=data.investment_type,
            investment_amount=data.investment_amount
        )
        db.add(new_data)

    db.commit()

    return {"message": "Financial data saved"}


# Create POST API
@app.post("/analyze")
def analyze(data: UserData):
    savings = data.income - data.expenses
    emergency_fund = data.expenses * 6

    health_score = int((savings / data.income) * 100) if data.income > 0 else 0

    advice = ai_explainer(
        data.age,
        data.income,
        data.expenses,
        savings,
        data.goal,
        data.target_amount,
        data.time
    )

    return {
        "savings": savings,
        "emergency_fund": emergency_fund,
        "health_score": health_score,
        "advice": advice
    }








