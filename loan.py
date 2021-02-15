class Loan:

    def __init__(self, principal, interest_rate, months):
        self.principal = principal
        self.interest_rate = interest_rate
        self.monthly_rate = self.interest_rate / 12
        self.months = months
        self.monthly_payment = self.__monthly_payment()

    def __monthly_payment(self):
        """Calculate monthly payment

        p((1+r)^(m-1)+(1+r)^(m-2)+...+(1+r)+1) = P(1+r)^m
        p((1+r)^m-1)/r = P(1+r)^m
        p = Pr(1+r)^m/((1+r)^m-1)
        """
        compound = (1 + self.monthly_rate) ** self.months
        payment = self.principal * self.monthly_rate * compound / (compound - 1)
        return payment

    def get_monthly_payment(self):
        return self.monthly_payment

    def amortization_schedule(self):
        month = list(range(1,self.months+1))
        monthly_principal = []
        monthly_interest = []
        monthly_balance = []
        balance = self.principal
        for i in month:
            interest = balance * self.monthly_rate
            principal = self.monthly_payment - interest
            balance = balance - principal
            monthly_principal.append(principal)
            monthly_interest.append(interest)
            monthly_balance.append(balance)
        return month, monthly_principal, monthly_interest, monthly_balance

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--Principal", help="Loan ammount", type=float)
    parser.add_argument("-I", "--InterestRate", help="Interest rate", type=float)
    parser.add_argument("-M", "--Months", help="Number of months to pay off the loan", type=int)
    args = parser.parse_args()
    print(f"Principal: {args.Principal}")
    print(f"Interest Rate: {args.InterestRate}")
    print(f"Months: {args.Months}")
    loan = Loan(args.Principal, args.InterestRate, args.Months)
    payment = loan.get_monthly_payment()
    print(f"Monthly Payment: {payment}")
    print("Amortization Schedule:")
    month, principal, interest, balance = loan.amortization_schedule()
    print("month\tprincipal\tinterest\tbalance")
    for i in range(len(month)):
        print(f"{month[i]}\t{principal[i]}\t{interest[i]}\t{balance[i]}")
