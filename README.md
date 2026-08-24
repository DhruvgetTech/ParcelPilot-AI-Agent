# 📦 ParcelPilot AI Agent

<p align="center">
  <b>AI-Powered Customer Support Assistant</b><br/>
  A secure, intelligent support application for retrieving customer, order, ticket, and knowledge-base information.
</p>

---

## 🚀 Overview

**ParcelPilot AI Agent** is an AI-powered customer support application designed to help support teams and users quickly retrieve information related to:

* Customer accounts
* Orders
* Support tickets
* Knowledge and documents
* Ticket escalations

The application provides a **React + Vite frontend** and a **FastAPI backend**, with secure access control and a confirmation-based escalation workflow.

---

## ✨ Key Features

* 🤖 AI-powered customer support assistant
* 🏢 Customer account information lookup
* 📦 Order information lookup
* 🎫 Support ticket lookup
* 📚 Knowledge and document retrieval
* 🔐 Account-level access control
* 👤 Role-based access control
* 🩺 Backend health monitoring
* 🕒 Recent query history
* ⚡ Quick action buttons
* ⏳ Loading state handling
* ⚠️ Error handling
* 🗑️ Clear results and query history
* 🚨 Secure ticket escalation workflow
* 📝 Custom escalation reason
* ✅ Explicit user confirmation before escalation
* 📋 Escalation management API
* 📱 Responsive user interface

---

# 🏗️ System Architecture

```text
                    ┌───────────────┐
                    │     User      │
                    └───────┬───────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   React + Vite Frontend │
              └────────────┬────────────┘
                           │
                        REST API
                           │
                           ▼
              ┌─────────────────────────┐
              │     FastAPI Backend     │
              └────────────┬────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    AI Agent Service   Data Service   Access Control
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
              Knowledge & Escalation Service
```

---

# 🛠️ Tech Stack

## 🎨 Frontend

* React
* Vite
* JavaScript
* CSS
* Fetch API

## ⚙️ Backend

* Python
* FastAPI
* Pydantic
* Uvicorn

---

# 📂 Project Structure

```text
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
├── screenshots/
│   ├── dashboard.png
│   ├── ticket-details.png
│   └── escalation.png
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Backend Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/DhruvgetTech/ParcelPilot-AI-Agent.git
```

Move into the project folder:

```bash
cd ParcelPilot-AI-Agent
```

---

## 2️⃣ Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install Backend Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is unavailable, install the dependencies manually:

```bash
pip install fastapi uvicorn pydantic
```

---

## 4️⃣ Run the Backend

From the project root, run:

```bash
uvicorn backend.main:app --reload
```

The backend will start at:

```text
http://127.0.0.1:8000
```

---

# 🩺 Backend Health Check

Open:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# 📖 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can test all available APIs directly from the Swagger UI.

---

# 🎨 Frontend Setup

Open a **new terminal** and navigate to the frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

The frontend will display a URL similar to:

```text
http://localhost:5173
```

Open the URL in your browser.

---

# 🔗 Frontend–Backend API Connection

The frontend communicates with the FastAPI backend using:

```text
http://127.0.0.1:8000
```

## Main API Endpoint

### `POST /ask`

Example request:

```json
{
  "question": "Tell me details about ACCT-001"
}
```

---

# 🔐 Access Control

ParcelPilot AI Agent implements **account-level access control** to protect customer information.

## 👨‍💼 Internal Users

Internal support users can access customer data across authorized accounts.

Example:

```text
support_admin
```

## 👤 Customer Users

Customer users can only access information belonging to their own account.

Unauthorized access returns:

```text
403 Forbidden
```

---

# 🚨 Secure Escalation Workflow

To prevent accidental state-changing actions, ParcelPilot uses a **confirmation-based escalation process**.

## Step 1: Prepare Escalation

```text
POST /prepare-escalation
```

The escalation is prepared but **not created yet**.

---

## Step 2: User Confirmation

The user reviews:

* Ticket ID
* Escalation reason
* Escalation action

The escalation is created only after the user gives explicit confirmation.

---

## Step 3: Confirm Escalation

```text
POST /confirm-escalation
```

Example request:

```json
{
  "ticket_id": "TKT-501",
  "reason": "Customer issue requires higher-level support.",
  "confirmed": true
}
```

---

# 📋 View Escalations

Internal users can view all escalations using:

```text
GET /escalations
```

---

# 🧪 Testing the Application

## 🏢 Test Account

Ask:

```text
Tell me details about ACCT-001
```

## 📦 Test Order

Ask:

```text
Tell me details about ORD-1001
```

## 🎫 Test Ticket

Ask:

```text
Tell me details about TKT-501
```

## ❌ Test Cancellation

Ask:

```text
Can I cancel order ORD-1001?
```

## 🚨 Test Escalation

1. Search for `TKT-501`
2. Click **🚨 Escalate Ticket**
3. Enter an escalation reason
4. Click **Prepare & Confirm**
5. Review the escalation details
6. Confirm the action
7. Escalation is created successfully

---

# 🖥️ Application Flow

```text
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
```

---

# 🔒 Secure Action Flow

```text
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
```

---

# 📸 Screenshots

Add your application screenshots inside the `screenshots` folder.

```text
screenshots/
├── dashboard.png
├── ticket-details.png
└── escalation.png
```

### Example

```markdown
![ParcelPilot Dashboard](screenshots/dashboard.png)
```

> Add actual screenshots after capturing your running application.

---

# 🔮 Future Improvements

* 🔑 JWT authentication
* 🗄️ Database integration
* 🧠 Real LLM integration
* 👤 User login and authentication system
* 🕒 Persistent query history
* 💾 Persistent escalation storage
* 📊 Admin dashboard
* 📧 Email notifications
* 🐳 Docker deployment
* ☁️ Cloud deployment
* 🧪 Unit and integration testing

---

# 👨‍💻 Author

**Dhruv Dubey**

🎓 B.Tech Computer Science Engineering
📅 Class of 2026

---

<p align="center">
  ⭐ If you found this project useful, consider giving the repository a star!
</p>
