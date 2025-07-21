import { AppRouter } from '@app/router'
import { Background3D } from '@shared/ui/Background3D'

export function App() {
  return (
    <div className="app" style={{ position: 'relative', zIndex: 1 }}>
      <Background3D />
      <AppRouter />
    </div>
  )
} 