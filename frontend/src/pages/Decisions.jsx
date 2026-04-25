import { useState, useEffect } from "react";
import { fetchDecisions } from "../api";
import RiskBadge from "../components/RiskBadge";
import IntentBadge from "../components/IntentBadge";

const USER_EMAIL = "glitchmybrain@gmail.com"; // same email as before

const ACTION_LABELS = {
  auto_draft: { label: "Auto Draft", color: "#22c55e", bg: "#052e16" },
  suggest_and_approve: { label: "Queued", color: "#f59e0b", bg: "#2d1f00" },
  escalate: { label: "Escalated", color: "#ef4444", bg: "#2d0a0a" },
};

function ActionBadge({ action }) {
  const c = ACTION_LABELS[action] || { label: action, color: "#888", bg: "#1a1a1a" };
  return (
    <span style={{
      backgroundColor: c.bg,
      color: c.color,
      border: `1px solid ${c.color}33`,
      borderRadius: "6px",
      padding: "2px 8px",
      fontSize: "11px",
      fontWeight: "600",
    }}>
      {c.label}
    </span>
  );
}

export default function Decisions() {
  const [decisions, setDecisions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchDecisions(USER_EMAIL)
      .then((data) => {
        setDecisions(data.decisions || []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const filtered = filter === "all"
    ? decisions
    : decisions.filter((d) => d.risk_level === filter);

  const counts = {
    all: decisions.length,
    low: decisions.filter((d) => d.risk_level === "low").length,
    medium: decisions.filter((d) => d.risk_level === "medium").length,
    high: decisions.filter((d) => d.risk_level === "high").length,
  };

  if (loading) return (
    <div style={{ color: "#888", fontSize: "14px" }}>Loading decisions...</div>
  );

  if (error) return (
    <div style={{ color: "#ef4444", fontSize: "14px" }}>Error: {error}</div>
  );

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: "24px" }}>
        <h1 style={{ fontSize: "22px", fontWeight: "600", color: "#fff" }}>
          Decision Log
        </h1>
        <p style={{ color: "#666", fontSize: "13px", marginTop: "4px" }}>
          Full audit trail of every AI classification decision
        </p>
      </div>

      {/* Stats row */}
      <div style={{
        display: "grid", gridTemplateColumns: "repeat(4, 1fr)",
        gap: "12px", marginBottom: "24px"
      }}>
        {[
          { label: "Total", value: counts.all, color: "#888" },
          { label: "Low Risk", value: counts.low, color: "#22c55e" },
          { label: "Medium Risk", value: counts.medium, color: "#f59e0b" },
          { label: "High Risk", value: counts.high, color: "#ef4444" },
        ].map((stat) => (
          <div key={stat.label} style={{
            backgroundColor: "#111", border: "1px solid #1e1e1e",
            borderRadius: "10px", padding: "16px",
            textAlign: "center"
          }}>
            <div style={{ fontSize: "24px", fontWeight: "700", color: stat.color }}>
              {stat.value}
            </div>
            <div style={{ fontSize: "12px", color: "#555", marginTop: "4px" }}>
              {stat.label}
            </div>
          </div>
        ))}
      </div>

      {/* Filter tabs */}
      <div style={{ display: "flex", gap: "8px", marginBottom: "20px" }}>
        {["all", "low", "medium", "high"].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            style={{
              padding: "6px 14px",
              borderRadius: "6px",
              border: "1px solid",
              fontSize: "12px",
              fontWeight: "500",
              cursor: "pointer",
              backgroundColor: filter === f ? "#1e1e1e" : "transparent",
              borderColor: filter === f ? "#333" : "#1e1e1e",
              color: filter === f ? "#fff" : "#555",
              textTransform: "capitalize",
            }}
          >
            {f} {f !== "all" && `(${counts[f]})`}
          </button>
        ))}
      </div>

      {/* Decision table */}
      {filtered.length === 0 ? (
        <div style={{
          backgroundColor: "#111", border: "1px solid #1e1e1e",
          borderRadius: "12px", padding: "40px",
          textAlign: "center", color: "#555", fontSize: "14px"
        }}>
          No decisions found for this filter
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {filtered.map((decision, index) => (
            <div
              key={index}
              style={{
                backgroundColor: "#111",
                border: "1px solid #1e1e1e",
                borderRadius: "10px",
                padding: "14px 16px",
                display: "grid",
                gridTemplateColumns: "1fr auto",
                gap: "12px",
                alignItems: "center",
              }}
            >
              {/* Left side */}
              <div>
                <div style={{ display: "flex", gap: "6px", marginBottom: "6px", alignItems: "center" }}>
                  <IntentBadge intent={decision.intent} />
                  <RiskBadge level={decision.risk_level} />
                  <ActionBadge action={decision.action} />
                </div>
                <div style={{ fontSize: "14px", fontWeight: "500", color: "#fff", marginBottom: "4px" }}>
                  {decision.subject}
                </div>
                <div style={{ fontSize: "12px", color: "#555" }}>
                  ⚡ {decision.risk_reason}
                </div>
              </div>

              {/* Right side — timestamp */}
              <div style={{ textAlign: "right", flexShrink: 0 }}>
                <div style={{ fontSize: "11px", color: "#444" }}>
                  {decision.timestamp
                    ? new Date(decision.timestamp).toLocaleString("en-IN", {
                        dateStyle: "short",
                        timeStyle: "short",
                      })
                    : "—"}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}