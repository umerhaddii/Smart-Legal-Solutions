import logging
from .agents import (
    legal_summary_agent, 
    legal_appeal_agent, 
    legal_review_agent, 
    legal_lawsuit_agent,
    legal_lawsuit_response_agent,
    legal_contract_analysis_agent,
    legal_chat_helper_agent  # Add new import
)

class LegalDocumentProcessor:
    async def process_document(self, text: str, request_type: str, question: str = "") -> dict:
        try:
            if not text.strip():
                return {"error": "Document cannot be empty"}

            # Define valid request types and their handlers
            request_handlers = {
                "summary": legal_summary_agent,
                "appeal": legal_appeal_agent,
                "review": legal_review_agent,
                "lawsuit": legal_lawsuit_agent,
                "lawsuit_response": legal_lawsuit_response_agent,
                "contract_analysis": legal_contract_analysis_agent,
                "chat": legal_chat_helper_agent
            }

            if request_type not in request_handlers:
                valid_types = ", ".join(request_handlers.keys())
                logging.error(f"Invalid request type: {request_type}. Valid types: {valid_types}")
                return {"error": f"Invalid request type. Must be one of: {valid_types}"}

            handler = request_handlers[request_type]
            try:
                if request_type == "chat":
                    result = await handler(text, question or "")
                else:
                    result = await handler(text)
                return {"result": result}
            except Exception as e:
                logging.error(f"Handler error for {request_type}: {str(e)}")
                return {"error": f"Error processing {request_type} request: {str(e)}"}

        except Exception as e:
            logging.error(f"Processing error: {e}")
            return {"error": str(e)}