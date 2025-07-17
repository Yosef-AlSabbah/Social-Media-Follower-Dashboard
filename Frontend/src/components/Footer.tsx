import developerPhoto from '../assets/developer-photo.jpg'
import motionWayLogo from '../assets/motion-way-logo.png'

export function Footer() {
  return (
    <footer className="mt-16 py-12 border-t border-border/50 bg-card/30 backdrop-blur-sm">
      <div className="container mx-auto px-6">
        <div className="flex flex-col items-center space-y-8">
          {/* Developer and Company Info */}
          <div className="flex flex-col md:flex-row items-center gap-8">
            {/* Developer Photo */}
            <div className="relative group">
              <img 
                src={developerPhoto} 
                alt="Youssef Mohammed Youssef Al-Sabbah"
                className="w-20 h-20 rounded-full border-2 border-accent/50 shadow-glow-accent transition-all duration-500 group-hover:scale-110 group-hover:border-accent"
              />
              <div className="absolute inset-0 rounded-full bg-gradient-to-r from-accent/20 to-secondary/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            </div>
            
            {/* Company Logo */}
            <div className="relative group">
              <img 
                src={motionWayLogo} 
                alt="Motion Way Company"
                className="w-16 h-16 transition-all duration-500 group-hover:scale-110"
              />
            </div>
          </div>
          
          {/* Text Content */}
          <div className="space-y-4 text-center">
            <p className="text-lg font-bold bg-gradient-to-r from-accent to-secondary bg-clip-text text-transparent">
              مطور البرمجيات يوسف محمد يوسف السباح
            </p>
            <p className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              شركة موشن واي
            </p>
            <p className="text-sm text-muted-foreground">
              جميع الحقوق محفوظة لشركة موشن واي © 2024
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}