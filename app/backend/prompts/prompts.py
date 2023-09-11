def generate_prompt(categories, transaction):
    prompt = f"""You are a bot that classifies credit card and bank transactions into a number of user-specified categories.

    Categories:
    {categories}

    Transaction:
    {transaction}

    Category:
"""
    
    return prompt