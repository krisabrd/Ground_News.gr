# 📰 News Aggregator & Bias Analyzer

An asynchronous, AI-powered terminal application that gathers news clusters, synthesizes coverage using Google GenAI, analyzes political spectrum bias with Scikit-learn, and renders rich interactive terminal dashboards.

---

## 📁 Repository Structure & File Overview

| File | Primary Role & Description |
| :--- | :--- |
| **`main.py`** | **Application Orchestrator**: Manages the CLI execution flow, handles asynchronous pipeline coordination, and delegates layout rendering. |
| **`fetcher.py`** | **Data Acquisition**: Handles asynchronous web requests and API integration to fetch and parse raw news cluster data. |
| **`analyzer.py`** | **Machine Learning Engine**: Implements Scikit-learn models to process news text, feature-extract themes, and map media bias spectrum distribution. |
| **`ai_service.py`** | **LLM Integration**: Interacts with the Google GenAI SDK to generate concise summaries, neutral Ground News cards, and Greek-language coverage insights. |
| **`ui.py`** | **Terminal UI Renderer**: Uses the `rich` library to build styled panels, tables, layout grids, and visual bias breakdown indicators in the CLI. |
| **`config.py`** | **Settings & Environment**: Loads application configurations, constants, and API setup using `python-dotenv`. |
| **`requirements.txt`** | **Dependencies**: Lists all external Python modules required to build and run the application. |
| **`.env`** *(ignored)* | **Secrets**: Stores private credentials such as API keys and environment variables securely. |

---

## 🛠️ Key Concepts & Tech Stack I Learned

### 1. Asynchronous Programming (`asyncio` & `async/await`)
* **Concurreny over Parallelism**: Learned how `async` and `await` allow Python to execute non-blocking I/O operations (like fetching web feeds or waiting on API responses) without freezing the main event loop.
* **Parallel Execution**: Used concurrent model calls to generate multiple news summaries simultaneously, drastically speeding up application performance.

### 2. Artificial Intelligence & LLMs (`google-genai`)
* **Google GenAI Integration**: Configured and invoked Gemini models to synthesize complex news clusters into neutral, structured summaries.
* **Structured System Prompting**: Crafted multi-step prompt guidelines to enforce concise, objective outputs and localized Greek responses.

### 3. Machine Learning & Data Science (`scikit-learn`)
* **Natural Language Processing (NLP)**: Utilized `scikit-learn` to analyze textual patterns across multi-source news articles.
* **Data Classification & Vectorization**: Formatted and processed news text to evaluate media spectrum distributions (e.g., Left, Center-Left, Center-Right, Unmapped).

### 4. Terminal User Interfaces (`rich`)
* **Modern CLI Design**: Built clean, colorful, and formatted terminal dashboards using Rich components like `Panel`, `Table`, and layout blocks.
* **Visual Data Presentation**: Visualized numerical spectrum distributions and status updates directly in the terminal window.

### 5. Environment & Configuration Management (`python-dotenv`)
* **Secure Credential Handling**: Used `python-dotenv` to load environment variables from local `.env` files.
* **Best Practices**: Ensured sensitive credentials (like Gemini API keys) are kept out of source control and project repositories.

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/krisabrd/Ground_News.gr.git](https://github.com/krisabrd/news-bias-analyzer.git)
   cd news-bias-analyzer
   
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate 

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Set up your environment variables:**
   Create a .env file in the root directory:
    GEMINI_API_KEY=your_google_genai_api_key_here

5. **Run the application:**
   ```bash
   python main.py