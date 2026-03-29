from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from dotenv import load_dotenv
import os

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
    income: int
    expenses: int

def ai_explainer(income, expenses, savings):
    print("AI FUNCTION CALLED")

    prompt = f"Income: {income}, Expenses: {expenses}, Savings: {savings}. Give short financial advice."

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
        )

        print("AI RESPONSE RECEIVED")

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR >>>>>>>>>>>>>>>")
        print(e)
        print("<<<<<<<<<<<<<<<<<<<<<<<")
        return "AI advice unavailable"
# def generate_advice(income, expenses, savings):
#     advice = ""

#     if savings <= 0:
#         advice += "You are overspending. Reduce unnecessary expenses immediately."
#     else:
#         advice += f"You are saving ₹{savings} per month."

#     # Emergency fund
#     emergency = expenses * 6
#     advice += f"Build an emergency fund of ₹{emergency}."

#     # Investment suggestion
#     if savings > 0:
#         sip = int(savings * 0.7)
#         advice += f"Invest around ₹{sip} monthly in SIPs."

#     # Basic insight
#     savings_rate = (savings / income) * 100 if income > 0 else 0

#     if savings_rate < 20:
#         advice += "Your savings rate is low. Try to increase it."
#     else:
#         advice += "Your savings rate is healthy."

#     return advice

# Create POST API
@app.post("/analyze")
def analyze(data: UserData):
    savings = data.income - data.expenses
    emergency_fund = data.expenses * 6
    health_score = int((savings / data.income) * 100) if data.income > 0 else 0

    advice = ai_explainer(
    data.income,
    data.expenses,
    savings
)

    return {
        "savings": savings,
        "emergency_fund": emergency_fund,
        "health_score": health_score,
        "advice": advice
    }