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
        pass


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
