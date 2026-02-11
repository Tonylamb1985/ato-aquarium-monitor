# 🌡️ Upgrade to 3 Temperature Sensors

## Overview

Upgrading your ATO system to monitor **3 locations**:
1. **ATO Reservoir** (original)
2. **Main Display Tank** (new)
3. **Sump** (new)

---

## 🔌 Hardware Setup

### Wiring (All 3 Sensors on Same GPIO)

**All DS18B20 sensors connect to GPIO 4 (Pin 7):**

```
Pi Pin 1 (3.3V) ─┬─ Red Wire (Sensor 1)
                 ├─ Red Wire (Sensor 2)
                 └─ Red Wire (Sensor 3)

Pi Pin 6 (GND)  ─┬─ Black Wire (Sensor 1)
                 ├─ Black Wire (Sensor 2)
                 └─ Black Wire (Sensor 3)

Pi Pin 7 (GPIO4)─┬─ Yellow Wire (Sensor 1)
                 ├─ Yellow Wire (Sensor 2)
                 ├─ Yellow Wire (Sensor 3)
                 └─ 4.7kΩ Resistor to 3.3V
```

**Physical Connection:**
- Use terminal block or breadboard
- All yellow wires → GPIO 4
- All red wires → 3.3V
- All black wires → GND
- ONE 4.7kΩ pull-up resistor

See `MULTI_SENSOR_WIRING.md` for detailed diagrams!

---

## 🔍 Find Your Sensor IDs

After connecting all 3 sensors:

```bash
# List all sensors
ls /sys/bus/w1/devices/28-*

# Should show 3 sensors:
# 28-0000xxxxxxx1
# 28-0000xxxxxxx2
# 28-0000xxxxxxx3
```

### Identify Which Sensor is Which

**Method 1: Temperature Test**
```bash
# Read all sensors
for sensor in /sys/bus/w1/devices/28-*/w1_slave; do
  echo "$sensor"
  cat "$sensor" | grep "t="
done

# Touch one sensor (warms it up)
# Re-run - the temperature that increased is the one you touched!
```

**Method 2: Connect One at a Time**
1. Connect only Display sensor → Note ID
2. Add Sump sensor → Note new ID
3. Add ATO sensor → Note last ID

---

## 📝 Python Script Changes

### Key Modifications Needed

**1. Multiple Sensor Variables**
```python
# Replace single sensor with dictionary
temp_sensors = {
    'display': {
        'id': None,
        'name': 'Display Tank',
        'current_temp': None,
        'calibration_offset': 0.0,
        'history': []
    },
    'sump': {
        'id': None,
        'name': 'Sump',
        'current_temp': None,
        'calibration_offset': 0.0,
        'history': []
    },
    'ato': {
        'id': None,
        'name': 'ATO Reservoir',
        'current_temp': None,
        'calibration_offset': 0.0,
        'history': []
    }
}
```

**2. Auto-Detection Function**
```python
def find_all_temp_sensors():
    """Auto-detect all DS18B20 sensors"""
    sensors = glob.glob('/sys/bus/w1/devices/28-*')
    
    if len(sensors) < 3:
        print(f"⚠️  Only found {len(sensors)} sensors (need 3)")
    
    # Assign by order (alphabetically by ID)
    sensors.sort()
    
    if len(sensors) >= 3:
        temp_sensors['display']['id'] = sensors[0]
        temp_sensors['sump']['id'] = sensors[1]
        temp_sensors['ato']['id'] = sensors[2]
        print(f"✅ Found 3 temperature sensors")
        return True
    
    return False
```

**3. Read Multiple Temperatures**
```python
def read_all_temperatures():
    """Read all 3 temperature sensors"""
    for sensor_key, sensor_data in temp_sensors.items():
        sensor_id = sensor_data['id']
        if not sensor_id:
            continue
        
        temp = read_temperature_from_sensor(sensor_id)
        if temp is not None:
            # Apply calibration
            calibrated = temp + sensor_data['calibration_offset']
            sensor_data['current_temp'] = round(calibrated, 2)
```

**4. MQTT Publishing**
```python
def publish_temperature_stats():
    """Publish all temperature data"""
    # Display Tank
    client.publish("aquarium/temp/display", temp_sensors['display']['current_temp'])
    client.publish("aquarium/temp/display_raw", temp_sensors['display']['current_temp'] - temp_sensors['display']['calibration_offset'])
    
    # Sump
    client.publish("aquarium/temp/sump", temp_sensors['sump']['current_temp'])
    client.publish("aquarium/temp/sump_raw", temp_sensors['sump']['current_temp'] - temp_sensors['sump']['calibration_offset'])
    
    # ATO (keep old topics for compatibility)
    client.publish("aquarium/ato/temperature", temp_sensors['ato']['current_temp'])
    client.publish("aquarium/ato/temperature_raw", temp_sensors['ato']['current_temp'] - temp_sensors['ato']['calibration_offset'])
    
    # Temperature difference
    if temp_sensors['display']['current_temp'] and temp_sensors['sump']['current_temp']:
        diff = abs(temp_sensors['display']['current_temp'] - temp_sensors['sump']['current_temp'])
        client.publish("aquarium/temp/display_sump_diff", round(diff, 2))
```

