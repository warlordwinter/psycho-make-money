import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

# === Load environment ===
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# === Load and format CPT data ===
cpt_df = pd.read_csv("Mental_Health_CPT_Codes.csv")
cpt_chunks = [
    f"CPT {row['CPT Code']}: {row['Description']} — Category: {row['Category']} — Notes: {row['Notes']}"
    for _, row in cpt_df.iterrows()
]

# === Build retriever ===
embedding_model = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(cpt_chunks, embedding_model)
retriever = vectorstore.as_retriever(search_type="similarity", k=3)

def retrieve_memory(query: str, k=3):
    docs = retriever.get_relevant_documents(query)
    return "\n".join([doc.page_content for doc in docs])

# === Initialize LLM ===
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.2)

# === Agent 1: Parsing & Cleaning ===
parse_prompt = ChatPromptTemplate.from_template(
    """
    Clean and format this therapy transcript:
    - Separate speakers (Therapist: / Client:)
    - Fix formatting/typos
    - Split by topic if possible
    
    Transcript:
    {raw_text}
    """
)
parse_agent = parse_prompt | llm

# === Agent 2: Summarization ===
summarize_prompt = ChatPromptTemplate.from_template(
    """
    You are a licensed psychologist (PhD). You do not prescribe medication.
    Based on the transcript, generate:
    - SOAP Note
    - ICD-10 Code (with justification)
    - CPT Code (only codes like 90791, 90834, etc.)

    Transcript:
    {cleaned_text}
    """
)
summarization_agent = summarize_prompt | llm

# === Agent 3: Compliance Checker ===
compliance_prompt = ChatPromptTemplate.from_template(
    """
    Therapist License: {license}
    Summary: {summary}
    ICD-10: {icd}
    CPT: {cpt}

    Is this within legal and ethical scope? COMPLIANT or NON-COMPLIANT?
    Justify your answer.
    """
)
compliance_agent = compliance_prompt | llm

# === Agent 4: Billing Argument ===
billing_prompt = ChatPromptTemplate.from_template(
    """
    Create a paragraph justifying CPT code {cpt}, using:
    - SOAP Note: {soap}
    - ICD-10: {icd}
    """
)
billing_agent = billing_prompt | llm

# === Agent 5: Documentation Builder ===
doc_prompt = ChatPromptTemplate.from_template(
    """
    Combine and format the final documentation:
    - SOAP Note
    - ICD-10
    - CPT
    - Justification

    SOAP: {soap}
    ICD-10: {icd}
    CPT: {cpt}
    Justification: {justification}
    """
)
documentation_agent = doc_prompt | llm

# === Helper: Extract Parts ===
def extract_soap_icd_cpt(text: str):
    try:
        soap = text.split("SOAP Note:")[1].split("ICD-10")[0].strip()
        icd = text.split("ICD-10 Code:")[1].split("CPT")[0].strip()
        cpt = text.split("CPT Code:")[1].splitlines()[0].strip()
        return soap, icd, cpt
    except:
        return "", "", ""

# === Pipeline Runner ===
def run_full_therapist_pipeline(raw_text: str, license: str):
    cleaned = parse_agent.invoke({"raw_text": raw_text}).content.strip()
    summary_output = summarization_agent.invoke({"cleaned_text": cleaned}).content
    soap, icd, cpt = extract_soap_icd_cpt(summary_output)
    compliance_result = compliance_agent.invoke({
        "summary": summary_output,
        "license": license,
        "icd": icd,
        "cpt": cpt
    }).content.strip()
    justification = billing_agent.invoke({"soap": soap, "icd": icd, "cpt": cpt}).content.strip()
    final_doc = documentation_agent.invoke({
        "soap": soap,
        "icd": icd,
        "cpt": cpt,
        "justification": justification
    }).content.strip()
    return {
        "cleaned_transcript": cleaned,
        "summary": summary_output,
        "icd": icd,
        "cpt": cpt,
        "compliance": compliance_result,
        "billing_justification": justification,
        "final_documentation": final_doc
    }
