class RiskAgent:

    def calculate(self, data):

        income = int(data.get("income",0))

        if income < 20000:
            return 0.8

        if income < 50000:
            return 0.5

        return 0.2