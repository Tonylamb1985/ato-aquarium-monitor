# 🌡️ 3-Sensor Version Files

## Overview

This folder contains the **upgraded 3-sensor version** of the ATO Aquarium Monitor.

## Files Included

### Core Files
- `ato_monitor_3sensors.py` - Updated Python script for 3 sensors
- `config_3sensors.py` - Configuration template
- `home-assistant-3sensors/` - HA configuration folder
  - `configuration_3sensors.yaml` - MQTT sensors for all 3 temps
  - `dashboard_3sensors.yaml` - 7-tab dashboard

### Documentation
- `3_SENSOR_UPGRADE_GUIDE.md` - Complete upgrade instructions
- `MULTI_SENSOR_WIRING.md` - Wiring diagrams for 3 sensors
- `3_SENSORS_INSTALL.md` - Installation guide

## Quick Start

### 1. Wire Hardware
See `MULTI_SENSOR_WIRING.md` - all 3 sensors connect to GPIO 4

### 2. Find Sensor IDs
```bash
ls /sys/bus/w1/devices/28-*
```

### 3. Configure
```bash
cd /home/pi/ato-aquarium-monitor
cp config_3sensors.py config.py
nano config.py
# Update sensor IDs or enable auto-detect
```

### 4. Install Script
```bash
# Backup original
cp ato_monitor.py ato_monitor_original.py

# Copy new version
cp ato_monitor_3sensors.py ato_monitor.py

# Restart service
sudo systemctl restart ato-monitor.service
```

### 5. Update Home Assistant
Copy contents from `home-assistant-3sensors/configuration_3sensors.yaml`
Paste into your Home Assistant `configuration.yaml`

### 6. Add Dashboard Tab
Copy from `dashboard_3sensors.yaml` and add as new tab

## Differences from Original

### Added Features
✅ 3 temperature sensors (Display, Sump, ATO)
✅ Individual calibration per sensor
✅ Temperature difference monitoring
✅ Display vs Sump difference alerts
✅ New dashboard tab "All Temperatures"
✅ Auto-detection of sensors
✅ Enhanced temperature alerts

### Backward Compatible
✅ All original features still work
✅ Original MQTT topics maintained
✅ Existing dashboard still works
✅ Can upgrade without losing data

## Monitoring Locations

1. **Display Tank** (`sensor.display_tank_temperature`)
   - Main aquarium
   - Primary monitoring
   - Critical alerts enabled

2. **Sump** (`sensor.sump_temperature`)
   - Sump/filtration area
   - Primary monitoring
   - Critical alerts enabled
   - Compared with Display for circulation issues

3. **ATO Reservoir** (`sensor.ato_tank_temperature`)
   - Reservoir water
   - Informational only
   - No critical alerts (just tracking)

## New MQTT Topics

### Temperature Data
- `aquarium/temp/display` - Display tank calibrated temp
- `aquarium/temp/display_raw` - Display tank raw reading
- `aquarium/temp/sump` - Sump calibrated temp
- `aquarium/temp/sump_raw` - Sump raw reading
- `aquarium/temp/display_sump_diff` - Temperature difference

### Calibration
- `aquarium/temp/display_calibration` - Display offset
- `aquarium/temp/sump_calibration` - Sump offset
- `aquarium/temp/ato_calibration` - ATO offset (renamed from old)

### Statistics
- `aquarium/temp/display_stats` - Display 24h/7d stats
- `aquarium/temp/sump_stats` - Sump 24h/7d stats

## Configuration Options

### Auto-Detection (Recommended)
```python
AUTO_DETECT_SENSORS = True
```
System automatically finds and assigns sensors.

### Manual Assignment
```python
AUTO_DETECT_SENSORS = False
TEMP_SENSOR_DISPLAY_ID = "28-0000xxxxxxx1"
TEMP_SENSOR_SUMP_ID = "28-0000xxxxxxx2"
TEMP_SENSOR_ATO_ID = "28-0000xxxxxxx3"
```

## Alert Thresholds

### Temperature Alerts (Display & Sump)
- Critical Low: <20°C
- Warning Low: <22°C
- Warning High: >28°C
- Critical High: >30°C

### Temperature Difference (Display vs Sump)
- Warning: >2.0°C difference
- Critical: >3.0°C difference

### ATO Reservoir
- No critical alerts (informational only)
- Tracked for trend analysis

## Dashboard

### New Tab: "All Temperatures"
- 3 temperature gauges side-by-side
- Temperature difference indicator
- 24-hour comparison chart
- Calibration interface for all 3 sensors
- 7-day trend comparison

### Original Tabs
All original tabs still work!
Temperature tab now focuses on Display tank

## Troubleshooting

### Only 2 Sensors Detected
Check wiring - all yellow wires to GPIO 4?

### Sensors Show Wrong Values
Use manual assignment instead of auto-detect

### Temperature Difference Always High
Calibrate each sensor individually

### One Sensor Shows 85°C
Power cycle Pi, check that sensor's wiring

## Support

See detailed guides:
- Installation: `3_SENSORS_INSTALL.md`
- Wiring: `MULTI_SENSOR_WIRING.md`
- Upgrade: `3_SENSOR_UPGRADE_GUIDE.md`

---

**Ready to monitor 3 locations! 🌡️🌡️🌡️**
