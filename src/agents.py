import os
import logging
from dotenv import load_dotenv
# from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Initialize model with environment variable
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Define prompt templates and message creation
def create_messages(prompt: str, document: str):
    return [
        SystemMessage(content="You are a legal expert AI assistant."),
        HumanMessage(content=prompt.format(document=document))
    ]

def chunk_document(document: str, max_length: int = 5000) -> list[str]:
    chunks = []
    start = 0
    while start < len(document):
        end = min(start + max_length, len(document))
        chunks.append(document[start:end])
        start = end
    return chunks

async def legal_summary_agent(document: str) -> str:
    """Generate a document summary following Serbian legal standards."""
    try:
        doc_chunks = chunk_document(document)
        summaries = []
        for chunk in doc_chunks:
            messages = create_messages(
                """Vi ste AI asistent dizajniran da pomognete srpskim advokatima generisanjem sažetih pravnih dokumenata.
                Analizirajte dokument i generišite sažetak prema sledećoj strukturi:

                **Pregled slučaja:**
                - Stranke: [Stranke u postupku]
                - Sud: [Naziv suda]
                - Broj predmeta: [Broj predmeta]
                - Datum: [Datum dokumenta]

                **Ključne činjenice:**
                [Sažetak najvažnijih činjenica u 2-3 tačke]

                **Pravni problemi:**
                [Lista glavnih pravnih pitanja u 2-3 tačke]

                **Argumenti:**
                - Argumenti tužioca: [Sažetak argumenata]
                - Argumenti tuženog: [Sažetak argumenata]

                **Dokazi:**
                [Lista najvažnijih dokaza obe strane]

                **Sudska odluka ili ishod:**
                [Sažetak odluke ili trenutnog stanja]

                **Ključni zaključci:**
                [Korisni uvidi i preporuke za dalje korake]

                Analizirajte sledeći dokument i popunite strukturu:
                {document}""",
                chunk
            )
            response = model.invoke(messages)
            summaries.append(response.content)
        return " ".join(summaries)
    except Exception as e:
        logging.error(f"Error in summary agent: {e}")
        return f"Error generating summary: {str(e)}"

async def legal_appeal_agent(document: str) -> str:
    """Generate a formal appeal based on Serbian legal standards."""
    try:
        doc_chunks = chunk_document(document)
        appeal_parts = []
        for chunk in doc_chunks:
            messages = create_messages(
                """Vi ste pravni pomoćnik specijalizovan za sastavljanje formalnih žalbi na osnovu dostavljenog pravnog dokumenta.
                Analizirajte dokument i generišite žalbu prema sledećoj strukturi:

                1. Zaglavlje
                [IME SUDA]
                [JURISDIKCIJA]
                [Broj predmeta]
                [IME ŽALIOCA/APELANTA], Apelant
                protiv
                [IME ODGOVARAJUĆE STRANKE], Apelovanog

                2. ŽALBA / OBAVEŠTENJE O ŽALBI
                [Formalno obaveštenje o žalbi]

                3. Izjava o Jurisdikciji
                [Objašnjenje nadležnosti]

                4. Izjava Činjenica
                [Činjenična pozadina]

                5. Pitanja na koja se Žali
                [Lista konkretnih pitanja]

                6. Argumentacija
                [Detaljni argumenti za svako pitanje]

                7. Zaključak
                [Traženi ishod]

                8. Potpis i Kontakt Informacije
                [Potpis i detalji]

                9. Sertifikat o Dostavljanju
                [Potvrda o dostavljanju]

                Analizirajte sledeći dokument i popunite strukturu:
                {document}""",
                chunk
            )
            response = model.invoke(messages)
            appeal_parts.append(response.content)
        return " ".join(appeal_parts)
    except Exception as e:
        logging.error(f"Error in appeal agent: {e}")
        return f"Error generating appeal: {str(e)}"

async def legal_review_agent(document: str) -> str:
    """Generate a comprehensive legal review following Serbian legal standards."""
    try:
        doc_chunks = chunk_document(document)
        reviews = []
        for chunk in doc_chunks:
            messages = create_messages(
                """Vi ste AI asistent dizajniran da pomognete srpskim advokatima generisanjem sveobuhvatnih pravnih pregleda.
                Analizirajte dokument i generišite pravni pregled prema sledećoj strukturi:

                1. Pregled dokumenta
                [Svrha dokumenta, uključene strane, ključni uslovi]

                2. Ključne klauzule i obaveze
                - Uslovi plaćanja
                - Rokovi
                - Klauzule o raskidu
                - Ostale važne klauzule

                3. Provera pravne usklađenosti
                [Provera usklađenosti sa srpskim zakonima]
                - Reference na relevantne zakone
                - Analiza usklađenosti klauzula

                4. Procena rizika
                [Lista potencijalnih rizika]
                - Nejasne klauzule
                - Potencijalni sporovi
                - Pravne rupe

                5. Preporuke
                [Konkretne preporuke za poboljšanje]
                - Predložene izmene
                - Dodatne klauzule
                - Mere za smanjenje rizika

                6. Zaključak
                [Sažetak ključnih nalaza i kritičnih problema]

                Analizirajte sledeći dokument i popunite strukturu:
                {document}""",
                chunk
            )
            response = model.invoke(messages)
            reviews.append(response.content)
        return " ".join(reviews)
    except Exception as e:
        logging.error(f"Error in review agent: {e}")
        return f"Error generating review: {str(e)}"

