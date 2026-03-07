from langchain_core.prompts import ChatPromptTemplate

sql_prompt = ChatPromptTemplate.from_template("""
You are an expert SQL generator.

Generate SQL for this question:
{question}
""")

validation_prompt = ChatPromptTemplate.from_template("""
Validate the following SQL query for correctness.

Question:
{question}
""")

explanation_prompt = ChatPromptTemplate.from_template("""
Explain the SQL query in simple terms.

Question:
{question}
""")