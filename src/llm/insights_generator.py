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
        'nu'
        "columns":	["Region", "Country", "Item Type", "Sales Channel", "Order Priority", "Order Date", "Order ID", "Ship Date", "Units Sold", "Unit Price", "Unit Cost", "Total Revenue", "Total Cost", "Total Profit"],
        "num_rows" : 1330,
        "statistics" :	{"numeric": {"Order ID": {"max": 999879729, "min": 100640618, "std": 257388211.81845534, "mean": 541204760.2428571}, "Unit Cost": {"max": 524.96, "min": 6.92, "std": 176.15887275845554, "mean": 187.2468120300752}, "Total Cost": {"max": 5248025.12, "min": 373.68, "std": 1134845.4635111452, "mean": 903719.0599924811}, "Unit Price": {"max": 668.27, "min": 9.33, "std": 217.32345951945007, "mean": 264.89354135338345}, "Units Sold": {"max": 9999, "min": 2, "std": 2904.105430440249, "mean": 4949.114285714286}, "Total Profit": {"max": 1700448.6, "min": 130.14, "std": 368983.2804269547, "mean": 377200.0363308271}, "Total Revenue": {"max": 6672675.95, "min": 503.82, "std": 1443064.5488383293, "mean": 1280919.0963233083}}, "categorical": {"Region": {"top_values": {"Europe": 1330}, "unique_values": 1}, "Country": {"top_values": {"Kosovo": 35, "Andorra": 40, "Romania": 34, "San Marino": 40, "Bosnia and Herzegovina": 33}, "unique_values": 48}, "Item Type": {"top_values": {"Beverages": 121, "Cosmetics": 114, "Vegetables": 114, "Personal Care": 115, "Office Supplies": 123}, "unique_values": 12}, "Ship Date": {"top_values": {"11/3/2012": 3, "3/21/2013": 3, "3/27/2017": 3, "4/11/2013": 3, "5/30/2014": 3}, "unique_values": 1070}, "Order Date": {"top_values": {"1/6/2012": 3, "1/16/2016": 4, "3/23/2012": 4, "6/10/2011": 4, "11/21/2016": 3}, "unique_values": 1049}, "Sales Channel": {"top_values": {"Online": 663, "Offline": 667}, "unique_values": 2}, "Order Priority": {"top_values": {"C": 307, "H": 335, "L": 334, "M": 354}, "unique_values": 4}}},
        "samples": [{"Region": "Europe", "Country": "Czech Republic", "Order ID": 478051030, "Item Type": "Beverages", "Ship Date": "9/29/2011", "Unit Cost": 31.79, "Order Date": "9/12/2011", "Total Cost": 151892.62, "Unit Price": 47.45, "Units Sold": 4778, "Total Profit": 74823.48, "Sales Channel": "Offline", "Total Revenue": 226716.1, "Order Priority": "C"}]
    }
    res = generate_insights(metadata)

    print(res)

    # py -m src.llm.insights_generator