from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import plotly.graph_objects as go
from pathlib import Path

class ReportGenerator:
    """Generate HTML/PDF simulation reports"""
    
    def __init__(self, template_dir: str = "simulation_engine/templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate_report(self, 
                       circuit_name: str,
                       metrics: dict,
                       bode_plot: go.Figure,
                       transient_plot: go.Figure = None,
                       validation: dict = None) -> str:
        """
        Generate HTML report
        Returns:
            HTML string
        """
        template = self.env.get_template('report_template.html')
        
        # Convert plots to HTML
        bode_html = bode_plot.to_html(include_plotlyjs='cdn', full_html=False)
        transient_html = (
            transient_plot.to_html(include_plotlyjs=False, full_html=False)
            if transient_plot else None
        )
        
        # Render template
        html = template.render(
            circuit_name=circuit_name,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            metrics=metrics,
            bode_plot=bode_html,
            transient_plot=transient_html,
            validation=validation or {'passed': True, 'issues': []}
        )
        
        return html
    
    def save_report(self, html: str, filepath: str):
        """Save HTML report to file"""
        Path(filepath).write_text(html, encoding='utf-8')
    
    def generate_pdf(self, html: str, filepath: str):
        """Convert HTML to PDF (requires weasyprint)"""
        try:
            from weasyprint import HTML
            HTML(string=html).write_pdf(filepath)
        except ImportError:
            print(" weasyprint not installed, skipping PDF generation")
