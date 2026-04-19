# AI-Driven Ransomware Detection System

## Quick Start

### Option 1: Use the Launcher (Recommended)
```bash
python launch.py
```

### Option 2: Direct Launch
```bash
python main.py
```

### Option 3: Dashboard Interface
```bash
streamlit run app.py
```

## System Flow

The integrated system follows this flow:

1. **System Monitoring** - Monitors file operations and system resources
2. **Feature Extraction** - Extracts behavioral patterns from activities  
3. **AI Detection** - Uses trained model to detect ransomware patterns
4. **Automated Response** - Triggers containment actions when threats detected
5. **Dashboard Data** - Sends metrics to dashboard for visualization

## Key Features

- **Real-time Monitoring**: Continuous file system and resource monitoring
- **AI-Powered Detection**: Machine learning model for pattern recognition
- **Automated Response**: Immediate threat containment and alerting
- **Modular Design**: Clean separation of concerns across modules
- **Dashboard Integration**: Real-time visualization of system status

## System Components

- `main.py` - Main integration module
- `launch.py` - System launcher with dependency checks
- `monitor/` - System monitoring components
- `features/` - Feature extraction logic
- `detection/` - AI detection engine
- `response/` - Automated response handlers
- `app.py` - Streamlit dashboard interface

## Output Files

- `dashboard_data.json` - Real-time metrics for dashboard
- `ransomware_detections.log` - Detection event log
- `ransomware_model.pkl` - Trained detection model

## Controls

- **Ctrl+C** - Graceful system shutdown
- **Status Updates** - Every 30 seconds in console
- **Dashboard** - Real-time web interface on localhost:8501

## Configuration

Response actions can be configured in `response_config.json`:
- System isolation settings
- Backup preferences  
- Alert configurations
- Email notifications