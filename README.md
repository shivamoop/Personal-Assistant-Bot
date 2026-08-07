# AI Sales Orchestrator

An intelligent, multi-agent conversational AI system built with **n8n**, **Streamlit**, and **LangChain**. 

The AI Sales Orchestrator acts as a highly specialized business intelligence assistant. It uses a Master Orchestrator Agent to intelligently route user queries to four specialized sub-agents (Date-Wise, Employee, Zone, and Cases). By integrating natively with Google Sheets and employing deterministic name-resolution pre-processing, it delivers lightning-fast, hallucination-free sales reports and field activity summaries.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Multi-Agent Orchestration:** A Master Agent dynamically analyzes incoming queries and delegates them to the most capable sub-agent (Date-Wise, Zone, Employee, or Cases) based on strict business logic.
- **Deterministic Name Resolution:** An ultra-fast n8n native Google Sheets & Javascript pre-processor intercepts queries to perfectly resolve employee names *before* they reach the AI. It prevents hallucinations and automatically handles name collisions (e.g., asking for "Rahul" when two exist).
- **Persistent Conversational Memory:** Seamlessly passes Streamlit Session IDs throughout the entire n8n node ecosystem, ensuring all sub-agents share a unified "hive mind" memory for flawless follow-up questions.
- **Live Google Sheets Integration:** Fetches real-time case volumes, target metrics, and daily field activity directly from the master trackolap database.

## Architecture
1. **Frontend:** A responsive chat interface built with `Streamlit` (`streamlit_app.py`).
2. **Backend Engine:** `n8n` hosted via Docker (`docker-compose.yml`), running specialized LangChain AI nodes.
3. **LLM Provider:** OpenRouter API leveraging state-of-the-art conversational models.
4. **Database:** Google Sheets API.

## Prerequisites
Ensure you have the following installed before proceeding:
- **Docker** & **Docker Compose** (for hosting n8n)
- **Python 3.10+** (for the Streamlit frontend)
- **Node.js v18+** (Optional, for local n8n development)

## Installation

1. **Start the n8n Backend Engine**
   Navigate to the n8n Docker directory and spin up the container:
   ```bash
   cd n8n-docker
   docker-compose up -d
   ```

2. **Configure n8n Credentials**
   - Access n8n at `http://localhost:5678`.
   - Add your **OpenRouter** API key.
   - Add your **Google Sheets** credentials and ensure the Webhook node and Google Sheets native nodes are pointing to your master spreadsheet.

3. **Install Frontend Dependencies**
   ```bash
   pip install streamlit requests
   ```

## Usage

To launch the conversational AI frontend, run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

### Example Queries
- *"How many cases were done by Sachin in July?"* (Routes to Cases Agent, auto-resolves Sachin)
- *"What is the yesterday report for the South Zone?"* (Routes to Date-Wise Agent)
- *"Show me the monthly performance for Mayur."* (Routes to Employee Agent)

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.
