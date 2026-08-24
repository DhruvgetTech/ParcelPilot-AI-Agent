import { useState, useEffect } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [backendConnected, setBackendConnected] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);

  // Escalation states
  const [showEscalationBox, setShowEscalationBox] = useState(false);
  const [escalationReason, setEscalationReason] = useState("");
  const [escalationLoading, setEscalationLoading] = useState(false);
  const [escalationSuccess, setEscalationSuccess] = useState("");

  // Escalation history states
  const [escalations, setEscalations] = useState([]);
  const [showEscalations, setShowEscalations] = useState(false);
  const [escalationsLoading, setEscalationsLoading] = useState(false);

  // ================= BACKEND HEALTH CHECK =================

  const checkBackend = async () => {
    try {
      const res = await fetch(`${API_URL}/health`);
      setBackendConnected(res.ok);
    } catch {
      setBackendConnected(false);
    }
  };

  useEffect(() => {
    checkBackend();

    const interval = setInterval(() => {
      checkBackend();
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  // ================= ASK AI AGENT =================

  const sendQuestion = async (questionText) => {
    if (!questionText.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setResponse(null);
    setEscalationSuccess("");
    setShowEscalationBox(false);

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-user-id": "support_admin",
        },
        body: JSON.stringify({
          question: questionText,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data?.detail || "Failed to get response from backend."
        );
      }

      setResponse(data);
      setBackendConnected(true);

      setHistory((previousHistory) => {
        const newHistory = [
          {
            id: Date.now(),
            question: questionText,
            answer: data.answer,
          },
          ...previousHistory.filter(
            (item) =>
              item.question.toLowerCase() !==
              questionText.toLowerCase()
          ),
        ];

        return newHistory.slice(0, 5);
      });
    } catch (err) {
      setError(
        err.message ||
          "Backend connection failed. Please make sure FastAPI is running on port 8000."
      );

      setBackendConnected(false);
    } finally {
      setLoading(false);
    }
  };

  // ================= NORMAL QUESTION =================

  const askAgent = () => {
    sendQuestion(question);
  };

  const setQuickQuestion = (value) => {
    setQuestion(value);
    sendQuestion(value);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !loading) {
      askAgent();
    }
  };

  // ================= CLEAR =================

  const clearResults = () => {
    setQuestion("");
    setResponse(null);
    setError("");
    setEscalationSuccess("");
    setShowEscalationBox(false);
    setEscalationReason("");
  };

  const clearHistory = () => {
    setHistory([]);
  };

  const openHistoryItem = (historyItem) => {
    setQuestion(historyItem.question);
    sendQuestion(historyItem.question);
  };

  // ================= OPEN ESCALATION BOX =================

  const openEscalationBox = () => {
    setError("");
    setEscalationSuccess("");

    setEscalationReason(
      response?.ticket?.subject
        ? `Escalation requested for: ${response.ticket.subject}`
        : ""
    );

    setShowEscalationBox(true);
  };

  const cancelEscalation = () => {
    setShowEscalationBox(false);
    setEscalationReason("");
  };

  // ================= PREPARE ESCALATION =================

  const prepareEscalation = async () => {
    if (!response?.ticket?.ticket_id) {
      setError("No ticket available for escalation.");
      return;
    }

    if (!escalationReason.trim()) {
      setError("Please enter an escalation reason.");
      return;
    }

    setEscalationLoading(true);
    setError("");

    try {
      const res = await fetch(`${API_URL}/prepare-escalation`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-user-id": "support_admin",
        },
        body: JSON.stringify({
          ticket_id: response.ticket.ticket_id,
          reason: escalationReason,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data?.detail || "Failed to prepare escalation."
        );
      }

      const confirmed = window.confirm(
        `${data.message}\n\nTicket ID: ${data.ticket_id}\nReason: ${data.reason}\n\nDo you want to confirm and create the escalation?`
      );

      if (confirmed) {
        await confirmEscalation(
          data.ticket_id,
          data.reason
        );
      } else {
        setEscalationSuccess(
          "Escalation was prepared but cancelled before creation."
        );
      }
    } catch (err) {
      setError(
        err.message || "Failed to prepare escalation."
      );
    } finally {
      setEscalationLoading(false);
    }
  };

  // ================= CONFIRM ESCALATION =================

  const confirmEscalation = async (ticketId, reason) => {
    setEscalationLoading(true);

    try {
      const res = await fetch(`${API_URL}/confirm-escalation`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-user-id": "support_admin",
        },
        body: JSON.stringify({
          ticket_id: ticketId,
          reason: reason,
          confirmed: true,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data?.detail || "Failed to create escalation."
        );
      }

      const escalationId =
        data.escalation?.escalation_id || "N/A";

      setEscalationSuccess(
        `Escalation created successfully. Escalation ID: ${escalationId}`
      );

      setShowEscalationBox(false);
      setEscalationReason("");

      // Refresh escalation history if it is currently open
      if (showEscalations) {
        loadEscalations();
      }
    } catch (err) {
      setError(
        err.message || "Failed to create escalation."
      );
    } finally {
      setEscalationLoading(false);
    }
  };

  // ================= LOAD ESCALATIONS =================

  const loadEscalations = async () => {
    setEscalationsLoading(true);
    setError("");

    try {
      const res = await fetch(`${API_URL}/escalations`, {
        headers: {
          "x-user-id": "support_admin",
        },
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data?.detail || "Failed to load escalations."
        );
      }

      setEscalations(data.escalations || []);
      setShowEscalations(true);
    } catch (err) {
      setError(
        err.message || "Failed to load escalations."
      );
    } finally {
      setEscalationsLoading(false);
    }
  };

  // ================= CLOSE ESCALATIONS =================

  const closeEscalations = () => {
    setShowEscalations(false);
  };

  // ================= UI =================

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div className="brand">
          <div className="brand-icon">📦</div>

          <div>
            <h1>ParcelPilot AI Agent</h1>
            <p>AI-Powered Customer Support Assistant</p>
          </div>
        </div>

        <div
          className={`connection-status ${
            backendConnected
              ? "connected"
              : "disconnected"
          }`}
        >
          <span className="status-dot"></span>

          {backendConnected
            ? "Backend Connected"
            : "Backend Disconnected"}
        </div>
      </header>

      <main className="main-content">

        {/* SEARCH */}
        <section className="search-card">
          <h2>Ask ParcelPilot</h2>

          <p>
            Search account, order, ticket,
            cancellation and support information.
          </p>

          <div className="search-box">
            <input
              type="text"
              placeholder="Ask about an account, order or ticket..."
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              onKeyDown={handleKeyDown}
              disabled={loading}
            />

            <button
              onClick={askAgent}
              disabled={loading}
            >
              {loading
                ? "Thinking..."
                : "Ask Agent"}
            </button>
          </div>

          {/* QUICK ACTIONS */}
          <div className="quick-actions">

            <button
              disabled={loading}
              onClick={() =>
                setQuickQuestion(
                  "Tell me details about ACCT-001"
                )
              }
            >
              ACCT-001
            </button>

            <button
              disabled={loading}
              onClick={() =>
                setQuickQuestion(
                  "Tell me details about ORD-1001"
                )
              }
            >
              ORD-1001
            </button>

            <button
              disabled={loading}
              onClick={() =>
                setQuickQuestion(
                  "Tell me details about TKT-501"
                )
              }
            >
              TKT-501
            </button>

            <button
              disabled={loading}
              onClick={() =>
                setQuickQuestion(
                  "Can I cancel order ORD-1001?"
                )
              }
            >
              Cancel Order
            </button>

            {/* VIEW ESCALATIONS */}
            <button
              className="view-escalations-button"
              onClick={loadEscalations}
              disabled={escalationsLoading}
            >
              {escalationsLoading
                ? "Loading..."
                : "📋 View Escalations"}
            </button>

          </div>
        </section>

        {/* ERROR */}
        {error && (
          <div className="error-box">
            ⚠️ {error}
          </div>
        )}

        {/* SUCCESS */}
        {escalationSuccess && (
          <div className="success-box">
            ✅ {escalationSuccess}
          </div>
        )}

        {/* LOADING */}
        {loading && (
          <div className="loading-box">
            <div className="spinner"></div>

            <p>
              ParcelPilot AI is analyzing your request...
            </p>
          </div>
        )}

        {/* ESCALATION HISTORY */}
        {showEscalations && (
          <section className="escalations-card">

            <div className="escalations-header">
              <div>
                <h2>🚨 Escalation History</h2>
                <p>
                  Total Escalations: {escalations.length}
                </p>
              </div>

              <button
                onClick={closeEscalations}
                className="close-escalations-button"
              >
                ✖ Close
              </button>
            </div>

            {escalations.length === 0 ? (
              <p className="no-escalations">
                No escalations found.
              </p>
            ) : (
              <div className="escalations-list">

                {escalations.map((item) => (
                  <div
                    className="escalation-item"
                    key={item.escalation_id}
                  >

                    <div className="escalation-top">
                      <strong>
                        🚨 {item.escalation_id}
                      </strong>

                      <span className="escalation-status">
                        {item.status || "created"}
                      </span>
                    </div>

                    <p>
                      <strong>Ticket ID:</strong>{" "}
                      {item.ticket_id || "N/A"}
                    </p>

                    <p>
                      <strong>Reason:</strong>{" "}
                      {item.reason || "N/A"}
                    </p>

                    <p>
                      <strong>Created By:</strong>{" "}
                      {item.created_by || "N/A"}
                    </p>

                    <p>
                      <strong>Created At:</strong>{" "}
                      {item.created_at || "N/A"}
                    </p>

                  </div>
                ))}

              </div>
            )}

          </section>
        )}

        {/* RESPONSE */}
        {response && !loading && (
          <section className="response-section">

            {/* RESULT ACTIONS */}
            <div className="result-actions">

              <button onClick={clearResults}>
                🗑️ Clear Results
              </button>

              {response.ticket && (
                <button
                  className="escalate-button"
                  onClick={openEscalationBox}
                  disabled={escalationLoading}
                >
                  🚨 Escalate Ticket
                </button>
              )}

              <button
                className="view-escalations-button"
                onClick={loadEscalations}
                disabled={escalationsLoading}
              >
                {escalationsLoading
                  ? "Loading..."
                  : "📋 View Escalations"}
              </button>

            </div>

            {/* ESCALATION BOX */}
            {showEscalationBox && response.ticket && (
              <div className="escalation-card">

                <h3>🚨 Escalate Support Ticket</h3>

                <p>
                  Ticket ID:
                  <strong>
                    {" "}
                    {response.ticket.ticket_id}
                  </strong>
                </p>

                <label>
                  Escalation Reason
                </label>

                <textarea
                  value={escalationReason}
                  onChange={(e) =>
                    setEscalationReason(e.target.value)
                  }
                  placeholder="Enter the reason for escalation..."
                  rows="4"
                  disabled={escalationLoading}
                />

                <div className="escalation-actions">

                  <button
                    className="cancel-escalation-button"
                    onClick={cancelEscalation}
                    disabled={escalationLoading}
                  >
                    Cancel
                  </button>

                  <button
                    className="confirm-escalation-button"
                    onClick={prepareEscalation}
                    disabled={escalationLoading}
                  >
                    {escalationLoading
                      ? "Processing..."
                      : "Prepare & Confirm"}
                  </button>

                </div>

              </div>
            )}

            {/* AI ANSWER */}
            <div className="answer-card">
              <h2>🤖 AI Response</h2>

              <p>
                {response.answer}
              </p>
            </div>

            {/* ACCOUNT */}
            {response.account && (
              <div className="details-card">

                <h3>🏢 Account Details</h3>

                <div className="details-grid">
                  {Object.entries(
                    response.account
                  ).map(([key, value]) => (

                    <div
                      className="detail-item"
                      key={key}
                    >
                      <span>
                        {key.replaceAll("_", " ")}
                      </span>

                      <strong>
                        {String(value ?? "N/A")}
                      </strong>
                    </div>

                  ))}
                </div>

              </div>
            )}

            {/* ORDER */}
            {response.order && (
              <div className="details-card">

                <h3>📦 Order Details</h3>

                <div className="details-grid">
                  {Object.entries(
                    response.order
                  ).map(([key, value]) => (

                    <div
                      className="detail-item"
                      key={key}
                    >
                      <span>
                        {key.replaceAll("_", " ")}
                      </span>

                      <strong>
                        {String(value ?? "N/A")}
                      </strong>
                    </div>

                  ))}
                </div>

              </div>
            )}

            {/* TICKET */}
            {response.ticket && (
              <div className="details-card">

                <h3>🎫 Ticket Details</h3>

                <div className="details-grid">
                  {Object.entries(
                    response.ticket
                  ).map(([key, value]) => (

                    <div
                      className="detail-item"
                      key={key}
                    >
                      <span>
                        {key.replaceAll("_", " ")}
                      </span>

                      <strong>
                        {String(value ?? "N/A")}
                      </strong>
                    </div>

                  ))}
                </div>

              </div>
            )}

            {/* KNOWLEDGE SOURCES */}
            {response.knowledge_sources?.length > 0 && (
              <div className="knowledge-card">

                <h3>📚 Knowledge Sources</h3>

                {response.knowledge_sources.map(
                  (item, index) => (

                    <div
                      className="knowledge-item"
                      key={`${item.filename}-${index}`}
                    >
                      <span>
                        📄 {item.filename}
                      </span>

                      <span className="score">
                        Relevance: {item.score}
                      </span>
                    </div>

                  )
                )}

              </div>
            )}

          </section>
        )}

        {/* QUERY HISTORY */}
        {history.length > 0 && (
          <section className="history-card">

            <div className="history-header">

              <h3>🕒 Recent Queries</h3>

              <button onClick={clearHistory}>
                Clear History
              </button>

            </div>

            <div className="history-list">

              {history.map((item) => (

                <button
                  key={item.id}
                  className="history-item"
                  onClick={() =>
                    openHistoryItem(item)
                  }
                  disabled={loading}
                >
                  <strong>
                    {item.question}
                  </strong>

                  <span>
                    {item.answer}
                  </span>
                </button>

              ))}

            </div>

          </section>
        )}

      </main>
    </div>
  );
}

export default App;