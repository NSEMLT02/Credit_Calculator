from math import ceil, log, pow
import argparse


class InvalidParameter(Exception):
    pass


def check_positive(value):
    # Method to check if args are positive and bigger than 0
    try:
        ivalue = float(value)
        if ivalue <= 0:
            raise InvalidParameter()
        return ivalue
    except InvalidParameter as Error:
        print("Incorrect parameters")
        exit()


is_periods = False
is_principal = False
is_interest = False
is_payment = False
# Declare and config parser
parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, required=True,
                    action='store')
parser.add_argument("--payment", type=check_positive, action="store")
parser.add_argument("--principal", type=check_positive, action="store")
parser.add_argument("--periods", type=check_positive, action="store")
parser.add_argument("--interest", type=check_positive, action="store")
args = parser.parse_args()


def parameter_check():
    # Check if argparse parameters are valid to operate
    global is_payment, is_interest, is_principal, is_periods
    count = 0
    # If type is annuity check which parameters where given
    if args.type == "annuity":
        if args.payment:
            count += 1
            is_payment = True
        if args.interest:
            count += 1
            is_interest = True
        if args.principal:
            count += 1
            is_principal = True
        if args.periods:
            count += 1
            is_periods = True

    # All other checks
    if not args.type:
        raise InvalidParameter()
    elif args.type == "diff" and args.payment:
        raise InvalidParameter()
    elif args.type == "annuity" and not args.interest:
        raise InvalidParameter()
    elif args.type == "diff" and not (args.principal and args.periods
                                      and args.interest):
        raise InvalidParameter()
    elif args.type == "annuity" and count != 3:
        raise InvalidParameter()


def main():
    try:
        parameter_check()
    except InvalidParameter as Error:
        print("Incorrect parameters")
        exit()
    if args.type == "diff":
        diff_payment()
    elif args.type == "annuity":
        annuity_payment()


def diff_payment():
    # Calculate each month payment for diff payment and print it
    p = args.principal
    n = int(args.periods)
    i = args.interest / 1200
    payments = []
    for m in range(1, n+1):
        dm = p / n + i * (p - p * (m - 1) / n)
        payments.append(ceil(dm))
    overpayment = int(sum(payments) - p)
    for i in range(n):
        print(f"Month {i + 1}: paid out {payments[i]}")
    print(overpayment)


def annuity_payment():
    # Decide, perform and print result of annuity calculation
    def overpayment():
        nonlocal credit_principal, monthly_payment, count_of_periods
        print(f"Overpayment = {ceil(monthly_payment * count_of_periods - credit_principal)}")

    count_of_periods = args.periods
    credit_interest = args.interest
    monthly_payment = args.payment
    credit_principal = args.principal
    # Decide which type of calculation perform
    type_of_calculation = None
    if not is_periods:
        type_of_calculation = "periods"
    elif not is_principal:
        type_of_calculation = "principal"
    elif not is_payment:
        type_of_calculation = "payment"
    # Perform calculation according to previous decision
    if type_of_calculation == 'periods':
        # Handle period calculation
        i = credit_interest / 1200
        x = monthly_payment / (monthly_payment - i * credit_principal)
        n = ceil(log(x, i + 1))
        count_of_periods = n
        years = n // 12
        months = n % 12
        if months <= 0:
            print(f'You need {years} years to repay this credit')
        else:
            print(f'You need {"0" if years < 1 else years} years and {months}'
                  f' months to repay this credit!')
        overpayment()

    elif type_of_calculation == 'payment':
        # Handle payment calculation
        i = credit_interest / 1200
        monthly_payment = ceil(
            credit_principal * ((i * pow(1 + i, count_of_periods)) / (pow(1 + i, count_of_periods) - 1)))
        print(f'Your annuity payment = {monthly_payment}!')
        overpayment()
    elif type_of_calculation == 'principal':
        # Handle principal calculation
        i = credit_interest / 1200
        credit_principal = int(
            monthly_payment / ((i * pow(1 + i, count_of_periods)) / (pow(1 + i, count_of_periods) - 1)))
        print(f'Your credit principal = {credit_principal}!')
        overpayment()


if __name__ == "__main__":
    main()

