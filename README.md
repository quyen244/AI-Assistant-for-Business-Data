<p align="center">
  <a href="https://www.uit.edu.vn/" title="University of Information Technology" style="border: none;">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="University of Information Technology (UIT)">
  </a>
</p>

<h1 align="center"><b>SE363.Q12 - AI Assistant for Business Data</b></h1>

# **SE363 Personal Project: AI Assistant for Business Data (AABD)**

> This project focuses on building an **Intelligent Data Query System** that leverages Large Language Models (LLMs) to convert natural language questions into SQL queries. The system automatically analyzes business data and returns actionable insights, enabling efficient business intelligence and data exploration without requiring SQL expertise.
> 
> **Technical Highlights:** Integration of **LangChain** for LLM orchestration, **FastAPI** for production-ready REST API, **SQLAlchemy** for database abstraction, and **Streamlit** for interactive data exploration. Supports multiple LLM providers (OpenAI GPT and Google Gemini) for maximum flexibility.

<p align="center">
  <img src="https://github.com/quyen244/AI-Assistant-for-Business-Data/raw/master/docs/architecture.png" width="600" alt="System Architecture Diagram">
</p>

---

## **Team Information**

| No. | Student ID | Full Name | Role | Github | Email |
| --- | --- | --- | --- | --- | --- |
| 1 | 23521329 | Nguyen Van Quyen | Developer | [quyen244](https://github.com/quyen244) | 23521329@gm.uit.edu.vn |

---

## **Table of Contents**

* [Overview](#overview)
* [System Architecture](#system-architecture)
* [Tech Stack](#tech-stack)
* [Database Schema](#database-schema)
* [Features](#features)
* [Repository Structure](#repository-structure)
* [Installation & Usage](#installation--usage)
* [API Documentation](#api-documentation)
* [Example Queries](#example-queries)
* [Contributing](#contributing)
* [License](#license)

---

## **Overview**

The **AI Assistant for Business Data (AABD)** is an intelligent system that bridges the gap between business users and data. Users can ask questions in natural language, and the system automatically:

1. **Understands** the intent of the question using advanced LLMs
2. **Generates** appropriate SQL queries to fetch relevant data
3. **Executes** queries against the database
4. **Presents** results with meaningful insights and visualizations

### **Problem Statement**
Traditional business intelligence tools require users to know SQL query syntax. This creates a barrier for non-technical stakeholders who need data-driven insights. AABD eliminates this barrier by allowing users to ask questions in plain English (or any natural language).

### **Solution**
By combining LangChain with state-of-the-art LLMs (GPT-4 or Gemini), the system intelligently converts natural language to SQL while maintaining data accuracy and query safety.

---

## **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│         (Streamlit Frontend / FastAPI Client)                │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   API Layer (FastAPI)                        │
│  - Query Processing Endpoints                               │
│  - Data Upload Endpoints                                    │
│  - Database Management Endpoints                            │
└────────────────────┬──────────────────────────────────────┬─┘
                     │                                        │
    ┌────────────────▼──────────────┐      ┌────────────────▼──────────────┐
    │    LLM Integration Layer       │      │   Database Layer              │
    │  - LangChain Orchestration     │      │  - SQLAlchemy ORM             │
    │  - GPT/Gemini Providers        │      │  - SQL Query Executor         │
    │  - SQL Query Generation        │      │  - Schema Management          │
    │  - Prompt Engineering          │      │                               │
    └────────────────┬───────────────┘      └────────────────┬──────────────┘
                     │                                        │
    ┌────────────────▼──────────────────────────────────────▼──────────────┐
    │              Utilities & Config Layer                                 │
    │  - Environment Configuration                                         │
    │  - Logging & Monitoring                                              │
    │  - Input Validation                                                  │
    └─────────────────────────────────────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  SQLite Database│
                    │  (Production:   │
                    │   PostgreSQL)   │
                    └─────────────────┘
```

---

## **Tech Stack**

| Category | Technology | Purpose |
| --- | --- | --- |
| **LLM Framework** | LangChain | LLM orchestration and chaining |
| **Language Models** | OpenAI GPT, Google Gemini | Natural language understanding |
| **Backend Framework** | FastAPI | REST API server |
| **Frontend Framework** | Streamlit | Interactive dashboard |
| **Web Server** | Uvicorn | ASGI server |
| **Database** | SQLite/PostgreSQL | Data storage and querying |
| **ORM** | SQLAlchemy | Database abstraction layer |
| **Data Processing** | Pandas, NumPy | Data manipulation |
| **Configuration** | python-dotenv | Environment variable management |
| **Validation** | Pydantic | Request/response validation |
| **Logging** | Python logging | System monitoring |
| **Testing** | pytest | Unit and integration tests |
| **Documentation** | Sphinx | API documentation |

---

## **Database Schema**

The system uses a flexible SQLite database that can be configured for various business domains. Default schema includes:

### **Products Table**
```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10, 2),
    cost DECIMAL(10, 2),
    created_at TIMESTAMP
);
```

### **Sales Table**
```sql
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity INTEGER,
    sale_date DATE,
    revenue DECIMAL(12, 2),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

### **Customers Table**
```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(255),
    email VARCHAR(255),
    country VARCHAR(100),
    registration_date DATE
);
```

See [docs/DATABASE.md](docs/DATABASE.md) for detailed schema documentation.

---

## **Features**

✅ **Natural Language to SQL Conversion** - Ask questions in English, get SQL queries  
✅ **Multi-LLM Support** - Seamlessly switch between OpenAI GPT and Google Gemini  
✅ **Data Upload** - Import CSV/Excel files as database tables  
✅ **Query Execution** - Safely execute generated SQL with sandboxing  
✅ **Results Visualization** - Interactive charts and tables  
✅ **Query History** - Track and manage previous queries  
✅ **Database Management** - Create, modify, and manage database schemas  
✅ **API-First Design** - RESTful API for programmatic access  
✅ **Logging & Monitoring** - Comprehensive system logging  
✅ **Error Handling** - User-friendly error messages with suggestions  

---

## **Repository Structure**

```
AI Assistant for Business Data/
├── src/                                 # Source code
│   ├── __init__.py
│   ├── llm/                            # LLM integration modules
│   │   ├── __init__.py
│   │   ├── llm_client.py               # Unified LLM provider interface
│   │   ├── sql_generator.py            # Natural language to SQL conversion
│   │   └── prompt_templates.py         # Reusable prompt templates
│   ├── database/                       # Database layer
│   │   ├── __init__.py
│   │   ├── schema.py                   # SQLAlchemy models
│   │   ├── connection.py               # Database connection handler
│   │   └── queries.py                  # Database query helpers
│   ├── api/                            # FastAPI backend
│   │   ├── __init__.py
│   │   ├── main.py                     # Main FastAPI application
│   │   ├── routes.py                   # API endpoint definitions
│   │   └── models.py                   # Pydantic request/response models
│   ├── frontend/                       # Streamlit frontend
│   │   ├── __init__.py
│   │   └── streamlit_app.py            # Main Streamlit application
│   └── utils/                          # Utility modules
│       ├── __init__.py
│       ├── config.py                   # Configuration management
│       ├── logger.py                   # Logging setup
│       └── validators.py               # Input validation functions
├── config/                             # Configuration files
│   ├── __init__.py
│   └── settings.py                     # Application settings
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── test_llm.py                    # LLM module tests
│   ├── test_database.py               # Database module tests
│   └── test_api.py                    # API endpoint tests
├── data/                               # Sample/test data
│   └── sample_data.csv                # Sample CSV for testing
├── docs/                               # Documentation
│   ├── API.md                         # API documentation
│   ├── ARCHITECTURE.md                # Detailed architecture
│   └── DATABASE.md                    # Database documentation
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

## **Installation & Usage**

### **Prerequisites**
- Python 3.8+ 
- pip or conda
- API keys for at least one LLM provider (OpenAI GPT or Google Gemini)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/quyen244/AI-Assistant-for-Business-Data.git
cd "AI Assistant for Business Data"
```

### **Step 2: Create Virtual Environment**
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n aabd python=3.10
conda activate aabd
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Configure Environment Variables**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your configuration
# Add your API keys and database settings
nano .env  # or use your preferred editor
```

### **Step 5: Initialize Database**
```bash
# Create database and tables
python -m src.database.connection
```

### **Step 6: Run the Application**

#### **Option A: FastAPI Server + Streamlit Frontend**
```bash
# Terminal 1: Start FastAPI server
python -m uvicorn src.api.main:app --reload --port 8000

# Terminal 2: Start Streamlit dashboard
streamlit run src/frontend/streamlit_app.py
```

#### **Option B: Streamlit Only (Recommended for Development)**
```bash
streamlit run src/frontend/streamlit_app.py
```

The application will be available at:
- **Streamlit Dashboard**: `http://localhost:8501`
- **FastAPI Server**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`

---

## **API Documentation**

### **Query Endpoint**
```http
POST /api/v1/query
Content-Type: application/json

{
  "question": "What is my revenue last month?",
  "llm_provider": "gpt-4",
  "table_context": "sales, products"
}
```

**Response:**
```json
{
  "question": "What is my revenue last month?",
  "generated_sql": "SELECT SUM(revenue) FROM sales WHERE MONTH(sale_date) = MONTH(CURRENT_DATE) - 1;",
  "results": [
    {"revenue": 125000.50}
  ],
  "execution_time": 0.234
}
```

### **Data Upload Endpoint**
```http
POST /api/v1/upload
Content-Type: multipart/form-data

file: <CSV_FILE>
table_name: products
```

See [docs/API.md](docs/API.md) for complete API documentation.

---

## **Example Queries**

The system handles various types of business queries:

### **Revenue Queries**
- "What is my revenue last month?"
- "Which product has the highest profit?"
- "Show total sales by category"

### **Trend Analysis**
- "What is the sales trend over the last year?"
- "Which products are declining in sales?"
- "Show monthly growth rate"

### **Customer Insights**
- "How many customers are from the US?"
- "Which customers have the highest lifetime value?"
- "Show customer distribution by country"

### **Complex Analysis**
- "Find the profit margin for each product category"
- "Show top 5 products by revenue and their growth rates"
- "Identify products with high sales but low profit"

---

## **Contributing**

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a pull request

---

## **License**

This project is licensed under the MIT License - see LICENSE file for details.

---

## **Contact & Support**

For questions or issues, please contact:
- **Developer**: Nguyen Van Quyen
- **Email**: 23521329@gm.uit.edu.vn
- **GitHub**: [quyen244](https://github.com/quyen244)

---

**Last Updated**: March 5, 2026  
**Status**: 🚀 Active Development
