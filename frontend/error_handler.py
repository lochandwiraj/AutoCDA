import streamlit as st
from backend.error_messages import UserFriendlyErrors

def display_error(error_type, details=None):
    errors = UserFriendlyErrors()
    
    error_map = {
        "component_calculation": errors.component_calculation_failed(),
        "unclear_description": errors.unclear_circuit_description(),
        "validation": errors.validation_failed(details or []),
        "api": errors.api_error()
    }
    
    error_info = error_map.get(error_type, errors.api_error())
    
    st.error(f"❌ **{error_info['title']}**")
    st.write(error_info['message'])
    
    if 'errors' in error_info:
        for err in error_info['errors']:
            st.write(f"• {err}")
    
    st.info("💡 **Suggestions:**")
    for suggestion in error_info['suggestions']:
        st.write(f"• {suggestion}")
