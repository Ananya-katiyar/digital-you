const cards = [
  { title: 'Inbox', description: 'View emails with AI risk classification', href: '/inbox', icon: '📧', color: '#1a1a2e' },
  { title: 'Approval Queue', description: 'Review and approve medium-risk replies', href: '/queue', icon: '⏳', color: '#1a2e1a' },
  { title: 'Decision Log', description: 'Full audit trail of every AI decision', href: '/decisions', icon: '📋', color: '#2e1a1a' },
  { title: 'Profile', description: 'Manage tone, AFK mode and rules', href: '/profile', icon: '⚙️', color: '#1a1a1a' },
]

export default function Home() {
  return (
    <div>
      <div style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '28px', fontWeight: '600', color: '#fff' }}>Heyy Ananyaa, Good to see you!🎀</h1>
        <p style={{ color: '#666', marginTop: '8px', fontSize: '14px' }}>
          Your AI representative is active and monitoring your inbox.
        </p>
      </div>

      <div style={{
        backgroundColor: '#111', border: '1px solid #222',
        borderRadius: '12px', padding: '16px 20px',
        marginBottom: '32px', display: 'flex', alignItems: 'center', gap: '8px'
      }}>
        <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#22c55e' }} />
        <span style={{ fontSize: '13px', color: '#888' }}>
          Digital You is active — risk engine running, queue monitored
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
        {cards.map((card) => (
          <a key={card.href} href={card.href} style={{ textDecoration: 'none' }}>
            <div style={{
              backgroundColor: card.color, border: '1px solid #222',
              borderRadius: '12px', padding: '24px', cursor: 'pointer',
            }}>
              <div style={{ fontSize: '28px', marginBottom: '12px' }}>{card.icon}</div>
              <div style={{ fontSize: '16px', fontWeight: '500', color: '#fff', marginBottom: '6px' }}>{card.title}</div>
              <div style={{ fontSize: '13px', color: '#666' }}>{card.description}</div>
            </div>
          </a>
        ))}
      </div>
    </div>
  )
}