class Account:
    def __init__(self, user_id, account_type):
        self.user_id = user_id
        self.account_type = account_type
        self.balance = 0

        if account_type == "saving":
            self.interest_rate = 4
        else:
            self.interest_rate = 0