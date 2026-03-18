"""AI Service for intelligent conversation"""
import os
from openai import AsyncOpenAI

class AIService:
    """
    AI-powered conversation engine
    Uses OpenAI API to generate intelligent responses
    """
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-key"))
    
    async def generate_response(
        self,
        customer_message: str,
        conversation_history: list,
        lead_context: any
    ) -> str:
        """
        Generate AI response to customer inquiry
        """
        
        # Build context for AI
        context = f"""You are a helpful car salesperson for a dealership.

Customer: {lead_context.customer_name}
Interested in: {lead_context.interested_vehicle or 'browsing'}
Previous status: {lead_context.status}

Your goal is to:
1. Answer questions about vehicles
2. Provide pricing information
3. Schedule test drives
4. Be helpful and friendly

Keep responses concise (2-3 sentences max).
"""
        
        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": context}
        ]
        
        # Add conversation history
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            messages.append({"role": "user", "content": msg})
        
        # Add current message
        messages.append({"role": "user", "content": customer_message})
        
        # Demo response - in production, call OpenAI
        # response = await self.client.chat.completions.create(
        #     model="gpt-4",
        #     messages=messages,
        #     max_tokens=150
        # )
        # return response.choices[0].message.content
        
        # Demo mode
        if "price" in customer_message.lower() or "cost" in customer_message.lower():
            return f"Great question! The {lead_context.interested_vehicle or 'vehicle you\'re interested in'} is priced competitively. I can send you a detailed quote with payment options. Would you like me to email that to you?"
        
        elif "test drive" in customer_message.lower():
            return "I'd love to set up a test drive for you! We have availability tomorrow and this weekend. What works best for your schedule?"
        
        else:
            return f"Thanks for reaching out! I'm here to help with any questions about the {lead_context.interested_vehicle or 'vehicles in our inventory'}. What would you like to know?"

# Singleton instance
ai_service = AIService()
