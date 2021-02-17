from decimal import *
from math import log

class Loan:

    def __init__(self, principal, interest_rate, months):
        self.principal = principal
        self.interest_rate = interest_rate
        self.monthly_rate = self.interest_rate / 12
        self.months = months
        self.monthly_payment = self.__monthly_payment()
        self.total_payment = self.months * self.monthly_payment
        self.total_interest = self.total_payment - self.principal

    def __init__(self, principal, interest_rate, monthly_payment):
        self.principal = principal
        self.interest_rate = interest_rate
        self.monthly_rate = self.interest_rate / 12
        self.monthly_payment = monthly_payment
        self.months = self.__months()
        self.total_payment = self.months * self.monthly_payment
        self.total_interest = self.total_payment - self.principal

    def __monthly_payment(self):
        """Calculate monthly payment

        p((1+r)^(m-1)+(1+r)^(m-2)+...+(1+r)+1) = P(1+r)^m
        p((1+r)^m-1)/r = P(1+r)^m
        p = Pr(1+r)^m/((1+r)^m-1)
        """
        compound = (1 + self.monthly_rate) ** self.months
        payment = self.principal * self.monthly_rate * compound / (compound - 1)
        return payment

    def __months(self):
        """Calculate months

        ((1+r)^m-1)/(1+r)^m = Pr/p
        1 - 1/(1+r)^m = Pr/p
        (1+r)^m = p/(p-Pr)
        m = log(p/(p-Pr)) / log(1+r)
        """
        months = log(self.monthly_payment / (self.monthly_payment - self.principal * self.monthly_rate)) / log(1 + self.monthly_rate)
        return round(months)

    def get_months(self):
        return self.months

    def get_monthly_payment(self):
        return self.monthly_payment

    def get_total_payment(self):
        return self.total_payment

    def get_total_interest(self):
        return self.total_interest

    def amortization_schedule(self):
        month = list(range(1,self.months+1))
        monthly_principal = []
        monthly_interest = []
        monthly_balance = []
        fraction = 8
        balance = round(self.principal, fraction)
        for i in month:
            interest = round(balance * self.monthly_rate, fraction)
            principal = round(self.monthly_payment - interest, fraction)
            balance = round(balance - principal, fraction)
            monthly_principal.append(principal)
            monthly_interest.append(interest)
            monthly_balance.append(balance)
        return month, monthly_principal, monthly_interest, monthly_balance

if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--Principal", help="Loan ammount", type=Decimal)
    parser.add_argument("-I", "--InterestRate", help="Interest rate", type=Decimal)
    parser.add_argument("-M", "--Months", help="Number of months to pay off the loan", type=int, default=0)
    parser.add_argument("-p", "--MonthlyPayment", help="Monthly payment", type=Decimal, default=0)
    args = parser.parse_args()
    print(f"Principal: {args.Principal}")
    print(f"Interest Rate: {args.InterestRate}")
    if args.Months == 0 and args.MonthlyPayment == 0:
        sys.exit("Must provide --Months or --MonthlyPayment")
    if args.Months != 0:
        loan = Loan(args.Principal, args.InterestRate, args.Months)
    elif args.MonthlyPayment != 0:
        loan = Loan(args.Principal, args.InterestRate, args.MonthlyPayment)
    months = loan.get_months()
    print(f"Months: {months}")
    payment = loan.get_monthly_payment()
    print(f"Monthly Payment: {payment}")
    total_payment = loan.get_total_payment()
    print(f"Total Payment: {total_payment}")
    total_interest = loan.get_total_interest()
    print(f"Total Interest: {total_interest}")
    print("Amortization Schedule:")
    month, principal, interest, balance = loan.amortization_schedule()
    print("month\tprincipal\tinterest\tbalance")
    for i in range(len(month)):
        print(f"{month[i]}\t{principal[i]}\t{interest[i]}\t{balance[i]}")
