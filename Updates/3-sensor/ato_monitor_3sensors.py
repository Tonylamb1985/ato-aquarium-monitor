#!/usr/bin/env python3
"""
ATO Aquarium Monitor - 3 Temperature Sensors Version
Version: 2.0.0
Author: ATO Aquarium Monitor Project (Enhanced by Tony Lamb)
License: MIT

Complete aquarium Auto Top-Off monitoring system with:
- Float switch monitoring
- Pump control via relay
- 3x Temperature monitoring (Display Tank, Sump, ATO Reservoir)
- Auto-calibration
- Seasonal tracking
- MQTT integration for Home Assistant
"""

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
import json
import pickle
import os
import glob

# Import configuration
try:
    from config import *
except ImportError:
    print("ERROR: config.py not found!")
    print("Please copy config_3sensors.py to config.py and edit with your settings")
    exit(1)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOAT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PUMP_PIN, GPIO.OUT)
GPIO.output(PUMP_PIN, GPIO.HIGH)  # Start with pump OFF

# Initialize MQTT client
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
except Exception as e:
    print(f"ERROR: Could not connect to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Error: {e}")
    exit(1)

# State variables
daily_usage = 0
activation_count = 0
reservoir_level = RESERVOIR_CAPACITY
last_activation_time = datetime.now()
activation_history = []
last_state = GPIO.input(FLOAT_PIN)
monitoring_enabled = True
disabled_reason = None
filling_start_time = None
filling_duration = 0
stuck_alert_sent = False
pump_running = False

# Calibration data
calibration_data = {
    'activations_since_refill': 0,
    'last_refill_amount': 0,
    'refill_history': [],
    'calibrated_lph': LITERS_PER_ACTIVATION,
    'confidence': 0,
    'last_calibration_date': None
}

# Tracking data
alerts_history = []
pump_performance_history = []

# ============================================================================
# TEMPERATURE SENSOR CONFIGURATION (3 SENSORS)
# ============================================================================

temp_sensors = {
    'display': {
        'id': None,
        'name': 'Display Tank',
        'current_temp': None,
        'raw_temp': None,
        'calibration_offset': 0.0,
        'history': [],
        'alerts_enabled': True  # Critical alerts enabled
    },
    'sump': {
        'id': None,
        'name': 'Sump',
        'current_temp': None,
        'raw_temp': None,
        'calibration_offset': 0.0,
        'history': [],
        'alerts_enabled': True  # Critical alerts enabled
    },
    'ato': {
        'id': None,
        'name': 'ATO Reservoir',
        'current_temp': None,
        'raw_temp': None,
        'calibration_offset': 0.0,
        'history': [],
        'alerts_enabled': False  # Informational only
    }
}

last_temp_alert = {}

# ============================================================================
# TEMPERATURE SENSOR FUNCTIONS (MULTI-SENSOR)
# ============================================================================

def find_all_temp_sensors():
    """Auto-detect all DS18B20 sensors or use manual configuration"""
    global temp_sensors
    
    try:
        all_sensors = glob.glob('/sys/bus/w1/devices/28-*')
        
        if len(all_sensors) == 0:
            print("⚠️  No DS18B20 temperature sensors detected")
            return False
        
        print(f"🔍 Found {len(all_sensors)} DS18B20 sensor(s)")
        
        # Check if we should auto-detect or use manual IDs
        if hasattr(globals().get('config'), 'AUTO_DETECT_SENSORS') and AUTO_DETECT_SENSORS:
            # Auto-detection mode
            all_sensors.sort()  # Sort alphabetically by ID
            
            if len(all_sensors) >= 1:
                temp_sensors['display']['id'] = all_sensors[0]
                print(f"   Display Tank: {all_sensors[0].split('/')[-1]}")
            
            if len(all_sensors) >= 2:
                temp_sensors['sump']['id'] = all_sensors[1]
                print(f"   Sump: {all_sensors[1].split('/')[-1]}")
            
            if len(all_sensors) >= 3:
                temp_sensors['ato']['id'] = all_sensors[2]
                print(f"   ATO Reservoir: {all_sensors[2].split('/')[-1]}")
            
            if len(all_sensors) < 3:
                print(f"⚠️  Only {len(all_sensors)} sensor(s) detected (system supports 3)")
                print("   Add more sensors or switch to manual ID configuration")
        
        else:
            # Manual configuration mode
            for sensor_key, sensor_data in temp_sensors.items():
                config_id_key = f'TEMP_SENSOR_{sensor_key.upper()}_ID'
                if hasattr(globals().get('config'), config_id_key):
                    manual_id = getattr(globals().get('config'), config_id_key)
                    
                    # Find full path
                    for full_path in all_sensors:
                        if manual_id in full_path:
                            sensor_data['id'] = full_path
                            print(f"   {sensor_data['name']}: {manual_id}")
                            break
        
        # Verify at least one sensor found
        sensors_found = sum(1 for s in temp_sensors.values() if s['id'] is not None)
        if sensors_found > 0:
            print(f"✅ Configured {sensors_found} temperature sensor(s)")
            return True
        else:
            print("⚠️  No temperature sensors configured")
            return False
    
    except Exception as e:
        print(f"⚠️  Error detecting temperature sensors: {e}")
        return False

def read_temp_raw_from_sensor(sensor_path):
    """Read raw data from a specific temperature sensor"""
    if not sensor_path:
        return None
    try:
        with open(sensor_path + '/w1_slave', 'r') as f:
            return f.readlines()
    except Exception as e:
        return None

