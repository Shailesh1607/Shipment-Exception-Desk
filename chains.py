
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import llm


CLASSIFY_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You triage shipment exception reports for a logistics company. "
     "Read the report and classify it into exactly one word: "
     "'delayed', 'damaged', 'lost', or 'unknown' if it doesn't clearly "
     "fit any of those. Reply with that single word only, nothing else."),
    ("human", "{report_text}"),
])

classify_chain = CLASSIFY_PROMPT | llm | StrOutputParser()


ESCALATE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You write short internal notes for a shipment-exception manager "
     "who needs to approve a compensation decision. Summarize the "
     "report, the category, and the reasoning below in 2-3 sentences, "
     "and end with a clear request for approval."),
    ("human",
     "Report: {report_text}\nCategory: {category}\n"
     "Proposed compensation: ${amount:.2f}\n"
     "Reasoning: {reasoning}"),
])

escalate_chain = ESCALATE_PROMPT | llm | StrOutputParser()


DRAFT_EMAIL_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You write short, polite customer-facing emails for a logistics "
     "company resolving a shipment exception. Acknowledge the issue, "
     "state the compensation being issued, and keep it to 3-4 sentences."),
    ("human",
     "Report: {report_text}\nCategory: {category}\n"
     "Compensation: ${amount:.2f}\nReasoning: {reasoning}"),
])

draft_email_chain = DRAFT_EMAIL_PROMPT | llm | StrOutputParser()
