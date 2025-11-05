"""
AI Service using Google Gemini API
Handles all AI-powered features in the accounting system.
"""
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime
from io import BytesIO
from PIL import Image
import base64

import google.generativeai as genai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from backend.app.core.config import settings
from backend.app.models.ai import AITrainingData, AIPrediction, AIChatHistory
from backend.app.models.chart_of_accounts import ChartOfAccounts

logger = logging.getLogger(__name__)


class GeminiAIService:
    """AI Service powered by Google Gemini."""

    def __init__(self):
        """Initialize Gemini AI service."""
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not set. AI features will not work.")
            self.enabled = False
            return

        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Initialize models
        self.text_model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.vision_model = genai.GenerativeModel(settings.GEMINI_VISION_MODEL)

        # Generation config
        self.generation_config = {
            "temperature": settings.GEMINI_TEMPERATURE,
            "max_output_tokens": settings.GEMINI_MAX_TOKENS,
        }

        self.enabled = True
        logger.info("Gemini AI Service initialized successfully")

    async def process_document(
        self,
        file_content: bytes,
        file_type: str,
        company_id: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Process invoice/receipt using Gemini Vision.

        Args:
            file_content: Binary content of the image/PDF
            file_type: MIME type of the file
            company_id: Company ID for context
            db: Database session

        Returns:
            Dictionary with extracted data and confidence score
        """
        if not self.enabled:
            return {"error": "AI service not enabled"}

        try:
            # Convert to image
            image = Image.open(BytesIO(file_content))

            # Create prompt for Gemini
            prompt = """
            Analyze this invoice/receipt image and extract the following information in JSON format:

            {
              "document_type": "invoice" or "receipt" or "bill",
              "vendor_name": "Name of the vendor/supplier",
              "customer_name": "Name of customer (if applicable)",
              "document_number": "Invoice/receipt number",
              "document_date": "Date in YYYY-MM-DD format",
              "due_date": "Due date in YYYY-MM-DD format (if applicable)",
              "currency": "Currency code (USD, SAR, etc.)",
              "subtotal": 0.00,
              "tax_amount": 0.00,
              "total_amount": 0.00,
              "line_items": [
                {
                  "description": "Item description",
                  "quantity": 0,
                  "unit_price": 0.00,
                  "total": 0.00
                }
              ],
              "payment_method": "Cash/Credit Card/Bank Transfer (if mentioned)",
              "notes": "Any additional notes or terms"
            }

            Be precise and extract only information that is clearly visible.
            If any field is not found, use null.
            Return only valid JSON, no additional text.
            """

            # Generate content with image
            response = self.vision_model.generate_content(
                [prompt, image],
                generation_config=self.generation_config
            )

            # Parse JSON response
            extracted_text = response.text.strip()

            # Remove markdown code blocks if present
            if extracted_text.startswith("```json"):
                extracted_text = extracted_text[7:]
            if extracted_text.startswith("```"):
                extracted_text = extracted_text[3:]
            if extracted_text.endswith("```"):
                extracted_text = extracted_text[:-3]

            extracted_data = json.loads(extracted_text.strip())

            # Calculate confidence based on completeness
            confidence = self._calculate_extraction_confidence(extracted_data)

            # Save to database for learning
            await self._save_extraction_result(
                company_id=company_id,
                extracted_data=extracted_data,
                confidence=confidence,
                db=db
            )

            return {
                "success": True,
                "document_type": extracted_data.get("document_type", "unknown"),
                "extracted_data": extracted_data,
                "confidence": confidence,
                "raw_response": response.text
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            return {
                "success": False,
                "error": "Failed to parse document data",
                "raw_response": response.text if 'response' in locals() else None
            }
        except Exception as e:
            logger.error(f"Error processing document with Gemini: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def categorize_transaction(
        self,
        description: str,
        amount: float,
        company_id: str,
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Auto-categorize a transaction using Gemini.

        Args:
            description: Transaction description
            amount: Transaction amount
            company_id: Company ID
            db: Database session

        Returns:
            Suggested account with confidence score
        """
        if not self.enabled:
            return {"error": "AI service not enabled"}

        try:
            # Get company's chart of accounts
            result = await db.execute(
                select(ChartOfAccounts).where(
                    and_(
                        ChartOfAccounts.company_id == company_id,
                        ChartOfAccounts.is_active == True,
                        ChartOfAccounts.is_parent == False
                    )
                )
            )
            accounts = result.scalars().all()

            if not accounts:
                return {
                    "success": False,
                    "error": "No accounts found for this company"
                }

            # Format accounts for prompt
            accounts_list = [
                f"- {acc.account_code}: {acc.account_name_en} ({acc.account_type})"
                for acc in accounts[:50]  # Limit to 50 accounts to avoid token limits
            ]

            # Get historical categorizations for context
            historical = await self._get_historical_categorizations(
                company_id, description, db
            )

            historical_context = ""
            if historical:
                historical_context = "\n\nHistorical patterns for similar transactions:\n"
                for h in historical[:5]:
                    historical_context += f"- '{h['description']}' → {h['account']}\n"

            # Create prompt
            prompt = f"""
            You are an expert accountant. Categorize this transaction to the most appropriate account.

            Transaction:
            - Description: "{description}"
            - Amount: ${amount:.2f}

            Available accounts:
            {chr(10).join(accounts_list)}
            {historical_context}

            Based on the transaction description and amount, suggest the most appropriate account.

            Respond in JSON format:
            {{
              "account_code": "1234",
              "account_name": "Account Name",
              "confidence": 0.95,
              "reasoning": "Brief explanation why this account was chosen"
            }}

            Return only valid JSON, no additional text.
            """

            # Generate response
            response = self.text_model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            # Parse response
            result_text = response.text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:-3]
            if result_text.startswith("```"):
                result_text = result_text[3:-3]

            result_data = json.loads(result_text.strip())

            # Find matching account
            matching_account = next(
                (acc for acc in accounts if acc.account_code == result_data["account_code"]),
                None
            )

            if matching_account:
                result_data["account_id"] = matching_account.id
                result_data["success"] = True

                # Save for learning
                await self._save_categorization_result(
                    company_id=company_id,
                    description=description,
                    amount=amount,
                    suggested_account=matching_account.id,
                    confidence=result_data["confidence"],
                    db=db
                )
            else:
                result_data["success"] = False
                result_data["error"] = "Suggested account not found in company's chart of accounts"

            return result_data

        except Exception as e:
            logger.error(f"Error categorizing transaction: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def chat(
        self,
        message: str,
        company_id: str,
        user_id: str,
        session_id: str,
        context: Optional[Dict[str, Any]],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Chat with AI assistant about accounting data.

        Args:
            message: User's message
            company_id: Company ID for context
            user_id: User ID
            session_id: Chat session ID
            context: Additional context (current page, selected data, etc.)
            db: Database session

        Returns:
            AI response with suggestions and actions
        """
        if not self.enabled:
            return {"error": "AI service not enabled"}

        try:
            # Get chat history for context
            history_result = await db.execute(
                select(AIChatHistory)
                .where(
                    and_(
                        AIChatHistory.company_id == company_id,
                        AIChatHistory.session_id == session_id
                    )
                )
                .order_by(AIChatHistory.timestamp.desc())
                .limit(10)
            )
            history = list(reversed(history_result.scalars().all()))

            # Build conversation history
            conversation_context = ""
            if history:
                conversation_context = "\n\nPrevious conversation:\n"
                for msg in history:
                    conversation_context += f"{msg.message_type}: {msg.message_text}\n"

            # Create system prompt
            system_prompt = f"""
            You are an intelligent accounting assistant for a modern accounting system.
            You help users with:
            - Answering questions about their financial data
            - Generating reports
            - Creating journal entries
            - Understanding accounting concepts
            - Providing financial insights

            Current context:
            - Company ID: {company_id}
            - User is looking at: {context.get('current_page', 'unknown')}
            {conversation_context}

            When the user asks for data or reports:
            1. Explain what you understand from their request
            2. Suggest the appropriate report or action
            3. If you need more information, ask clarifying questions

            Be concise, professional, and helpful.
            """

            # Generate response
            full_prompt = f"{system_prompt}\n\nUser: {message}\n\nAssistant:"

            response = self.text_model.generate_content(
                full_prompt,
                generation_config=self.generation_config
            )

            assistant_message = response.text.strip()

            # Save to chat history
            user_msg = AIChatHistory(
                company_id=company_id,
                user_id=user_id,
                session_id=session_id,
                message_type="USER",
                message_text=message,
                timestamp=datetime.utcnow()
            )
            db.add(user_msg)

            assistant_msg = AIChatHistory(
                company_id=company_id,
                user_id=user_id,
                session_id=session_id,
                message_type="ASSISTANT",
                message_text=assistant_message,
                timestamp=datetime.utcnow()
            )
            db.add(assistant_msg)
            await db.commit()

            return {
                "success": True,
                "response": assistant_message,
                "suggestions": [],  # Can be enhanced to extract action items
                "actions": []  # Can be enhanced to suggest specific actions
            }

        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def generate_insights(
        self,
        company_id: str,
        financial_data: Dict[str, Any],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Generate financial insights using Gemini.

        Args:
            company_id: Company ID
            financial_data: Dictionary with financial metrics
            db: Database session

        Returns:
            List of insights with confidence scores
        """
        if not self.enabled:
            return {"error": "AI service not enabled"}

        try:
            prompt = f"""
            Analyze this financial data and provide 3-5 key insights:

            Financial Metrics:
            {json.dumps(financial_data, indent=2)}

            For each insight, provide:
            1. Type: "alert", "recommendation", "observation", or "opportunity"
            2. Title: Short, attention-grabbing title
            3. Description: Brief explanation (1-2 sentences)
            4. Priority: "high", "medium", or "low"
            5. Suggested action: What the user should do (if applicable)

            Focus on:
            - Unusual patterns or anomalies
            - Areas of concern
            - Opportunities for improvement
            - Trends that need attention

            Return as JSON array:
            [
              {{
                "type": "alert",
                "title": "Insight title",
                "description": "Description",
                "priority": "high",
                "suggested_action": "What to do",
                "confidence": 0.90
              }}
            ]

            Return only valid JSON array, no additional text.
            """

            response = self.text_model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            # Parse response
            result_text = response.text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:-3]
            if result_text.startswith("```"):
                result_text = result_text[3:-3]

            insights = json.loads(result_text.strip())

            return {
                "success": True,
                "insights": insights,
                "generated_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    # Helper methods

    def _calculate_extraction_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score based on extracted data completeness."""
        required_fields = ["vendor_name", "document_date", "total_amount"]
        optional_fields = ["document_number", "line_items", "tax_amount"]

        required_score = sum(1 for field in required_fields if data.get(field)) / len(required_fields)
        optional_score = sum(1 for field in optional_fields if data.get(field)) / len(optional_fields)

        # Weighted average: required fields are more important
        confidence = (required_score * 0.7) + (optional_score * 0.3)

        return round(confidence, 2)

    async def _save_extraction_result(
        self,
        company_id: str,
        extracted_data: Dict[str, Any],
        confidence: float,
        db: AsyncSession
    ):
        """Save document extraction result for training."""
        try:
            training_data = AITrainingData(
                company_id=company_id,
                data_type="DOCUMENT_EXTRACTION",
                input_data=json.dumps({"request": "document_extraction"}),
                output_data=json.dumps(extracted_data),
                confidence_score=confidence,
                is_validated=False
            )
            db.add(training_data)
            await db.commit()
        except Exception as e:
            logger.error(f"Error saving extraction result: {e}")

    async def _save_categorization_result(
        self,
        company_id: str,
        description: str,
        amount: float,
        suggested_account: str,
        confidence: float,
        db: AsyncSession
    ):
        """Save categorization result for training."""
        try:
            training_data = AITrainingData(
                company_id=company_id,
                data_type="CATEGORIZATION",
                input_data=json.dumps({"description": description, "amount": amount}),
                output_data=json.dumps({"account_id": suggested_account}),
                confidence_score=confidence,
                is_validated=False
            )
            db.add(training_data)
            await db.commit()
        except Exception as e:
            logger.error(f"Error saving categorization result: {e}")

    async def _get_historical_categorizations(
        self,
        company_id: str,
        description: str,
        db: AsyncSession,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get historical categorizations for similar transactions."""
        try:
            result = await db.execute(
                select(AITrainingData)
                .where(
                    and_(
                        AITrainingData.company_id == company_id,
                        AITrainingData.data_type == "CATEGORIZATION",
                        AITrainingData.is_validated == True
                    )
                )
                .order_by(AITrainingData.created_at.desc())
                .limit(limit * 2)  # Get more to find similar ones
            )
            training_data = result.scalars().all()

            historical = []
            for td in training_data:
                input_data = json.loads(td.input_data)
                output_data = json.loads(td.output_data)

                # Simple similarity check (can be enhanced)
                if any(word in input_data.get("description", "").lower()
                       for word in description.lower().split()):
                    historical.append({
                        "description": input_data.get("description"),
                        "account": output_data.get("account_id")
                    })

                if len(historical) >= limit:
                    break

            return historical
        except Exception as e:
            logger.error(f"Error getting historical categorizations: {e}")
            return []


# Create singleton instance
ai_service = GeminiAIService()
