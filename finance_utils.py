def simulate_loan(income, expenses, loan_amount, interest_rate, months):
    disposable = income - expenses


    if disposable <= 0:
        return {
            "monthly_payment": 0,
            "status": "Dangerous",
            "explanation": "You currently have no disposable income. Taking this loan would likely cause financial harm."
        }


    monthly_rate = interest_rate / 100 / 12


    monthly_payment = loan_amount * (
        (monthly_rate * (1 + monthly_rate) ** months) /
        ((1 + monthly_rate) ** months - 1)
    )


    ratio = monthly_payment / disposable


    if ratio < 0.3:
        status = "Safe"
    elif ratio < 0.5:
        status = "Caution"
    else:
        status = "Dangerous"


    explanation = (
        f"Your monthly disposable income is ${disposable:.2f}. "
        f"This loan would cost ${monthly_payment:.2f} per month. "
        f"This is considered {status}."
    )


    return {
        "monthly_payment": round(monthly_payment, 2),
        "status": status,
        "explanation": explanation
    }
