import math
class Category:
    def __init__(self,name):
        self.name = name
        self.ledger = []
        self.budget = 0

    def __str__(self):
        display = ""
        display += "*"*(int((30-len(self.name))/2))+self.name+"*"*(int((31-len(self.name))/2))+"\n"
        for operation in self.ledger:
            space = 30 - len(operation["description"][:23]) - len(f"{operation['amount']:.2f}")
            display += f'{operation["description"][:23]}'+" "*space+f"{operation['amount']:.2f}"+"\n"
        display += f'Total: {self.budget:.2f}'
        return display

    def check_funds(self,amount):
        return self.get_balance() >= amount

    def deposit(self,amount,description=""):
        self.budget += amount
        _ = {
            "amount":amount,
            "description":description
        }
        self.ledger.append(_)

    def withdraw(self,amount,description=""):
        if self.check_funds(amount):
            self.budget -= amount
            _ = {
                "amount": -amount,
                "description":description
            }
            self.ledger.append(_)
            return True
        return False

    def get_balance(self):
        return self.budget

    def transfer(self,amount,category):
        if self.check_funds(amount):
            self.withdraw(amount,f'Transfer to {category.name}')
            category.deposit(amount,f'Transfer from {self.name}')
            return True
        return False

def create_spend_chart(categories):
    category_names = []
    category_withdraws = []
    for category in categories:
        name = category.name
        total = 0
        for operation in category.ledger:
            if operation["amount"] < 0:
                total += abs(operation["amount"])
        category_names.append(name)
        category_withdraws.append(total)
    grand_total = sum(category_withdraws)
    percentages = []
    for withdraws in category_withdraws:
        percent = (withdraws / grand_total) * 100
        rounded = int(percent / 10) * 10
        percentages.append(rounded)
    
    chart = "Percentage spent by category\n"
    
    for level in range(100, -1, -10):
        if level == 100:
            chart += "100|"
        elif level >= 10:
            chart += " " + str(level) + "|"
        else:
            chart += "  " + str(level) + "|"
        
        for i in range(len(percentages)):
            if percentages[i] >= level:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"
    
    dashes = "    -"
    for i in range(len(categories)):
        dashes += "---"
    chart += dashes + "\n"
    
    chart += "     "
    for j in range(len(category_names)):
        chart += category_names[j][0]
        if j < len(category_names) - 1:
            chart += "  "
    chart += "  "
    
    return chart
