import Squares from './Squares';
import Shuffle from './Shuffle';
import './LandingPage.css';

const LandingPage = ({ onGetStarted }) => {
  return (
    <div className="landing-page">
      <Squares
        speed={0.5}
        squareSize={50}
        direction="diagonal"
        borderColor="rgba(102, 126, 234, 0.15)"
        hoverFillColor="rgba(102, 126, 234, 0.8)"
      />
      
      <div className="landing-content">
        <div className="landing-hero">
          <h1 className="landing-title">
            <span className="title-icon">⚡</span>
            <Shuffle
              text="AutoCDA"
              duration={350}
              stagger={30}
              triggerOnce={true}
              triggerOnHover={true}
            />
          </h1>
          <p className="landing-subtitle">
            AI-Powered Circuit Design Assistant
          </p>
          <p className="landing-description">
            Transform natural language into production-ready KiCad schematics.
            Powered by Claude 3.5 Sonnet.
          </p>

          <button className="get-started-btn" onClick={onGetStarted}>
            Get Started
            <span className="btn-arrow">→</span>
          </button>

          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI-Powered</h3>
              <p>Natural language understanding with Claude 3.5</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Instant Generation</h3>
              <p>Get KiCad schematics in seconds</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🔢</div>
              <h3>Smart Calculations</h3>
              <p>Automatic component value selection</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📐</div>
              <h3>Step-by-Step Math</h3>
              <p>Detailed calculation breakdowns</p>
            </div>
          </div>

          <div className="supported-circuits">
            <p className="supported-title">Supported Circuits:</p>
            <div className="circuit-tags">
              <span className="circuit-tag">RC Low-Pass Filter</span>
              <span className="circuit-tag">RC High-Pass Filter</span>
              <span className="circuit-tag">Voltage Divider</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
