README.md
# 📦 ParcelPilot AI Agent

## 🚀 AI-Powered Customer Support Assistant

ParcelPilot AI Agent is an AI-powered customer support application that helps users quickly retrieve information about customer accounts, orders, support tickets, and related knowledge sources.

The application includes a React frontend and FastAPI backend with account-level access control and a secure escalation workflow.

---

## ✨ Features

- 🤖 AI-powered customer support agent
- 🏢 Account information lookup
- 📦 Order information lookup
- 🎫 Support ticket lookup
- 📚 Knowledge/document retrieval
- 🔐 Account-level access control
- 👤 Role-based access control
- 🔄 Backend health monitoring
- 🕒 Recent query history
- ⚡ Quick action buttons
- ⏳ Loading state handling
- ⚠️ Error handling
- 🗑️ Clear results and history
- 🚨 Ticket escalation workflow
- 📝 Custom escalation reason
- ✅ Explicit user confirmation before escalation creation
- 📋 Escalation management API
- 📱 Responsive user interface

---

# 🏗️ Architecture

```text
User
  │
  ▼
React + Vite Frontend
  │
  │ REST API
  ▼
FastAPI Backend
  │
  ├── AI Agent Service
  ├── Data Service
  ├── Access Control
  ├── Knowledge Retrieval
  └── Escalation Service
🛠️ Tech Stack
Frontend
React
Vite
JavaScript
CSS
Fetch API
Backend
Python
FastAPI
Pydantic
Uvicorn
📂 Project Structure
ParcelPilot-AI-Agent/
│
├── backend/
│   ├── main.py
│   ├── data_service.py
│   ├── agent_service.py
│   ├── access_control.py
│   └── escalation_service.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   │
│   ├── package.json
│   └── ...
│
├── README.md
└── requirements.txt
⚙️ Backend Setup
1. Clone the Repository
git clone <your-repository-url>

Move into the project folder:

cd ParcelPilot-AI-Agent
2. Create Virtual Environment

Windows:

python -m venv venv

Activate the virtual environment:

venv\Scripts\activate
3. Install Backend Dependencies
pip install -r requirements.txt

If requirements.txt is not available, install manually:

pip install fastapi uvicorn pydantic
4. Run the Backend

From the project root, run:

uvicorn backend.main:app --reload

The backend will run on:

http://127.0.0.1:8000
🩺 Backend Health Check

Open:

http://127.0.0.1:8000/health

Expected response:

{
  "status": "healthy"
}
📖 API Documentation

FastAPI automatically provides API documentation.

Open:

http://127.0.0.1:8000/docs

You can test the APIs directly from Swagger UI.

🎨 Frontend Setup

Open a new terminal and move to the frontend folder:

cd frontend

Install dependencies:

npm install

Run the frontend:

npm run dev

The frontend will display a URL similar to:

http://localhost:5173

Open that URL in your browser.

🔗 API Connection

The frontend communicates with the backend using:

http://127.0.0.1:8000

Main API endpoint:

POST /ask

Example request:

{
  "question": "Tell me details about ACCT-001"
}
🔐 Access Control

ParcelPilot AI Agent includes account-level access control.

Internal Users

Internal users can access customer data across accounts.

Example:

support_admin
Customer Users

Customer users can only access data belonging to their own account.

Unauthorized access returns:

403 Forbidden
🚨 Escalation Workflow

The project uses a confirmation-based escalation process to prevent accidental state-changing actions.

Step 1: Prepare Escalation
POST /prepare-escalation

The escalation is prepared but not created.

Step 2: User Confirmation

The user reviews:

Ticket ID
Escalation reason
Escalation action

The escalation is only created after explicit confirmation.

Step 3: Confirm Escalation
POST /confirm-escalation

Example request:

{
  "ticket_id": "TKT-501",
  "reason": "Customer issue requires higher-level support.",
  "confirmed": true
}
📋 View Escalations

Internal users can view all escalations using:

GET /escalations
🧪 Testing the Application
Test Account

Ask:

Tell me details about ACCT-001
Test Order

Ask:

Tell me details about ORD-1001
Test Ticket

Ask:

Tell me details about TKT-501
Test Cancellation

Ask:

Can I cancel order ORD-1001?
Test Escalation
Search for TKT-501
Click 🚨 Escalate Ticket
Enter an escalation reason
Click Prepare & Confirm
Confirm the action
Escalation is created successfully
🖥️ Application Flow
User Question
      │
      ▼
React Frontend
      │
      ▼
FastAPI Backend
      │
      ▼
AI Agent / Context Builder
      │
      ├── Account Lookup
      ├── Order Lookup
      ├── Ticket Lookup
      └── Knowledge Retrieval
      │
      ▼
Access Control Validation
      │
      ▼
Generate Response
      │
      ▼
Display Result in Frontend
🔒 Secure Action Flow
User Opens Ticket
      │
      ▼
Clicks Escalate Ticket
      │
      ▼
Enters Escalation Reason
      │
      ▼
Prepare Escalation
      │
      ▼
User Confirmation
      │
      ├── Cancel
      │
      └── Confirm
            │
            ▼
     Create Escalation
📸 Screenshots

Add your project screenshots here.

Example:

![ParcelPilot Dashboard](screenshots/dashboard.png)

You can create a screenshots folder and add images such as:

screenshots/
├── dashboard.png
├── ticket-details.png
└── escalation.png
🔮 Future Improvements
JWT authentication
Database integration
Real LLM integration
User login system
Persistent query history
Escalation database storage
Admin dashboard
Email notifications
Docker deployment
Cloud deployment
Unit and integration testing
👨‍💻 Author

Dhruv Dubey

B.Tech Computer Science Engineering | 2026