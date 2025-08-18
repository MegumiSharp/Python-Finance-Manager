from datetime import datetime, timedelta
import random

from config.settings import INCORRECT_DATE, INCORRECT_YEAR

def generate_random_date(start_date, days_range=365):
    return (start_date + timedelta(days=random.randint(0, days_range))).strftime('%Y-%m-%d')

def seed_200_transactions(database):
    tags = ['Food', 'Rent', 'Utilities', 'Salary', 'Freelance', 'Travel', 'Shopping', 'Health']
    descriptions = ['Grocery store', 'Monthly rent', 'Electric bill', 'Company paycheck', 'Client invoice', 
                    'Flight to NYC', 'New shoes', 'Pharmacy visit']

    base_date = datetime.strptime("2024-01-01", "%Y-%m-%d")

    for i in range(200):
        date = generate_random_date(base_date)
        amount = round(random.uniform(-500, 1500), 2)  # Random amount: some negative (expenses), some positive (income)
        tag = random.choice(tags) + f"_{i}"  # Ensure uniqueness
        description = random.choice(descriptions) + f" #{i}"
        
        database.add_transaction(date=date, amount=amount, tag=tag, description=description)
        database.update_local()

def is_valid_date(date : str):
    try:
        date_str = date.strip()
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")

        if parsed_date.year > datetime.now().year:
            return INCORRECT_YEAR
        
        return True
    except ValueError:
        return INCORRECT_DATE
    

def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False