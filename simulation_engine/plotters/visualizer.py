import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Optional

class SimulationVisualizer:
    """Create interactive plots from simulation data"""
    
    @staticmethod
    def create_bode_plot(frequencies: List[float], 
                         magnitudes: List[float],
                         phases: Optional[List[float]] = None,
                         title: str = "Bode Plot") -> go.Figure:

        mags_db = 20 * np.log10(np.array(magnitudes) + 1e-12)

        if phases is not None:
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Magnitude', 'Phase'),
                vertical_spacing=0.1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=frequencies,
                    y=mags_db,
                    mode='lines',
                    name='Magnitude'
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=frequencies,
                    y=phases,
                    mode='lines',
                    name='Phase'
                ),
                row=2, col=1
            )
            
            fig.update_xaxes(title_text="Frequency (Hz)", type="log", row=2, col=1)
            fig.update_xaxes(type="log", row=1, col=1)
            fig.update_yaxes(title_text="Magnitude (dB)", row=1, col=1)
            fig.update_yaxes(title_text="Phase (rad)", row=2, col=1)
        
        else:
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=frequencies,
                    y=mags_db,
                    mode='lines',
                    name='Magnitude'
                )
            )
            fig.update_xaxes(title_text="Frequency (Hz)", type="log")
            fig.update_yaxes(title_text="Magnitude (dB)")
        
        fig.update_layout(
            title=title,
            hovermode='x unified',
            template='plotly_white',
            height=600 if phases else 400
        )
        
        return fig
