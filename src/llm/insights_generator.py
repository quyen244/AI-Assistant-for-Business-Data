from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from typing import List, Literal, Dict
from dotenv import load_dotenv

from src.llm.prompt_templates import summary_prompt, insight_prompt

load_dotenv()

llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

# -------------------
# Pydantic Schema
# -------------------

class Insight(BaseModel):
    title: str
    description: str
    related_columns: List[str]

    insight_type: Literal[
        "trend",
        "comparison",
        "distribution",
        "correlation",
        "anomaly",
    ]

    importance: Literal[
        "high",
        "medium",
        "low",
    ]

    suggested_visualization: Literal[
        "bar_chart",
        "line_chart",
        "histogram",
        "scatter_plot",
        "pie_chart",
    ]


class InsightsOutput(BaseModel):
    insights: List[Insight]


parser = PydanticOutputParser(pydantic_object=InsightsOutput)

format_instructions = parser.get_format_instructions()

# -------------------
# Chains
# -------------------

text_parser = StrOutputParser()

summary_chain = summary_prompt | llm | text_parser

insight_chain = insight_prompt | llm | parser


final_chain = (
    RunnablePassthrough()
    | {
        "summary": lambda x: summary_chain.invoke(
            {"metadata": x["metadata"]}
        )
    }
    | {
        "summary": lambda x: x["summary"],
        "insights": lambda x: insight_chain.invoke(
            {
                "summary": x["summary"],
                "format_instructions": format_instructions,
            }
        ),
    }
)


def generate_insights(metadata: Dict):

    res = final_chain.invoke(
        {
            "metadata": metadata
        }
    )

    return res 

if __name__ == "__main__":
    metadata = {
        'id' : 1 ,
        'filename' : 'sales.csv',
        "columns":	["Region", "Country", "Item Type", "Sales Channel", "Order Priority", "Order Date", "Order ID", "Ship Date", "Units Sold", "Unit Price", "Unit Cost", "Total Revenue", "Total Cost", "Total Profit"],
        "num_rows" : 1330,
        "samples": [{"Region": "Europe", "Country": "Czech Republic", "Order ID": 478051030, "Item Type": "Beverages", "Ship Date": "9/29/2011", "Unit Cost": 31.79, "Order Date": "9/12/2011", "Total Cost": 151892.62, "Unit Price": 47.45, "Units Sold": 4778, "Total Profit": 74823.48, "Sales Channel": "Offline", "Total Revenue": 226716.1, "Order Priority": "C"}]
    }
    res = generate_insights(metadata)
    
    print(type(res))
    
    print(res)

    # py -m src.llm.insights_generator