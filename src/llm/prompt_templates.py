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

summary = """
You are a data analyst.

Your task is to create a concise but informative summary of a dataset so that another LLM can understand the dataset structure and use it for analysis or question answering.

Dataset metadata is provided below.

METADATA:
{metadata}

Write a clear dataset summary including:

1. Dataset overview
- filename
- number of rows
- number of columns

2. Columns description
For each column mention:
- column name
- possible data type (numeric / categorical / text / datetime if inferable)
- short explanation of what the column likely represents

3. Important statistics (if available)
Summarize key statistics such as:
- mean / min / max for numeric columns
- common values for categorical columns
Do not list every statistic, only the most useful ones.

4. Sample data pattern
Briefly describe patterns visible from the sample rows.

Rules:
- Keep the summary structured and concise
- Avoid repeating raw metadata
- Focus on information useful for data analysis
- Maximum 200-300 words

Return only the summary.
"""

summary_prompt = ChatPromptTemplate.from_template(summary)

insight = """
You are a senior data analyst.

Your task is to analyze the dataset summary and generate meaningful data insights.

DATASET SUMMARY:
{summary}

Generate insights about patterns, trends, anomalies, or relationships in the dataset.

Return the insights in the following JSON format.

{format_instructions}


Rules:
- Generate 5 insights.
- Focus on meaningful patterns useful for business or analysis.
- Use only information from the dataset summary.
- Avoid vague statements.
- Always return valid JSON.
"""

insight_prompt = ChatPromptTemplate.from_template(insight)