async def legal_lawsuit_agent(document: str) -> str:
    """Generate a formal lawsuit based on the legal document analysis following Serbian legal standards."""
    try:
        doc_chunks = chunk_document(document)
        lawsuit_parts = []
        for chunk in doc_chunks:
            messages = create_messages(
                """Vi ste AI asistent dizajniran da pomognete srpskim advokatima u sastavljanju pravnih tužbi i srodnih dokumenata.
                Analizirajte dokument i generišite pravnu tužbu prema sledećoj strukturi:

                [Naziv suda]
                [Nadležnost]
                [Broj predmeta]

                TUŽILAC: [Izvući iz dokumenta]
                TUŽENI: [Izvući iz dokumenta]

                TUŽBA

                I. UVOD
                [Generisati uvod na osnovu dokumenta]

                II. NADLEŽNOST I MESTO SUDA
                [Utvrditi nadležnost]

                III. STRANKE
                [Detalji o strankama iz dokumenta]

                IV. ČINJENIČNE TVRDNJE
                [Izvući i organizovati činjenice]

                V. OSNOVI ZA TUŽBU
                [Pravni osnovi]

                VI. ŠTETE
                [Specifikacija štete]

                VII. ZAHTEV ZA NAKNADU ŠTETE
                [Formulisati zahteve]

                VIII. ZAHTEV ZA SUDSKIM VEĆEM
                [Standardni zahtev]

                IX. PRILOZI
                [Navesti dokaze]

                Analizirajte sledeći dokument i popunite strukturu:
                {document}""",
                chunk
            )
            response = model.invoke(messages)
            lawsuit_parts.append(response.content)
        return " ".join(lawsuit_parts)
    except Exception as e:
        logging.error(f"Error in lawsuit agent: {e}")
        return f"Error generating lawsuit: {str(e)}"

async def legal_lawsuit_response_agent(document: str) -> str:
    """Generate a formal response to a lawsuit based on Serbian legal standards."""
    try:
        doc_chunks = chunk_document(document)
        response_parts = []
        for chunk in doc_chunks:
            messages = create_messages(
                """Vi ste AI asistent dizajniran da pomognete srpskim advokatima u pripremanju pravnih odgovora na tužbe.
                Analizirajte dokument i generišite odgovor na tužbu prema sledećoj strukturi:

                [Naziv suda]
                [Nadležnost]
                [Broj predmeta]

                [Ime tuženog]
                Adresa: [Adresa tuženog]
                Telefon: [Telefon tuženog]
                Email: [Email tuženog]

                ODGOVOR NA TUŽBU

                I. UVOD
                [Generisati uvod na osnovu dokumenta]

                II. IZJAŠNJENJE O ČINJENIČNIM TVRDNJAMA
                [Obrada tvrdnji tužioca pojedinačno]

                III. PRAVNI ARGUMENTI
                [Pravni argumenti i kontraargumenti]

                IV. DOKAZI
                [Nabrojati i opisati dokaze]

                V. ZAHTEV ZA ODLUKU
                [Formulisati zahteve]

                VI. PRILOZI
                [Navesti dokaze]

                Analizirajte sledeći dokument i popunite strukturu:
                {document}""",
                chunk
            )
            response = model.invoke(messages)
            response_parts.append(response.content)
        return " ".join(response_parts)
    except Exception as e:
        logging.error(f"Error in lawsuit response agent: {e}")
        return f"Error generating lawsuit response: {str(e)}"

async def legal_contract_analysis_agent(document: str) -> str:
    """Analyze legal contracts to identify terms, risks, and potential issues."""
    try:
        doc_chunks = chunk_document(document)
        analysis_parts = []
        for chunk in doc_chunks:
            messages = create_messages(
                """Perform a comprehensive contract analysis. Include:
                1. Essential Terms Analysis
                   - Identify missing or incomplete terms
                   - Evaluate payment terms and conditions
                   - Review performance obligations
                
                2. Risk Assessment
                   - Identify potential legal risks
                   - Highlight liability concerns
                   - Review indemnification clauses
                
                3. Compliance Check
                   - Verify regulatory compliance
                   - Check for standard legal requirements
                   - Identify jurisdiction-specific issues
                
                4. Recommendations
                   - Suggest improvements
                   - Highlight areas needing clarification
                   - Propose risk mitigation strategies
                
                Document: {document}""",
                chunk
            )
            response = model.invoke(messages)
            analysis_parts.append(response.content)
        return " ".join(analysis_parts)
    except Exception as e:
        logging.error(f"Error in contract analysis agent: {e}")
        return f"Error analyzing contract: {str(e)}"

async def legal_chat_helper_agent(document: str, question: str = "") -> str:
    """Interactive chat agent for answering questions about legal documents."""
    try:
        system_message = SystemMessage(content="""
            You are the "Legal Chat Helper Agent," designed to assist users in managing and interacting with documents.
            Your role is to:
            - Guide users through document interactions
            - Provide explanations in clear, layman's terms
            - Help with understanding specific parts of documents
            - Suggest relevant document actions (summary, appeal, review, etc.)
            - Remain neutral and professional
            - Ensure accurate and helpful responses
            
            When responding:
            1. First understand if the user needs:
               - Explanation of document content
               - Help with document modifications
               - Guidance on using other agents
               - General legal document questions
            2. Provide clear, structured responses
            3. Suggest relevant next steps or actions
            4. Always base responses on the provided document content
        """)
        
        human_message = HumanMessage(content=f"""
            Based on this legal document, please help with the following:
            
            User Question: {question}
            
            Document Content:
            ---
            {document}
            ---
            
            Please provide a helpful and detailed response while maintaining professional legal context.
        """)
        
        messages = [system_message, human_message]
        response = model.invoke(messages)
        return response.content
    except Exception as e:
        logging.error(f"Error in chat helper: {e}")
        return "I apologize, but I encountered an error. Could you please rephrase your question or specify what you'd like to know about the document?"
