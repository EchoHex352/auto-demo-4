"""Payment Calculator Service"""

class PaymentCalculator:
    """Calculate monthly payments"""
    
    async def calculate_payment(
        self,
        amount: float,
        term: int,
        apr: float
    ) -> float:
        """
        Calculate monthly payment
        
        Formula: M = P * [r(1 + r)^n] / [(1 + r)^n - 1]
        Where:
        M = Monthly payment
        P = Principal (amount financed)
        r = Monthly interest rate (APR / 12 / 100)
        n = Number of payments (term in months)
        """
        if amount <= 0:
            return 0
        
        if apr == 0:
            return amount / term
        
        # Convert APR to monthly rate
        monthly_rate = apr / 12 / 100
        
        # Calculate payment
        payment = amount * (
            monthly_rate * ((1 + monthly_rate) ** term)
        ) / (
            ((1 + monthly_rate) ** term) - 1
        )
        
        return round(payment, 2)

# Singleton instance
payment_calculator = PaymentCalculator()
