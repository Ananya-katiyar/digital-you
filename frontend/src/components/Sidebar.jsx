import { NavLink } from 'react-router-dom'

const navItems = [
  { label: 'Inbox', href: '/inbox', icon: '📧' },
  { label: 'Queue', href: '/queue', icon: '⏳' },
  { label: 'Decisions', href: '/decisions', icon: '📋' },
  { label: 'Profile', href: '/profile', icon: '⚙️' },
]

export default function Sidebar() {
  return (
    <aside style={{
      width: '220px',
      minHeight: '100vh',
      backgroundColor: '#111111',
      borderRight: '1px solid #222',
      padding: '24px 16px',
      display: 'flex',
      flexDirection: 'column',
      gap: '8px',
      position: 'fixed',
      top: 0,
      left: 0,
    }}>
      {/* Logo */}
      <div style={{ marginBottom: '32px', padding: '0 8px' }}>
        <div style={{ fontSize: '18px', fontWeight: '600', color: '#fff' }}>
          Digital You
        </div>
        <div style={{ fontSize: '11px', color: '#555', marginTop: '4px' }}>
          AI Representative
        </div>
      </div>

      {/* Nav links */}
      {navItems.map((item) => (
        <NavLink
          key={item.href}
          to={item.href}
          style={({ isActive }) => ({
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            padding: '10px 12px',
            borderRadius: '8px',
            textDecoration: 'none',
            fontSize: '14px',
            fontWeight: isActive ? '500' : '400',
            color: isActive ? '#fff' : '#888',
            backgroundColor: isActive ? '#1e1e1e' : 'transparent',
            transition: 'all 0.15s ease',
          })}
        >
          <span>{item.icon}</span>
          <span>{item.label}</span>
        </NavLink>
      ))}
    </aside>
  )
}