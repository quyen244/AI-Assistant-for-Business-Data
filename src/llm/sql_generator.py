from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser , JsonOutputParser
from dotenv import load_dotenv
from src.llm.prompt_templates import sql_prompt, validation_prompt, explanation_prompt
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

llm = ChatOpenAI(model="gpt-5-nano", temperature=0.1)

generate_sql = sql_prompt | llm | StrOutputParser()
validate_sql = validation_prompt | llm | StrOutputParser()
explain_sql = explanation_prompt | llm | StrOutputParser()

chain = (
    RunnablePassthrough()
    | {
        'question' : lambda x : x['question'],
        'sql_query' : generate_sql
    }
    | {
        'question' : lambda x : x['question'],
        'sql_query' : lambda x : x['sql_query'],
        'validate_query' : validate_sql
    }
    | {
        'question' : lambda x : x['question'],
        'sql_query' : lambda x : x['sql_query'],
        'validate_query' : lambda x : x['validate_query'],
        'explain_query' : explain_sql
    }
)

if __name__ ==  "__main__":
    json_parser = JsonOutputParser()

    question = "What is the total sales for the last month?"
    result = chain.invoke({"question": question})
    print(json_parser.parse(result))
    #  py sql_generator.py / py -m src.llm.sql_generator