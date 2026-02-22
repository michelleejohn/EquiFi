import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from openai import OpenAI


from ai_utils import calculate_risk
from finance_utils import simulate_loan


load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")




@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()




@app.post("/analyze-document")
async def analyze_document(
    file: UploadFile = File(...),
    language: str = Form("English")
):
    text = (await file.read()).decode("utf-8")


    risk = calculate_risk(text)


    prompt = f"""
Rewrite this financial document at a 6th-grade reading level.
Then list the key risks in bullet points, with a new paragraph line for each bullet point.
Then explain APR in simple terms.
Make your answer concise and easy to understand, limited to one paragraph.
Translate everything to {language}.


Document:
{text}
"""


    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}]
    )


    simplified = response.choices[0].message.content


    return {
        "simplified": simplified,
        "risk": risk
    }




@app.post("/simulate-loan")
async def loan_simulation(
    income: float = Form(...),
    expenses: float = Form(...),
    loan_amount: float = Form(...),
    interest_rate: float = Form(...),
    months: int = Form(...)
):
    return simulate_loan(income, expenses, loan_amount, interest_rate, months)
