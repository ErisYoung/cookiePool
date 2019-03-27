
def parse_accounts(sep='----'):
    with open("account.txt",'r') as f:
        for account in f.readlines():
            nameuser,password=account.strip().split(sep)
            yield (nameuser,password)


