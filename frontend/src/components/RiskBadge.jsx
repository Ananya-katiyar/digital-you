const config = {
  low: { label: "LOW", color: "#22c55e", bg: "#052e16" },
  medium: { label: "MEDIUM", color: "#f59e0b", bg: "#2d1f00" },
  high: { label: "HIGH", color: "#ef4444", bg: "#2d0a0a" },
};

export default function RiskBadge({ level }) {
  const c = config[level] || config.low;
  return (
    <span style={{
      backgroundColor: c.bg,
      color: c.color,
      border: `1px solid ${c.color}33`,
      borderRadius: "6px",
      padding: "2px 8px",
      fontSize: "11px",
      fontWeight: "600",
      letterSpacing: "0.05em",
    }}>
      {c.label}
    </span>
  );
}