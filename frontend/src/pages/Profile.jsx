import { useState, useEffect } from "react";
import { fetchProfile, updateProfile } from "../api";

const USER_EMAIL = "glitchmybrain@gmail.com"; // same email as before

const TONE_OPTIONS = ["professional", "casual", "formal", "friendly"];

const RULE_PRESETS = [
  { description: "Don't schedule after 6 PM", rule_type: "time_based", condition: "after_6pm", action: "escalate" },
  { description: "Don't schedule after 8 PM", rule_type: "time_based", condition: "after_8pm", action: "escalate" },
  { description: "Escalate HR topics", rule_type: "topic_based", condition: "hr_topics", action: "escalate" },
  { description: "Escalate legal topics", rule_type: "topic_based", condition: "legal", action: "escalate" },
  { description: "Escalate financial topics", rule_type: "topic_based", condition: "financial", action: "escalate" },
];

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState(null);

  // Local editable state
  const [tone, setTone] = useState("professional");
  const [afkMode, setAfkMode] = useState(false);
  const [rules, setRules] = useState([]);

  useEffect(() => {
    fetchProfile(USER_EMAIL)
      .then((data) => {
        setProfile(data);
        setTone(data.preferences?.tone || "professional");
        setAfkMode(data.preferences?.afk_mode || false);
        setRules(data.preferences?.rules || []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  async function handleSave() {
    setSaving(true);
    setSaved(false);
    try {
      await updateProfile(USER_EMAIL, {
        tone,
        afk_mode: afkMode,
        rules,
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      setError(err.message);
    }
    setSaving(false);
  }

  function addRule(preset) {
    const already = rules.some((r) => r.condition === preset.condition);
    if (!already) setRules([...rules, preset]);
  }

  function removeRule(condition) {
    setRules(rules.filter((r) => r.condition !== condition));
  }

  if (loading) return (
    <div style={{ color: "#888", fontSize: "14px" }}>Loading profile...</div>
  );

  if (error) return (
    <div style={{ color: "#ef4444", fontSize: "14px" }}>Error: {error}</div>
  );

  return (
    <div style={{ maxWidth: "680px" }}>
      {/* Header */}
      <div style={{ marginBottom: "32px" }}>
        <h1 style={{ fontSize: "22px", fontWeight: "600", color: "#fff" }}>
          Profile & Preferences
        </h1>
        <p style={{ color: "#666", fontSize: "13px", marginTop: "4px" }}>
          Control how your AI representative behaves
        </p>
      </div>

      {/* Email display */}
      <div style={{
        backgroundColor: "#111", border: "1px solid #1e1e1e",
        borderRadius: "10px", padding: "16px 20px", marginBottom: "16px",
        display: "flex", alignItems: "center", gap: "12px"
      }}>
        <div style={{ width: "36px", height: "36px", borderRadius: "50%", backgroundColor: "#1e1e1e", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "16px" }}>
          👤
        </div>
        <div>
          <div style={{ fontSize: "14px", fontWeight: "500", color: "#fff" }}>{USER_EMAIL}</div>
          <div style={{ fontSize: "12px", color: "#555" }}>Connected via Google OAuth</div>
        </div>
      </div>

      {/* Tone selector */}
      <div style={{
        backgroundColor: "#111", border: "1px solid #1e1e1e",
        borderRadius: "10px", padding: "20px", marginBottom: "16px"
      }}>
        <div style={{ fontSize: "13px", fontWeight: "500", color: "#fff", marginBottom: "4px" }}>
          Reply Tone
        </div>
        <div style={{ fontSize: "12px", color: "#555", marginBottom: "14px" }}>
          How your AI representative sounds when drafting replies
        </div>
        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
          {TONE_OPTIONS.map((t) => (
            <button
              key={t}
              onClick={() => setTone(t)}
              style={{
                padding: "8px 16px", borderRadius: "8px",
                border: "1px solid",
                fontSize: "13px", fontWeight: "500",
                cursor: "pointer", textTransform: "capitalize",
                backgroundColor: tone === t ? "#1e3a1e" : "#0d0d0d",
                borderColor: tone === t ? "#22c55e" : "#2a2a2a",
                color: tone === t ? "#22c55e" : "#666",
              }}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* AFK Mode toggle */}
      <div style={{
        backgroundColor: "#111", border: "1px solid #1e1e1e",
        borderRadius: "10px", padding: "20px", marginBottom: "16px",
        display: "flex", justifyContent: "space-between", alignItems: "center"
      }}>
        <div>
          <div style={{ fontSize: "13px", fontWeight: "500", color: "#fff", marginBottom: "4px" }}>
            AFK Mode
          </div>
          <div style={{ fontSize: "12px", color: "#555" }}>
            When active, all non-low risk emails are queued automatically
          </div>
        </div>
        <button
          onClick={() => setAfkMode(!afkMode)}
          style={{
            width: "48px", height: "26px",
            borderRadius: "13px", border: "none",
            cursor: "pointer", position: "relative",
            backgroundColor: afkMode ? "#22c55e" : "#2a2a2a",
            transition: "background-color 0.2s ease",
            flexShrink: 0,
          }}
        >
          <div style={{
            width: "20px", height: "20px",
            borderRadius: "50%", backgroundColor: "#fff",
            position: "absolute", top: "3px",
            left: afkMode ? "25px" : "3px",
            transition: "left 0.2s ease",
          }} />
        </button>
      </div>

      {/* Rule engine */}
      <div style={{
        backgroundColor: "#111", border: "1px solid #1e1e1e",
        borderRadius: "10px", padding: "20px", marginBottom: "24px"
      }}>
        <div style={{ fontSize: "13px", fontWeight: "500", color: "#fff", marginBottom: "4px" }}>
          Personal Rules
        </div>
        <div style={{ fontSize: "12px", color: "#555", marginBottom: "16px" }}>
          Rules override the default risk classification
        </div>

        {/* Active rules */}
        {rules.length > 0 && (
          <div style={{ marginBottom: "16px", display: "flex", flexDirection: "column", gap: "8px" }}>
            {rules.map((rule) => (
              <div
                key={rule.condition}
                style={{
                  display: "flex", justifyContent: "space-between",
                  alignItems: "center", padding: "10px 12px",
                  backgroundColor: "#0d0d0d", borderRadius: "8px",
                  border: "1px solid #1e1e1e"
                }}
              >
                <div>
                  <div style={{ fontSize: "13px", color: "#fff" }}>{rule.description}</div>
                  <div style={{ fontSize: "11px", color: "#555", marginTop: "2px" }}>
                    {rule.rule_type} · {rule.action}
                  </div>
                </div>
                <button
                  onClick={() => removeRule(rule.condition)}
                  style={{
                    background: "none", border: "none",
                    color: "#555", cursor: "pointer",
                    fontSize: "16px", padding: "4px 8px",
                  }}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Add rule presets */}
        <div style={{ fontSize: "11px", color: "#444", marginBottom: "8px" }}>
          ADD RULE
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
          {RULE_PRESETS.filter(
            (p) => !rules.some((r) => r.condition === p.condition)
          ).map((preset) => (
            <button
              key={preset.condition}
              onClick={() => addRule(preset)}
              style={{
                padding: "8px 12px", borderRadius: "8px",
                border: "1px dashed #2a2a2a",
                backgroundColor: "transparent",
                color: "#555", fontSize: "12px",
                cursor: "pointer", textAlign: "left",
              }}
            >
              + {preset.description}
            </button>
          ))}
        </div>
      </div>

      {/* Save button */}
      <button
        onClick={handleSave}
        disabled={saving}
        style={{
          width: "100%", padding: "12px",
          backgroundColor: saved ? "#052e16" : "#1e3a1e",
          color: saved ? "#22c55e" : "#22c55e",
          border: `1px solid ${saved ? "#22c55e" : "#22c55e33"}`,
          borderRadius: "10px", fontSize: "14px",
          fontWeight: "500", cursor: saving ? "not-allowed" : "pointer",
        }}
      >
        {saving ? "Saving..." : saved ? "✓ Saved!" : "Save Preferences"}
      </button>
    </div>
  );
}