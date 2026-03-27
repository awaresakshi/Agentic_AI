from backend.app.agents.pan_agent import KYCAgent
from app.agents.fraud_agent import FraudAgent
from app.agents.risk_agent import RiskAgent
from app.agents.decision_engine import DecisionEngine

class OnboardingOrchestrator:

    def _init_(self):
        self.kyc = KYCAgent()
        self.fraud = FraudAgent()
        self.risk = RiskAgent()
        self.decision = DecisionEngine()

    def process(self, data):

        kyc_result = self.kyc.verify(data)

        fraud_result = self.fraud.check(data)

        risk_score = self.risk.calculate(data)

        final_decision = self.decision.make_decision(
            kyc_result,
            fraud_result,
            risk_score
        )

        return {
    "kyc": kyc_result,
    "fraud": fraud_result,
    "risk": risk_score,
    "decision": final_decision
}