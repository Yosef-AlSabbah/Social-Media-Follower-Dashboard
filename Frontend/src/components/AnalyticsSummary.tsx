import { TrendingUp, Award, BarChart3 } from 'lucide-react'
import { useEffect, useState } from 'react'

interface AnalyticsSummaryProps {
  totalFollowers: number
  topPlatform: string
  dailyGrowth: number
  isLoading?: boolean
}

export function AnalyticsSummary({ 
  totalFollowers, 
  topPlatform, 
  dailyGrowth, 
  isLoading = false 
}: AnalyticsSummaryProps) {
  const [animatedValues, setAnimatedValues] = useState({
    totalFollowers: 0,
    dailyGrowth: 0
  });

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`
    } else if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`
    }
    return num.toString()
  }

  // Smooth count-up animation
  useEffect(() => {
    if (!isLoading && totalFollowers > 0) {
      const duration = 2000; // 2 seconds
      const steps = 60;
      const stepDuration = duration / steps;
      
      let currentStep = 0;
      const interval = setInterval(() => {
        currentStep++;
        const progress = currentStep / steps;
        const easeOutProgress = 1 - Math.pow(1 - progress, 3);
        
        setAnimatedValues({
          totalFollowers: Math.floor(totalFollowers * easeOutProgress),
          dailyGrowth: Math.floor(dailyGrowth * easeOutProgress)
        });
        
        if (currentStep >= steps) {
          clearInterval(interval);
          setAnimatedValues({ totalFollowers, dailyGrowth });
        }
      }, stepDuration);
      
      return () => clearInterval(interval);
    }
  }, [totalFollowers, dailyGrowth, isLoading]);

  const stats = [
    {
      title: 'إجمالي المتابعين',
      value: formatNumber(animatedValues.totalFollowers),
      icon: TrendingUp,
      gradient: 'bg-gradient-secondary',
      glow: 'shadow-glow-secondary'
    },
    {
      title: 'المنصة الرائدة',
      value: topPlatform,
      icon: Award,
      gradient: 'bg-gradient-accent',
      glow: 'shadow-glow-accent'
    },
    {
      title: 'النمو اليومي',
      value: formatNumber(animatedValues.dailyGrowth),
      icon: BarChart3,
      gradient: 'bg-gradient-primary',
      glow: 'shadow-glow-primary'
    }
  ]

  if (isLoading) {
    return (
      <div className="mb-8 responsive-grid animate-pulse">
        {Array.from({ length: 3 }).map((_, index) => (
          <div key={index} className="platform-card group">
            <div className="realtime-indicator"></div>
            <div className="space-y-5">
              <div className="flex items-center space-x-4 space-x-reverse">
                <div className="h-12 w-12 rounded-2xl bg-muted"></div>
                <div className="h-6 w-28 rounded-lg bg-muted"></div>
              </div>
              <div className="h-10 w-24 rounded-lg bg-muted"></div>
            </div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="mb-8 responsive-grid">
      {stats.map((stat, index) => (
        <div 
          key={stat.title} 
          className={`platform-card group animate-fade-in overflow-hidden smooth-transition glassmorphism-enhanced`}
          style={{ 
            animationDelay: `${index * 0.15}s`,
            boxShadow: index === 0 ? 'var(--glow-secondary), 0 8px 32px rgba(0,0,0,0.12)' : 
                      index === 1 ? 'var(--glow-accent), 0 8px 32px rgba(0,0,0,0.12)' : 
                      'var(--glow-primary), 0 8px 32px rgba(0,0,0,0.12)',
            background: `linear-gradient(135deg, 
              rgba(255,255,255,0.1) 0%, 
              rgba(255,255,255,0.05) 50%, 
              rgba(255,255,255,0.1) 100%)`
          }}
        >
          <div className="realtime-indicator"></div>
          <div className="space-y-5">
            <div className="flex items-center space-x-4 space-x-reverse">
              <div className={`p-4 rounded-2xl ${stat.gradient} platform-icon shadow-lg breathe-icon relative overflow-hidden smooth-transition`}>
                <stat.icon className="w-7 h-7 text-white relative z-10" />
              </div>
              <h3 className="text-sm font-semibold text-muted-foreground tracking-wide uppercase arabic-text">
                {stat.title}
              </h3>
            </div>
            <p className="text-3xl font-bold text-foreground rtl-numbers tracking-tight">
              {stat.value}
            </p>
          </div>
        </div>
      ))}
    </div>
  )
}