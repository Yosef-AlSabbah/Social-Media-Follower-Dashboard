import { TrendingUp, TrendingDown, Users } from 'lucide-react'
import { LucideIcon } from 'lucide-react'

interface PlatformCardProps {
  platform: string
  followers: number
  delta: number
  icon: LucideIcon
  color: string
  platformId?: string
  isLoading?: boolean
}

export function PlatformCard({ 
  platform, 
  followers, 
  delta, 
  icon: Icon, 
  color,
  platformId = '',
  isLoading = false 
}: PlatformCardProps) {
  const isPositive = delta >= 0
  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`
    }
    return num.toString()
  }

  const getPlatformGlowClass = (id: string) => {
    const glowMap: { [key: string]: string } = {
      'facebook': 'facebook-glow',
      'twitter': 'twitter-glow', 
      'instagram': 'instagram-glow',
      'tiktok': 'tiktok-glow',
      'youtube': 'youtube-glow',
      'snapchat': 'snapchat-glow',
      'linkedin': 'linkedin-glow'
    }
    return glowMap[id] || ''
  }

  if (isLoading) {
    return (
      <div className="platform-card group animate-pulse">
        <div className="realtime-indicator"></div>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="h-12 w-12 rounded-2xl bg-muted"></div>
            <div className="h-5 w-20 rounded-lg bg-muted"></div>
          </div>
          <div className="h-8 w-28 rounded-lg bg-muted"></div>
          <div className="h-5 w-24 rounded-lg bg-muted"></div>
        </div>
      </div>
    )
  }

  return (
    <div className={`platform-card group animate-fade-in ${getPlatformGlowClass(platformId)}`}>
      <div className="realtime-indicator"></div>
      <div className="space-y-5">
        <div className="flex items-center justify-between">
          <div 
            className="platform-icon p-4 rounded-2xl shadow-lg smooth-transition"
            style={{ 
              backgroundColor: `${color}15`, 
              color: color,
              boxShadow: `0 0 20px ${color}30`
            }}
          >
            <Icon className="w-7 h-7" />
          </div>
          <span className="text-sm text-muted-foreground font-semibold tracking-wide arabic-text">
            {platform}
          </span>
        </div>
        
        <div className="space-y-3">
          <div className="text-3xl font-bold text-foreground rtl-numbers tracking-tight">
            {formatNumber(followers)}
          </div>
          <div className={`text-sm font-semibold flex items-center justify-between px-3 py-2 rounded-xl smooth-transition ${
            isPositive 
              ? 'text-accent bg-accent/10 shadow-glow-accent' 
              : 'text-destructive bg-destructive/10'
          }`}>
            <span className="rtl-numbers">{isPositive ? '+' : ''}{formatNumber(Math.abs(delta))}</span>
            <span className="arabic-text text-xs">هذا الأسبوع</span>
          </div>
        </div>
      </div>
    </div>
  )
}