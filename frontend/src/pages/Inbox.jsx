import { useState, useEffect } from "react";
import { fetchEmails, generateDraft } from "../api";
import RiskBadge from "../components/RiskBadge";
import IntentBadge from "../components/IntentBadge";

const USER_EMAIL = "glitchmybrain@gmail.com"; // replace with your Gmail

export default function Inbox() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [draft, setDraft] = useState(null);
  const [draftLoading, setDraftLoading] = useState(false);

  useEffect(() => {
    fetchEmails(USER_EMAIL)
      .then((data) => {
        setEmails(data.emails || []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  async function handleGenerateDraft(email) {
    setDraftLoading(true);
    setDraft(null);
    try {
      const result = await generateDraft(
        email.subject,
        email.snippet,
        "professional",
        USER_EMAIL
      );
      setDraft(result);
    } catch (err) {
      setDraft({ error: err.message });
    }
    setDraftLoading(false);
  }

  if (loading) return (
    <div style={{ color: "#888", fontSize: "14px" }}>Loading emails...</div>
  );

  if (error) return (
    <div style={{ color: "#ef4444", fontSize: "14px" }}>Error: {error}</div>
  );

  return (
    <div style={{ display: "flex", gap: "24px" }}>
      {/* Email list */}
      <div style={{ flex: 1 }}>
        <div style={{ marginBottom: "24px" }}>
          <h1 style={{ fontSize: "22px", fontWeight: "600", color: "#fff" }}>
            Inbox
          </h1>
          <p style={{ color: "#666", fontSize: "13px", marginTop: "4px" }}>
            {emails.length} emails analysed
          </p>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {emails.map((email) => (
            <div
              key={email.id}
              onClick={() => { setSelectedEmail(email); setDraft(null); }}
              style={{
                backgroundColor: selectedEmail?.id === email.id ? "#1a1a1a" : "#111",
                border: `1px solid ${selectedEmail?.id === email.id ? "#333" : "#1e1e1e"}`,
                borderRadius: "10px",
                padding: "14px 16px",
                cursor: "pointer",
                transition: "all 0.15s ease",
              }}
            >
              {/* Top row */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                <span style={{ fontSize: "13px", color: "#aaa", maxWidth: "200px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                  {email.sender}
                </span>
                <div style={{ display: "flex", gap: "6px", alignItems: "center" }}>
                  <IntentBadge intent={email.analysis?.intent} />
                  <RiskBadge level={email.risk?.risk_level} />
                </div>
              </div>

              {/* Subject */}
              <div style={{ fontSize: "14px", fontWeight: "500", color: "#fff", marginBottom: "4px" }}>
                {email.subject}
              </div>

              {/* Snippet */}
              <div style={{ fontSize: "12px", color: "#555", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {email.snippet}
              </div>

              {/* Risk reason */}
              {email.risk?.risk_reason && (
                <div style={{ fontSize: "11px", color: "#444", marginTop: "6px" }}>
                  ⚡ {email.risk.risk_reason}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Detail panel */}
      {selectedEmail && (
        <div style={{
          width: "380px",
          backgroundColor: "#111",
          border: "1px solid #1e1e1e",
          borderRadius: "12px",
          padding: "20px",
          height: "fit-content",
          position: "sticky",
          top: "20px",
        }}>
          <div style={{ marginBottom: "16px" }}>
            <div style={{ display: "flex", gap: "6px", marginBottom: "10px" }}>
              <IntentBadge intent={selectedEmail.analysis?.intent} />
              <RiskBadge level={selectedEmail.risk?.risk_level} />
            </div>
            <div style={{ fontSize: "15px", fontWeight: "600", color: "#fff", marginBottom: "4px" }}>
              {selectedEmail.subject}
            </div>
            <div style={{ fontSize: "12px", color: "#666" }}>
              {selectedEmail.sender}
            </div>
          </div>

          <div style={{ fontSize: "13px", color: "#aaa", lineHeight: "1.6", marginBottom: "16px" }}>
            {selectedEmail.snippet}
          </div>

          {/* Entities */}
          {selectedEmail.analysis?.entities?.length > 0 && (
            <div style={{ marginBottom: "16px" }}>
              <div style={{ fontSize: "11px", color: "#555", marginBottom: "6px" }}>DETECTED ENTITIES</div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: "4px" }}>
                {selectedEmail.analysis.entities.map((e, i) => (
                  <span key={i} style={{
                    backgroundColor: "#1a1a1a", border: "1px solid #2a2a2a",
                    borderRadius: "4px", padding: "2px 6px",
                    fontSize: "11px", color: "#888"
                  }}>
                    {e.text} · {e.label}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Risk reason */}
          <div style={{
            backgroundColor: "#0d0d0d", borderRadius: "8px",
            padding: "10px 12px", marginBottom: "16px",
            fontSize: "12px", color: "#666"
          }}>
            ⚡ {selectedEmail.risk?.risk_reason}
          </div>

          {/* Generate draft button */}
          {selectedEmail.risk?.risk_level !== "high" && (
            <button
              onClick={() => handleGenerateDraft(selectedEmail)}
              disabled={draftLoading}
              style={{
                width: "100%", padding: "10px",
                backgroundColor: draftLoading ? "#1a1a1a" : "#1e3a1e",
                color: draftLoading ? "#555" : "#22c55e",
                border: "1px solid #22c55e33",
                borderRadius: "8px", fontSize: "13px",
                fontWeight: "500", cursor: draftLoading ? "not-allowed" : "pointer",
                marginBottom: "12px",
              }}
            >
              {draftLoading ? "Generating draft..." : "✨ Generate Draft Reply"}
            </button>
          )}

          
          {/* Draft output */}
          {draft && !draft.error && (
            <div style={{
              backgroundColor: "#0d1a0d", border: "1px solid #22c55e22",
              borderRadius: "8px", padding: "12px",
              fontSize: "13px", color: "#aaa", lineHeight: "1.6"
            }}>
              <div style={{ fontSize: "11px", color: "#22c55e", marginBottom: "8px" }}>
                AI DRAFT — edit if needed, then mark as corrected
              </div>

              {/* Editable draft */}
              <textarea
                value={draft.draft}
                onChange={(e) => setDraft({ ...draft, draft: e.target.value })}
                rows={4}
                style={{
                  width: "100%", backgroundColor: "#0a150a",
                  border: "1px solid #1a2e1a", borderRadius: "6px",
                  color: "#ccc", fontSize: "13px", lineHeight: "1.6",
                  padding: "8px", resize: "vertical", fontFamily: "inherit"
                }}
              />

              {/* Save correction button */}
              <button
                onClick={async () => {
                  try {
                    await fetch(`${import.meta.env.VITE_API_URL}/learning/correct`, {
                      method: "POST",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify({
                        user_email: USER_EMAIL,
                        email_id: selectedEmail.id,
                        subject: selectedEmail.subject,
                        original_draft: draft.draft,
                        corrected_draft: draft.draft,
                        intent: draft.intent || selectedEmail.analysis?.intent,
                        tone: "professional"
                      })
                    });
                    alert("✓ Correction saved! AI will learn from this.");
                  } catch (err) {
                    console.error(err);
                  }
                }}
                style={{
                  marginTop: "8px", width: "100%",
                  padding: "7px", backgroundColor: "#1a2e1a",
                  color: "#22c55e", border: "1px solid #22c55e33",
                  borderRadius: "6px", fontSize: "12px",
                  cursor: "pointer"
                }}
              >
                💾 Save as correction — teach the AI
              </button>
            </div>
          )}

          {/* High risk warning */}
          {selectedEmail.risk?.risk_level === "high" && (
            <div style={{
              backgroundColor: "#2d0a0a", border: "1px solid #ef444433",
              borderRadius: "8px", padding: "12px",
              fontSize: "13px", color: "#ef4444"
            }}>
              🚨 High risk — no automated action taken. Review manually.
            </div>
          )}
        </div>
      )}
    </div>
  );
}