import { Routes, Route, Navigate } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Home from './pages/Home'
import Inbox from './pages/Inbox'
import Queue from './pages/Queue'
import Decisions from './pages/Decisions'
import Profile from './pages/Profile'

export default function App() {
  return (
    <div style={{ display: 'flex' }}>
      <Sidebar />
      <main style={{ marginLeft: '220px', padding: '40px', width: '100%', minHeight: '100vh' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/inbox" element={<Inbox />} />
          <Route path="/queue" element={<Queue />} />
          <Route path="/decisions" element={<Decisions />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>
    </div>
  )
}