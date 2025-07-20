import { Moon, Sun } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useTheme } from './ThemeProvider'
import logoImage from '@/assets/logo.webp'

export function Header() {
  const { theme, setTheme } = useTheme()

  return (
    <header className="header-glass rounded-3xl p-6 mb-8 animate-fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="w-40 h-15 bg-gradient-hero rounded-2xl flex items-center justify-center shadow-glow-accent smooth-transition hover:scale-110 hover:shadow-glow-intense p-2">
            <img src={logoImage} alt="Company Logo" className="w-full h-full object-contain" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-foreground bg-gradient-to-r from-foreground to-accent bg-clip-text">
              لوحة متابعة المتابعين
            </h1>
            <p className="text-muted-foreground text-lg">مراقبة منصات التواصل الاجتماعي</p>
          </div>
        </div>
        
        <Button
          variant="outline"
          size="icon"
          onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
          className="btn-glass w-12 h-12 group"
        >
          {theme === 'light' ? 
            <Moon className="h-5 w-5 group-hover:rotate-12 smooth-transition" /> : 
            <Sun className="h-5 w-5 group-hover:rotate-12 smooth-transition" />
          }
        </Button>
      </div>
    </header>
  )
}