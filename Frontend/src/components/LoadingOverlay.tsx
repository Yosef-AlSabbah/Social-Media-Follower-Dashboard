import { motion, AnimatePresence } from 'framer-motion';

interface LoadingOverlayProps {
  isVisible: boolean;
  message?: string;
}

export function LoadingOverlay({ isVisible, message = "جاري تحديث البيانات..." }: LoadingOverlayProps) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-40 flex items-center justify-center"
        >
          {/* Blur backdrop */}
          <motion.div
            initial={{ backdropFilter: 'blur(0px)' }}
            animate={{ backdropFilter: 'blur(8px)' }}
            exit={{ backdropFilter: 'blur(0px)' }}
            className="absolute inset-0 bg-background/30"
          />
          
          {/* Loading content */}
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="relative z-10 glass-card p-8 text-center max-w-sm mx-auto"
          >
            {/* Animated loader */}
            <div className="mb-6">
              <motion.div
                className="w-16 h-16 mx-auto rounded-full border-4 border-accent/20 border-t-accent"
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              />
            </div>
            
            {/* Message */}
            <motion.p
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="text-lg font-semibold text-foreground arabic-text"
            >
              {message}
            </motion.p>
            
            {/* Animated dots */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
              className="flex justify-center mt-4 space-x-1 space-x-reverse"
            >
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  className="w-2 h-2 bg-accent rounded-full"
                  animate={{
                    scale: [1, 1.3, 1],
                    opacity: [0.5, 1, 0.5]
                  }}
                  transition={{
                    duration: 1,
                    repeat: Infinity,
                    delay: i * 0.2
                  }}
                />
              ))}
            </motion.div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}