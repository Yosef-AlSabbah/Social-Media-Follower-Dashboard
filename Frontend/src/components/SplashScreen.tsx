import { motion } from 'framer-motion';
import motionWayLogo from '@/assets/motion-way-logo.png';

interface SplashScreenProps {
  onComplete?: () => void;
}

export function SplashScreen({ onComplete }: SplashScreenProps) {
  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-background via-background to-primary/5"
      initial={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.8, ease: "easeInOut" }}
      onAnimationComplete={() => onComplete?.()}
    >
      {/* Animated background effects */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute -inset-10 opacity-30"
          animate={{
            background: [
              'radial-gradient(circle at 20% 50%, hsl(var(--primary) / 0.15) 0%, transparent 50%)',
              'radial-gradient(circle at 80% 20%, hsl(var(--accent) / 0.15) 0%, transparent 50%)',
              'radial-gradient(circle at 40% 80%, hsl(var(--secondary) / 0.15) 0%, transparent 50%)',
              'radial-gradient(circle at 20% 50%, hsl(var(--primary) / 0.15) 0%, transparent 50%)',
            ]
          }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        />
      </div>

      {/* Main content */}
      <div className="relative z-10 text-center">
        {/* Logo animation */}
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="mb-8"
        >
          <motion.img
            src={motionWayLogo}
            alt="Motion Way Logo"
            className="w-24 h-24 mx-auto rounded-2xl shadow-2xl"
            animate={{ 
              boxShadow: [
                '0 0 20px hsl(var(--accent) / 0.3)',
                '0 0 40px hsl(var(--primary) / 0.4)',
                '0 0 20px hsl(var(--accent) / 0.3)'
              ]
            }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </motion.div>

        {/* Title animation */}
        <motion.h1
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="text-4xl font-bold mb-4 bg-gradient-to-r from-foreground via-accent to-primary bg-clip-text text-transparent"
        >
          Motion Way
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="text-lg text-muted-foreground mb-8 arabic-text"
        >
          لوحة تحكم منصات التواصل الاجتماعي
        </motion.p>

        {/* Loading animation */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.8 }}
          className="flex justify-center items-center space-x-2 space-x-reverse"
        >
          <div className="flex space-x-1 space-x-reverse">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-3 h-3 bg-accent rounded-full"
                animate={{
                  y: [0, -10, 0],
                  opacity: [0.5, 1, 0.5]
                }}
                transition={{
                  duration: 0.8,
                  repeat: Infinity,
                  delay: i * 0.2
                }}
              />
            ))}
          </div>
          <motion.span
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
            className="text-sm text-muted-foreground mr-4 arabic-text"
          >
            جاري التحميل...
          </motion.span>
        </motion.div>
      </div>
    </motion.div>
  );
}