**5. Temperature Difference Alerts**
```python
def check_temperature_alerts():
    """Check for temperature issues across all sensors"""
    display_temp = temp_sensors['display']['current_temp']
    sump_temp = temp_sensors['sump']['current_temp']
    
    # Check each sensor against thresholds
    for sensor_key, sensor_data in temp_sensors.items():
        temp = sensor_data['current_temp']
        if temp is None:
            continue
        
        # Critical alerts (Display and Sump only, not ATO)
        if sensor_key in ['display', 'sump']:
            if temp <= TEMP_MIN_CRITICAL:
                alerts.append({
                    "severity": "critical",
                    "message": f"🥶 CRITICAL: {sensor_data['name']} at {temp}°C!"
                })
    
    # Display vs Sump difference alert
    if display_temp and sump_temp:
        diff = abs(display_temp - sump_temp)
        if diff >= TEMP_DIFF_CRITICAL:
            alerts.append({
                "severity": "critical",
                "message": f"🌡️ CRITICAL: Display and Sump differ by {diff:.1f}°C!"
            })
        elif diff >= TEMP_DIFF_WARNING:
            alerts.append({
                "severity": "warning",
                "message": f"⚠️ Display and Sump differ by {diff:.1f}°C"
            })
```

---

## 🏠 Home Assistant Configuration

### New MQTT Sensors

Add to `configuration.yaml`:

```yaml
mqtt:
  sensor:
    # Display Tank Temperature
    - name: "Display Tank Temperature"
      state_topic: "aquarium/temp/display"
      unit_of_measurement: "°C"
      device_class: temperature
      state_class: measurement
      icon: mdi:thermometer-water
    
    - name: "Display Tank Temperature Raw"
      state_topic: "aquarium/temp/display_raw"
      unit_of_measurement: "°C"
      device_class: temperature
      icon: mdi:thermometer-probe
    
    # Sump Temperature
    - name: "Sump Temperature"
      state_topic: "aquarium/temp/sump"
      unit_of_measurement: "°C"
      device_class: temperature
      state_class: measurement
      icon: mdi:thermometer-water
    
    - name: "Sump Temperature Raw"
      state_topic: "aquarium/temp/sump_raw"
      unit_of_measurement: "°C"
      device_class: temperature
      icon: mdi:thermometer-probe
    
    # Temperature Difference
    - name: "Display Sump Temp Difference"
      state_topic: "aquarium/temp/display_sump_diff"
      unit_of_measurement: "°C"
      device_class: temperature
      icon: mdi:thermometer-alert
    
    # Stats for each sensor
    - name: "Display Tank 24h Average"
      state_topic: "aquarium/temp/display_stats"
      value_template: "{{ value_json.avg_24h }}"
      unit_of_measurement: "°C"
      device_class: temperature
    
    - name: "Sump 24h Average"
      state_topic: "aquarium/temp/sump_stats"
      value_template: "{{ value_json.avg_24h }}"
      unit_of_measurement: "°C"
      device_class: temperature
  
  # Calibration Controls
  number:
    - name: "Display Tank Temp Calibration"
      command_topic: "aquarium/temp/display_calibration_set"
      state_topic: "aquarium/temp/display_calibration"
      min: -5.0
      max: 5.0
      step: 0.1
      unit_of_measurement: "°C"
      icon: mdi:tune
      mode: box
    
    - name: "Sump Temp Calibration"
      command_topic: "aquarium/temp/sump_calibration_set"
      state_topic: "aquarium/temp/sump_calibration"
      min: -5.0
      max: 5.0
      step: 0.1
      unit_of_measurement: "°C"
      icon: mdi:tune
      mode: box
    
    - name: "ATO Reservoir Temp Calibration"
      command_topic: "aquarium/temp/ato_calibration_set"
      state_topic: "aquarium/temp/ato_calibration"
      min: -5.0
      max: 5.0
      step: 0.1
      unit_of_measurement: "°C"
      icon: mdi:tune
      mode: box
```

---

## 📊 New Dashboard Tab

### Tab 7: All Temperatures

Add this as a new tab in your dashboard:

