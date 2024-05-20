class IncomeSource: #Creating a parent class
    def __init__(self, name, amount):  # Constructor for IncomeSource objects
        if amount < 0:  # Checks if amount is negative
            raise ValueError("Income amount cannot be negative")  # Raises error for negative income
        self.name = name  # Assigns source_name to source attribute
        self.amount = amount  # Assigns amount to amount attribute

    def get_taxable_amount(self):  # Method to get taxable amount
        return self.amount  # Returns the full amount as taxable income

class SalaryIncome(IncomeSource): #Creating a child class
    def __init__(self, amount, pf_contribution, gis_contribution): #Recalling the parent parameters and initializing of parameters
        super().__init__("Salary", amount)
        self.deductions = pf_contribution + gis_contribution #Adding the pf_contribution and gis_contribution.

    def get_taxable_amount(self): #this behavior deductions pf and gis amount with the amount in the parent class. 
        return self.amount - self.deductions

class RentalIncome(IncomeSource):
    DEDUCTION_RATE = 0.2 #According the DRC, 20% duduction on on repairs and maintenance, interest payments, urban taxes and insurance premium.
    def __init__(self, total_income): #Recalling the parent parameters and initializing of parameters
        super().__init__("Rental", total_income)

    def get_taxable_amount(self):
        return self.amount * (1 - self.DEDUCTION_RATE)

class DividendIncome(IncomeSource):
    EXEMPTION = 30000 # it is set to 30000 as if dividend income exceeds 300000, TDS is charged
    TAX_RATE = 0.1 # 10% TDS is charged from the dividend

    def __init__(self, amount): #Initializes the parent class with "Dividend" as the income category and the total amount of dividend income.
        super().__init__("Dividend", amount)

    def get_taxable_amount(self): #This behavior calculates the taxable amount of the dividend income.
        taxable_amount = max(0, self.amount - self.EXEMPTION) # It calculates the taxable amount by subtracting the exemption and max is use to ensures it's non-negative. 
        return taxable_amount * self.TAX_RATE # Then, it applies the tax rate to this amount.

class OtherIncome(IncomeSource): # Inherits from IncomeSource class
    DEDUCTION_RATE = 0.3 #Fixed deduction rate for OtherIncome (30%)
    def __init__(self, amount): # Call parent constructor with type "Other" and amount
        super().__init__("Other", amount)

    def get_taxable_amount(self): # this behavior apply deduction rate to get taxable amount
        return self.amount * (1 - self.DEDUCTION_RATE)

class Taxpayer:
    def __init__(self, name):  # Initialize with taxpayer name
        self.name = name
        self.incomes = []
        self.general_deductions = 0

    def add_income(self, income):  # Add an income object to the incomes list
        self.incomes.append(income)

    def calculate_taxable_income(self):  # Sum the taxable amount from each income object
        return sum(income.get_taxable_amount() for income in self.incomes)

    def calculate_tax(self):  # Calculate taxable income
        taxable_income = self.calculate_taxable_income()
        net_income = taxable_income - self.general_deductions  # Subtract general deductions from taxable income
        tax_rate = self.get_tax_rate(net_income)  # Call get_tax_rate to find applicable tax rate based on net income
        tax = tax_rate * net_income  # Calculate base tax on net income
        if tax >= 1000000:  # Add a 10% surcharge if tax exceeds 1 million
            tax += tax * 0.1
        return tax

    def get_tax_rate(self, net_income):  # List of tax brackets (limit, rate)
        brackets = [(300000, 0),
            (400000, 0.1),
            (650000, 0.15),
            (1000000, 0.2),
            (1500000, 0.25),
            (float('inf'), 0.3),  # Use infinity for the last bracket
        ]
        for bracket_limit, rate in brackets:  # Loop through brackets to find applicable tax rate
            if net_income <= bracket_limit:
                return rate

    def add_general_deduction(self, amount):  # Add deduction amount to general deductions
        self.general_deductions += amount

    def get_formatted_tax_output(self):  # Define method to format tax output
        taxable_income = self.calculate_taxable_income()
        tax = self.calculate_tax()
        return f"{self.name}'s total tax payable: Nu{tax:,.2f}"  # Format tax with commas and two decimals

# Usage
taxpayer = Taxpayer("Lokesh") #Enter your name

salary_income = SalaryIncome(1200000, 30000, 10000) # Amount, PF and GIS
rental_income = RentalIncome(250000) # rental income
dividend_income = DividendIncome(10000) # dividend income

taxpayer.add_income(salary_income) # Add salary income to the taxpayer's income
taxpayer.add_income(rental_income) # Add rental income to the taxpayer's income
taxpayer.add_income(dividend_income) # Add dividend income to the taxpayer's income
taxpayer.add_general_deduction(0) # Add the general deduction as per the user(Right now the general deduction is 0)

formatted_output = taxpayer.get_formatted_tax_output() # Print out as (Name)'s total tax payable is (Tax) 
print(formatted_output)