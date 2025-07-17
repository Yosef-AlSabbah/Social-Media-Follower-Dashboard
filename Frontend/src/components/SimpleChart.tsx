import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts'
import { ChartDataPoint } from '@/lib/api-config'

interface SimpleChartProps {
  data: ChartDataPoint[]
  variant: 'accent' | 'secondary' | 'primary'
  title: string
}

export function SimpleChart({ data, variant, title }: SimpleChartProps) {
  const colors = {
    accent: 'hsl(140 85% 50%)', // Vibrant green
    secondary: 'hsl(210 90% 60%)', // Bright blue  
    primary: 'hsl(260 80% 55%)' // Purple
  }
  
  const glowClasses = {
    accent: 'shadow-glow-accent hover:scale-105',
    secondary: 'shadow-glow-secondary hover:scale-105', 
    primary: 'shadow-glow-primary hover:scale-105'
  }
  
  const color = colors[variant]
  const glowClass = glowClasses[variant]
  
  return (
    <div className={`chart-container group shadow-elegant transition-all duration-500 hover:${glowClass.split(' ')[0]} hover:scale-105`}>
      <h3 className="text-xl font-bold text-foreground mb-6 bg-gradient-to-r from-foreground to-accent bg-clip-text">
        {title}
      </h3>
      <div className="h-72 -mx-4">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 20, right: 20, left: 0, bottom: 20 }}>
            <XAxis 
              dataKey="day" 
              axisLine={false}
              tickLine={false}
              className="text-sm text-muted-foreground font-medium"
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              className="text-sm text-muted-foreground font-medium"
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => {
                if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`
                if (value >= 1000) return `${(value / 1000).toFixed(1)}K`
                return value.toString()
              }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'hsl(var(--card))',
                border: '1px solid hsl(var(--border))',
                borderRadius: '8px',
                color: 'hsl(var(--foreground))',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
              formatter={(value: number) => [
                value >= 1000000 ? `${(value / 1000000).toFixed(1)}M` :
                value >= 1000 ? `${(value / 1000).toFixed(1)}K` :
                value.toString(),
                'المتابعون'
              ]}
              labelStyle={{ color: 'hsl(var(--muted-foreground))' }}
            />
            <Line
              type="monotone"
              dataKey="value"
              stroke={color}
              strokeWidth={3}
              dot={{ fill: color, strokeWidth: 2, r: 4 }}
              activeDot={{
                r: 6,
                stroke: color,
                strokeWidth: 2,
                fill: 'hsl(var(--background))'
              }}
              style={{
                filter: `drop-shadow(0 0 8px ${color}40)`
              }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}