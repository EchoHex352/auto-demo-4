"""Email Service for sending quotes and notifications"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from datetime import datetime

class EmailService:
    """Send emails via SendGrid"""
    
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY", "your-sendgrid-key")
        self.from_email = os.getenv("FROM_EMAIL", "sales@yourdealership.com")
    
    async def send_quote_email(
        self,
        to_email: str,
        customer_name: str,
        vehicle: dict,
        quote: any
    ):
        """Send quote email to customer"""
        
        # Build email HTML
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Your Personalized Quote</h2>
            
            <p>Hi {customer_name},</p>
            
            <p>Thank you for your interest! Here's your instant quote for:</p>
            
            <div style="background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="margin-top: 0;">{vehicle['year']} {vehicle['make']} {vehicle['model']} {vehicle.get('trim', '')}</h3>
                <p><strong>Stock #:</strong> {vehicle['stock_number']}</p>
                <p><strong>Price:</strong> ${quote.selling_price:,.2f}</p>
                {f"<p><strong>Trade-In Value:</strong> ${quote.trade_value:,.2f}</p>" if quote.trade_value > 0 else ""}
                {f"<p><strong>Down Payment:</strong> ${quote.down_payment:,.2f}</p>" if quote.down_payment > 0 else ""}
                <p><strong>Amount to Finance:</strong> ${quote.amount_financed:,.2f}</p>
            </div>
            
            <h3>Payment Options:</h3>
            
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #333; color: white;">
                    <th style="padding: 10px; text-align: left;">Term</th>
                    <th style="padding: 10px; text-align: right;">Payment</th>
                </tr>
                {''.join([
                    f'<tr style="border-bottom: 1px solid #ddd;"><td style="padding: 10px;">{opt["term_months"]} months</td><td style="padding: 10px; text-align: right; font-weight: bold;">${opt["monthly_payment"]:.2f}/mo</td></tr>'
                    for opt in quote.payment_options
                ])}
            </table>
            
            <div style="margin: 30px 0; padding: 20px; background: #e8f5e9; border-left: 4px solid #4caf50;">
                <p style="margin: 0;"><strong>🎉 Special Offer:</strong> Schedule a test drive today and receive a $500 bonus towards your purchase!</p>
            </div>
            
            <p>
                <a href="https://yourdealership.com/schedule?quote={quote.id}" 
                   style="display: inline-block; padding: 15px 30px; background: #2196f3; color: white; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    Schedule Test Drive
                </a>
            </p>
            
            <p>Questions? Reply to this email or call us at (555) 123-4567.</p>
            
            <p>
                Best regards,<br>
                Your Dealership Sales Team
            </p>
            
            <p style="font-size: 12px; color: #666; margin-top: 30px;">
                This quote is valid for 7 days. Pricing subject to change. All financing subject to credit approval.
            </p>
        </body>
        </html>
        """
        
        # In production, send via SendGrid
        # message = Mail(
        #     from_email=self.from_email,
        #     to_emails=to_email,
        #     subject=f"Your Quote for {vehicle['year']} {vehicle['make']} {vehicle['model']}",
        #     html_content=html_content
        # )
        # sg = SendGridAPIClient(self.api_key)
        # response = sg.send(message)
        
        # Demo mode - just log
        print(f"[EMAIL] Quote sent to {to_email}")
        print(f"Subject: Your Quote for {vehicle['year']} {vehicle['make']} {vehicle['model']}")
        
        return True
    
    async def send_appointment_confirmation(
        self,
        to_email: str,
        customer_name: str,
        appointment_time: datetime,
        appointment_type: str
    ):
        """Send appointment confirmation"""
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Appointment Confirmed ✅</h2>
            
            <p>Hi {customer_name},</p>
            
            <p>Your {appointment_type.replace('_', ' ')} is confirmed for:</p>
            
            <div style="background: #f5f5f5; padding: 20px; margin: 20px 0;">
                <p style="font-size: 24px; margin: 0;">
                    <strong>{appointment_time.strftime('%A, %B %d, %Y')}</strong>
                </p>
                <p style="font-size: 20px; margin: 10px 0;">
                    {appointment_time.strftime('%I:%M %p')}
                </p>
            </div>
            
            <p>We look forward to seeing you!</p>
            
            <p>
                <strong>Location:</strong><br>
                Your Dealership Name<br>
                123 Main Street<br>
                Anytown, ST 12345
            </p>
            
            <p>Need to reschedule? Reply to this email or call (555) 123-4567.</p>
        </body>
        </html>
        """
        
        print(f"[EMAIL] Appointment confirmation sent to {to_email}")
        
        return True

# Singleton instance
email_service = EmailService()
