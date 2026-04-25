const config = {
  casual: { label: "casual", color: "#888", bg: "#1a1a1a" },
  scheduling: { label: "scheduling", color: "#60a5fa", bg: "#0d1f3c" },
  urgent: { label: "urgent", color: "#f87171", bg: "#2d0a0a" },
  promotional: { label: "promo", color: "#a78bfa", bg: "#1a0d2e" },
};

export default function IntentBadge({ intent }) {
  const c = config[intent] || config.casual;
  return (
    <span style={{
      backgroundColor: c.bg,
      color: c.color,
      borderRadius: "6px",
      padding: "2px 8px",
      fontSize: "11px",
      fontWeight: "500",
    }}>
      {c.label}
    </span>
  );
}