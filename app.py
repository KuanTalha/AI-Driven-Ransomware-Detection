import streamlit as st
import pandas as pd
import numpy as np
import time
import threading
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from collections import deque
import psutil

# Import your existing modules
from system_monitor import SystemMonitor
from detector import RansomwareDetector
from feature_extractor import FeatureExtractor

# Configure Streamlit page
st.set_page_config(
    page_title="Ransomware Detection Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'monitor' not in st.session_state:
    st.session_state.monitor = SystemMonitor()
if 'detector' not in st.session_state:
    try:
        st.session_state.detector = RansomwareDetector()
    except FileNotFoundError:
        st.session_state.detector = None
if 'extractor' not in st.session_state:
    st.session_state.extractor = FeatureExtractor()
if 'logs' not in st.session_state:
    st.session_state.logs = deque(maxlen=100)
if 'system_data' not in st.session_state:
    st.session_state.system_data = deque(maxlen=50)

def get_threat_color(score):
    """Return color based on threat score"""
    if score >= 0.8:
        return "#FF4B4B"  # Red
    elif score >= 0.5:
        return "#FF8C00"  # Orange
    elif score >= 0.3:
        return "#FFD700"  # Yellow
    return "#00FF00"  # Green

def add_log_entry(message, level="INFO"):
    """Add entry to logs"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.appendleft({
        'timestamp': timestamp,
        'level': level,
        'message': message
    })

def collect_system_data():
    """Collect current system data"""
    try:
        data = st.session_state.monitor.get_system_data()
        st.session_state.system_data.append(data)
        
        # Extract features if we have enough data
        if st.session_state.detector:
            feature_result = st.session_state.extractor.process_monitoring_data(data)
            if feature_result and feature_result['normalized_vector'] is not None:
                # Pad vector to match model expectations (10 features)
                padded_vector = np.pad(feature_result['normalized_vector'], 
                                     (0, max(0, 10 - len(feature_result['normalized_vector']))), 
                                     'constant')[:10]
                
                result = st.session_state.detector.detect_threat(padded_vector)
                data['threat_score'] = result['threat_score']
                data['alert_level'] = result['alert_level']
                
                if result['is_threat']:
                    add_log_entry(f"THREAT DETECTED! Score: {result['threat_score']:.3f}", "CRITICAL")
                elif result['alert_level'] != 'NORMAL':
                    add_log_entry(f"Elevated activity detected - {result['alert_level']}", "WARNING")
            else:
                data['threat_score'] = 0.0
                data['alert_level'] = 'NORMAL'
        else:
            data['threat_score'] = 0.0
            data['alert_level'] = 'NORMAL'
            
    except Exception as e:
        add_log_entry(f"Error collecting data: {str(e)}", "ERROR")

# Main dashboard
st.title("🛡️ Ransomware Detection Dashboard")

# Auto-refresh setup
placeholder = st.empty()

# Collect initial data
collect_system_data()

with placeholder.container():
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    current_data = st.session_state.system_data[-1] if st.session_state.system_data else {}
    
    with col1:
        cpu_usage = current_data.get('cpu_usage', 0)
        st.metric(
            label="CPU Usage",
            value=f"{cpu_usage:.1f}%",
            delta=f"{cpu_usage - 50:.1f}%" if cpu_usage > 50 else None
        )
    
    with col2:
        memory_usage = current_data.get('memory_usage', {}).get('percent', 0)
        st.metric(
            label="Memory Usage", 
            value=f"{memory_usage:.1f}%",
            delta=f"{memory_usage - 60:.1f}%" if memory_usage > 60 else None
        )
    
    with col3:
        disk_usage = psutil.disk_usage('C:\\').percent
        st.metric(
            label="Disk Usage",
            value=f"{disk_usage:.1f}%",
            delta=f"{disk_usage - 70:.1f}%" if disk_usage > 70 else None
        )
    
    with col4:
        threat_score = current_data.get('threat_score', 0)
        st.metric(
            label="Threat Score",
            value=f"{threat_score:.3f}",
            delta=f"{threat_score:.3f}" if threat_score > 0.3 else None
        )

    # Threat indicator
    st.subheader("🚨 Threat Status")
    threat_color = get_threat_color(threat_score)
    alert_level = current_data.get('alert_level', 'NORMAL')
    
    st.markdown(f"""
    <div style="padding: 20px; border-radius: 10px; background-color: {threat_color}20; border-left: 5px solid {threat_color};">
        <h3 style="color: {threat_color}; margin: 0;">Alert Level: {alert_level}</h3>
        <p style="margin: 5px 0 0 0;">Threat Score: {threat_score:.3f}</p>
    </div>
    """, unsafe_allow_html=True)

    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 System Performance")
        if len(st.session_state.system_data) > 1:
            df = pd.DataFrame([
                {
                    'Time': datetime.fromtimestamp(d['timestamp']),
                    'CPU': d['cpu_usage'],
                    'Memory': d['memory_usage']['percent'],
                    'Threat Score': d.get('threat_score', 0) * 100
                }
                for d in list(st.session_state.system_data)[-20:]
            ])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Time'], y=df['CPU'], name='CPU %', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=df['Time'], y=df['Memory'], name='Memory %', line=dict(color='green')))
            fig.add_trace(go.Scatter(x=df['Time'], y=df['Threat Score'], name='Threat Score %', line=dict(color='red')))
            
            fig.update_layout(
                height=300,
                showlegend=True,
                margin=dict(l=0, r=0, t=0, b=0),
                yaxis=dict(range=[0, 100])
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💾 File Operations")
        if current_data:
            file_ops = current_data.get('file_operations', {})
            
            fig = go.Figure(data=[
                go.Bar(
                    x=['Created', 'Deleted', 'Renamed'],
                    y=[file_ops.get('created', 0), file_ops.get('deleted', 0), file_ops.get('renamed', 0)],
                    marker_color=['#1f77b4', '#ff7f0e', '#2ca02c']
                )
            ])
            
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

    # Logs section
    st.subheader("📋 Event Logs")
    
    if st.session_state.logs:
        log_df = pd.DataFrame(list(st.session_state.logs))
        
        # Color code by level
        def get_log_color(level):
            colors = {
                'CRITICAL': '#FF4B4B',
                'ERROR': '#FF8C00', 
                'WARNING': '#FFD700',
                'INFO': '#00FF00'
            }
            return colors.get(level, '#FFFFFF')
        
        # Display logs with styling
        for log in list(st.session_state.logs)[:10]:
            color = get_log_color(log['level'])
            st.markdown(f"""
            <div style="padding: 8px; margin: 2px 0; border-left: 3px solid {color}; background-color: {color}10;">
                <strong>{log['timestamp']}</strong> [{log['level']}] {log['message']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No events logged yet.")

    # System info sidebar
    with st.sidebar:
        st.header("System Info")
        if current_data:
            st.write(f"**Processes:** {current_data.get('process_count', 0)}")
            st.write(f"**Available Memory:** {current_data.get('memory_usage', {}).get('available_gb', 0):.1f} GB")
            
            disk_io = current_data.get('disk_io', {})
            st.write(f"**Disk Read:** {disk_io.get('read_bytes_per_sec', 0) / 1024:.0f} KB/s")
            st.write(f"**Disk Write:** {disk_io.get('write_bytes_per_sec', 0) / 1024:.0f} KB/s")

# Auto-refresh every 3 seconds
time.sleep(3)
collect_system_data()
st.rerun()