```yaml
- title: All Temperatures
  path: all_temps
  icon: mdi:thermometer-lines
  cards:
    # Header
    - type: markdown
      content: |
        # 🌡️ Complete Temperature Monitoring
      card_mod:
        style: |
          ha-card {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            text-align: center;
          }
    
    # All 3 Temperature Gauges
    - type: horizontal-stack
      cards:
        - type: gauge
          entity: sensor.display_tank_temperature
          name: Display Tank
          min: 18
          max: 32
          needle: true
          severity:
            green: 24
            yellow: 22
            red: 20
        
        - type: gauge
          entity: sensor.sump_temperature
          name: Sump
          min: 18
          max: 32
          needle: true
          severity:
            green: 24
            yellow: 22
            red: 20
        
        - type: gauge
          entity: sensor.ato_tank_temperature
          name: ATO Reservoir
          min: 18
          max: 32
          needle: true
    
    # Temperature Difference Alert
    - type: entity
      entity: sensor.display_sump_temp_difference
      name: Display ↔ Sump Difference
      icon: mdi:thermometer-alert
      card_mod:
        style: |
          :host {
            {% set diff = states('sensor.display_sump_temp_difference') | float(0) %}
            {% if diff > 2.0 %}
            --paper-item-icon-color: #ef4444;
            {% elif diff > 1.0 %}
            --paper-item-icon-color: #f59e0b;
            {% else %}
            --paper-item-icon-color: #10b981;
            {% endif %}
          }
    
    # 24h Comparison Chart
    - type: custom:apexcharts-card
      header:
        show: true
        title: 📊 All Temperatures (24 Hours)
      graph_span: 24h
      apex_config:
        chart:
          height: 300
        stroke:
          curve: smooth
          width: 2
      series:
        - entity: sensor.display_tank_temperature
          name: Display Tank
          color: '#3b82f6'
        - entity: sensor.sump_temperature
          name: Sump
          color: '#10b981'
        - entity: sensor.ato_tank_temperature
          name: ATO Reservoir
          color: '#8b5cf6'
    
    # Calibration Section
    - type: entities
      title: 🔧 Temperature Calibration
      entities:
        - type: section
          label: Display Tank
        - entity: sensor.display_tank_temperature_raw
          name: Raw Reading
        - entity: number.display_tank_temp_calibration
          name: Calibration Offset
        - entity: sensor.display_tank_temperature
          name: Calibrated
        
        - type: section
          label: Sump
        - entity: sensor.sump_temperature_raw
          name: Raw Reading
        - entity: number.sump_temp_calibration
          name: Calibration Offset
        - entity: sensor.sump_temperature
          name: Calibrated
        
        - type: section
          label: ATO Reservoir
        - entity: sensor.ato_temperature_raw
          name: Raw Reading
        - entity: number.ato_reservoir_temp_calibration
          name: Calibration Offset
        - entity: sensor.ato_tank_temperature
          name: Calibrated
```

---

## 🎯 Summary of Changes

### Python Script (`ato_monitor.py`)
- ✅ Multi-sensor data structure
- ✅ Auto-detection of 3 sensors
- ✅ Individual calibration per sensor
- ✅ Temperature difference monitoring
- ✅ Enhanced alert logic

### Configuration (`config.py`)
- ✅ Sensor ID configuration
- ✅ Auto-detect option
- ✅ Temperature difference thresholds

### Home Assistant (`configuration.yaml`)
- ✅ 6 new temperature sensors
- ✅ 3 calibration number inputs
- ✅ Temperature difference sensor
- ✅ Stats for each sensor

### Dashboard
- ✅ New "All Temperatures" tab
- ✅ 3 temperature gauges
- ✅ Comparison chart
- ✅ Calibration interface for all 3

---

## ⚡ Quick Start

1. **Wire all 3 sensors** (see MULTI_SENSOR_WIRING.md)
2. **Find sensor IDs:**
   ```bash
   ls /sys/bus/w1/devices/28-*
   ```
3. **Update config.py** with sensor IDs (or use auto-detect)
4. **Update Python script** with multi-sensor code
5. **Add new sensors to HA** configuration.yaml
6. **Restart HA** and verify entities appear
7. **Add new dashboard tab**
8. **Calibrate each sensor** individually

---

## 🔧 Testing

```bash
# Test all 3 sensors detected
python3 << 'EOF'
import glob
sensors = glob.glob('/sys/bus/w1/devices/28-*')
print(f"Found {len(sensors)} sensors")
for s in sensors:
    print(f"  - {s.split('/')[-1]}")
EOF
```

Expected: "Found 3 sensors"

---

Would you like me to:
1. ✅ **Create the complete updated Python script**
2. ✅ **Create the complete updated HA configuration**
3. ✅ **Create a simple installation script**

Let me know and I'll generate the full files!
