import { useState, useEffect } from "react";
import { fetchQueue, approveQueueItem, rejectQueueItem } from "../api";
import RiskBadge from "../components/RiskBadge";
import IntentBadge from "../components/IntentBadge";

const USER_EMAIL = "glitchmybrain@gmail.com"; // same email as Inbox.jsx

export default function Queue() {
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState(null);
  const [resolved, setResolved] = useState({});

  useEffect(() => {
    fetchQueue(USER_EMAIL)
      .then((data) => {
        setQueue(data.queue || []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  async function handleApprove(item) {
    setActionLoading(item.email_id);
    try {
      const result = await approveQueueItem(item.email_id, USER_EMAIL);
      setResolved((prev) => ({
        ...prev,
        [item.email_id]: { action: "approved", draft: result.draft },
      }));
    } catch (err) {
      console.error(err);
    }
    setActionLoading(null);
  }

  async function handleReject(item) {
    setActionLoading(item.email_id);
    try {
      await rejectQueueItem(item.email_id, USER_EMAIL);
      setResolved((prev) => ({
        ...prev,
        [item.email_id]: { action: "rejected" },
      }));
    } catch (err) {
      console.error(err);
    }
    setActionLoading(null);
  }

  if (loading) return (
    <div style={{ color: "#888", fontSize: "14px" }}>Loading queue...</div>
  );

  if (error) return (
    <div style={{ color: "#ef4444", fontSize: "14px" }}>Error: {error}</div>
  );

  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: "24px" }}>
        <h1 style={{ fontSize: "22px", fontWeight: "600", color: "#fff" }}>
          Approval Queue
        </h1>
        <p style={{ color: "#666", fontSize: "13px", marginTop: "4px" }}>
          {queue.filter(i => !resolved[i.email_id]).length} items awaiting your review
        </p>
      </div>

      {/* Empty state */}
      {queue.length === 0 && (
        <div style={{
          backgroundColor: "#111", border: "1px solid #1e1e1e",
          borderRadius: "12px", padding: "40px",
          textAlign: "center", color: "#555", fontSize: "14px"
        }}>
          ✅ Queue is empty — no pending items
        </div>
      )}

      {/* Queue items */}
      <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
        {queue.map((item) => {
          const resolution = resolved[item.email_id];

          return (
            <div
              key={item.email_id}
              style={{
                backgroundColor: "#111",
                border: `1px solid ${
                  resolution?.action === "approved" ? "#22c55e33" :
                  resolution?.action === "rejected" ? "#ef444433" :
                  "#1e1e1e"
                }`,
                borderRadius: "12px",
                padding: "20px",
                opacity: resolution ? 0.7 : 1,
              }}
            >
              {/* Top row */}
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "12px" }}>
                <div>
                  <div style={{ display: "flex", gap: "6px", marginBottom: "8px" }}>
                    <IntentBadge intent={item.intent} />
                    <RiskBadge level={item.risk_level} />
                  </div>
                  <div style={{ fontSize: "15px", fontWeight: "600", color: "#fff", marginBottom: "4px" }}>
                    {item.subject}
                  </div>
                  <div style={{ fontSize: "12px", color: "#666" }}>
                    {item.sender}
                  </div>
                </div>

                {/* Resolution badge */}
                {resolution && (
                  <span style={{
                    padding: "4px 10px", borderRadius: "6px", fontSize: "12px", fontWeight: "500",
                    backgroundColor: resolution.action === "approved" ? "#052e16" : "#2d0a0a",
                    color: resolution.action === "approved" ? "#22c55e" : "#ef4444",
                    border: `1px solid ${resolution.action === "approved" ? "#22c55e33" : "#ef444433"}`,
                  }}>
                    {resolution.action === "approved" ? "✓ Approved" : "✗ Rejected"}
                  </span>
                )}
              </div>

              {/* Snippet */}
              <div style={{
                fontSize: "13px", color: "#888", lineHeight: "1.6",
                marginBottom: "12px", padding: "10px 12px",
                backgroundColor: "#0d0d0d", borderRadius: "8px"
              }}>
                {item.snippet}
              </div>

              {/* Risk reason */}
              <div style={{ fontSize: "12px", color: "#555", marginBottom: "16px" }}>
                ⚡ {item.risk_reason}
              </div>

              {/* Draft if available */}
              {item.draft && (
                <div style={{
                  backgroundColor: "#0d1a0d", border: "1px solid #22c55e22",
                  borderRadius: "8px", padding: "12px", marginBottom: "16px",
                  fontSize: "13px", color: "#aaa", lineHeight: "1.6"
                }}>
                  <div style={{ fontSize: "11px", color: "#22c55e", marginBottom: "8px" }}>
                    AI DRAFT — review before sending
                  </div>
                  {item.draft}
                </div>
              )}

              {/* Approved draft */}
              {resolution?.action === "approved" && resolution.draft && (
                <div style={{
                  backgroundColor: "#0d1a0d", border: "1px solid #22c55e44",
                  borderRadius: "8px", padding: "12px", marginBottom: "16px",
                  fontSize: "13px", color: "#aaa", lineHeight: "1.6"
                }}>
                  <div style={{ fontSize: "11px", color: "#22c55e", marginBottom: "8px" }}>
                    ✓ APPROVED DRAFT — copy and send manually
                  </div>
                  {resolution.draft}
                </div>
              )}

              {/* Action buttons */}
              {!resolution && (
                <div style={{ display: "flex", gap: "8px" }}>
                  <button
                    onClick={() => handleApprove(item)}
                    disabled={actionLoading === item.email_id}
                    style={{
                      flex: 1, padding: "10px",
                      backgroundColor: "#1e3a1e",
                      color: "#22c55e",
                      border: "1px solid #22c55e33",
                      borderRadius: "8px", fontSize: "13px",
                      fontWeight: "500", cursor: "pointer",
                    }}
                  >
                    {actionLoading === item.email_id ? "Processing..." : "✓ Approve"}
                  </button>
                  <button
                    onClick={() => handleReject(item)}
                    disabled={actionLoading === item.email_id}
                    style={{
                      flex: 1, padding: "10px",
                      backgroundColor: "#2d0a0a",
                      color: "#ef4444",
                      border: "1px solid #ef444433",
                      borderRadius: "8px", fontSize: "13px",
                      fontWeight: "500", cursor: "pointer",
                    }}
                  >
                    {actionLoading === item.email_id ? "Processing..." : "✗ Reject"}
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}