def read_temperature_from_sensor(sensor_path):
    """Read temperature from a specific DS18B20 sensor"""
    lines = read_temp_raw_from_sensor(sensor_path)
    if not lines:
        return None
    
    if lines[0].strip()[-3:] != 'YES':
        return None
    
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return round(temp_c, 2)
    
    return None

def read_all_temperatures():
    """Read all temperature sensors with calibration applied"""
    for sensor_key, sensor_data in temp_sensors.items():
        if not sensor_data['id']:
            continue
        
        raw_temp = read_temperature_from_sensor(sensor_data['id'])
        
        if raw_temp is not None:
            sensor_data['raw_temp'] = raw_temp
            calibrated_temp = raw_temp + sensor_data['calibration_offset']
            sensor_data['current_temp'] = round(calibrated_temp, 2)

def set_temp_calibration_offset(sensor_key, offset):
    """Set temperature calibration offset for a specific sensor"""
    if sensor_key not in temp_sensors:
        print(f"⚠️  Unknown sensor: {sensor_key}")
        return
    
    offset = round(float(offset), 2)
    
    # Safety limit
    if abs(offset) > 5.0:
        print(f"⚠️  Calibration offset too large: {offset}°C (limit: ±5°C)")
        return
    
    temp_sensors[sensor_key]['calibration_offset'] = offset
    save_temp_calibration()
    
    # Publish updated offset
    client.publish(f"aquarium/temp/{sensor_key}_calibration", offset)
    print(f"🌡️  {temp_sensors[sensor_key]['name']} calibration offset set to: {offset}°C")

def record_temperature(sensor_key, temp):
    """Record a temperature reading for a specific sensor"""
    if sensor_key not in temp_sensors:
        return
    
    temp_record = {
        'timestamp': datetime.now().isoformat(),
        'temperature': temp,
        'season': get_current_season()
    }
    
    temp_sensors[sensor_key]['history'].append(temp_record)
    
    # Keep last 10,000 readings per sensor
    if len(temp_sensors[sensor_key]['history']) > 10000:
        temp_sensors[sensor_key]['history'].pop(0)
    
    save_temp_history()

def calculate_temp_stats(sensor_key):
    """Calculate temperature statistics for a specific sensor"""
    if sensor_key not in temp_sensors:
        return None
    
    history = temp_sensors[sensor_key]['history']
    
    if not history:
        return {
            'avg_24h': None,
            'min_24h': None,
            'max_24h': None,
            'avg_7d': None,
            'min_7d': None,
            'max_7d': None
        }
    
    now = datetime.now()
    day_ago = now - timedelta(hours=24)
    week_ago = now - timedelta(days=7)
    
    temps_24h = [r['temperature'] for r in history 
                 if datetime.fromisoformat(r['timestamp']) >= day_ago]
    
    temps_7d = [r['temperature'] for r in history 
                if datetime.fromisoformat(r['timestamp']) >= week_ago]
    
    return {
        'avg_24h': round(sum(temps_24h) / len(temps_24h), 2) if temps_24h else None,
        'min_24h': round(min(temps_24h), 2) if temps_24h else None,
        'max_24h': round(max(temps_24h), 2) if temps_24h else None,
        'avg_7d': round(sum(temps_7d) / len(temps_7d), 2) if temps_7d else None,
        'min_7d': round(min(temps_7d), 2) if temps_7d else None,
        'max_7d': round(max(temps_7d), 2) if temps_7d else None
    }

def calculate_temp_difference():
    """Calculate temperature difference between Display and Sump"""
    display_temp = temp_sensors['display']['current_temp']
    sump_temp = temp_sensors['sump']['current_temp']
    
    if display_temp is not None and sump_temp is not None:
        return round(abs(display_temp - sump_temp), 2)
    
    return None

# ============================================================================
# SEASONAL TRACKING FUNCTIONS
# ============================================================================

def get_current_season():
    """Determine current season based on date (Northern Hemisphere)"""
    now = datetime.now()
    month = now.month
    
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Autumn"

def get_season_emoji():
    """Get emoji for current season"""
    season = get_current_season()
    emojis = {
        "Spring": "🌸",
        "Summer": "☀️",
        "Autumn": "🍂",
        "Winter": "❄️"
    }
    return emojis.get(season, "🌍")

def calculate_seasonal_stats():
    """Calculate evaporation statistics by season"""
    seasonal_data = {
        "Spring": {"activations": 0, "liters": 0, "days": 91, "avg_per_day": 0, "lph": 0},
        "Summer": {"activations": 0, "liters": 0, "days": 91, "avg_per_day": 0, "lph": 0},
        "Autumn": {"activations": 0, "liters": 0, "days": 91, "avg_per_day": 0, "lph": 0},
        "Winter": {"activations": 0, "liters": 0, "days": 91, "avg_per_day": 0, "lph": 0}
    }
    
    year_ago = datetime.now() - timedelta(days=365)
    
    for activation_time in activation_history:
        if activation_time >= year_ago:
            month = activation_time.month
            if month in [12, 1, 2]:
                season = "Winter"
            elif month in [3, 4, 5]:
                season = "Spring"
            elif month in [6, 7, 8]:
                season = "Summer"
            else:
                season = "Autumn"
            
            seasonal_data[season]["activations"] += 1
            seasonal_data[season]["liters"] += LITERS_PER_ACTIVATION
    
    for season in seasonal_data:
        days = seasonal_data[season]["days"]
        if days > 0 and seasonal_data[season]["liters"] > 0:
            seasonal_data[season]["avg_per_day"] = round(seasonal_data[season]["liters"] / days, 2)
            seasonal_data[season]["lph"] = round(seasonal_data[season]["avg_per_day"] / 24, 3)
    
    return seasonal_data

# Continue in next message due to length...
