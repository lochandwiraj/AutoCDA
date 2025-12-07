import { useRef, useEffect, useState } from 'react';
import './Shuffle.css';

const Shuffle = ({
  text,
  className = '',
  style = {},
  duration = 350,
  stagger = 30,
  triggerOnce = true,
  triggerOnHover = false
}) => {
  const ref = useRef(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [hasAnimated, setHasAnimated] = useState(false);

  const shuffle = () => {
    if (!ref.current || (triggerOnce && hasAnimated)) return;
    
    setIsAnimating(true);
    const chars = ref.current.querySelectorAll('.shuffle-char');
    const charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
    
    chars.forEach((char, index) => {
      const originalText = char.getAttribute('data-original');
      let iterations = 0;
      const maxIterations = 10;
      
      const interval = setInterval(() => {
        if (iterations >= maxIterations) {
          char.textContent = originalText;
          clearInterval(interval);
          if (index === chars.length - 1) {
            setIsAnimating(false);
            setHasAnimated(true);
          }
          return;
        }
        
        char.textContent = charset[Math.floor(Math.random() * charset.length)];
        iterations++;
      }, duration / maxIterations);
      
      setTimeout(() => {
        clearInterval(interval);
        char.textContent = originalText;
      }, duration + (index * stagger));
    });
  };

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !hasAnimated) {
            shuffle();
          }
        });
      },
      { threshold: 0.1 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, [hasAnimated]);

  const handleHover = () => {
    if (triggerOnHover && !isAnimating) {
      shuffle();
    }
  };

  return (
    <div
      ref={ref}
      className={`shuffle-container ${className}`}
      style={style}
      onMouseEnter={handleHover}
    >
      {text.split('').map((char, index) => (
        <span
          key={index}
          className="shuffle-char"
          data-original={char}
        >
          {char}
        </span>
      ))}
    </div>
  );
};

export default Shuffle;
