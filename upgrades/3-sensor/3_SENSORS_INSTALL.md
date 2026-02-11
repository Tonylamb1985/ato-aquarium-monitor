# 🚀 3-Sensor Installation Guide

## Quick Installation Path

Since the full Python script is very large (~2000 lines), I recommend this approach:

### Option 1: Modification Script (Recommended - 5 minutes)

I'll create a **patch script** that automatically modifies your existing `ato_monitor.py` to support 3 sensors.

**Steps:**
1. Run the patch script
2. Update config.py
3. Update Home Assistant config
4. Add dashboard tab
5. Done!

### Option 2: Complete Replacement (10 minutes)

Download the complete new Python script and replace the old one.

---

## 🔧 Option 1: Automated Patch (Easiest)

### Step 1: Download Patch Script

I'll create `patch_3sensors.sh` that:
- Backs up your current script
- Adds multi-sensor support
- Preserves all your data
- Takes 30 seconds to run

### Step 2: Run Patch

```bash
cd /home/pi/ato-aquarium-monitor
bash patch_3sensors.sh
```

### Step 3: Update Config

```bash
cp config.py config_backup.py
nano config.py
```

Add these lines:
```python
# Multiple sensor support
AUTO_DETECT_SENSORS = True

# Or manual assignment:
# TEMP_SENSOR_DISPLAY_ID = "28-xxxx"
# TEMP_SENSOR_SUMP_ID = "28-yyyy"
# TEMP_SENSOR_ATO_ID = "28-zzzz"
```

### Step 4: Restart Service

```bash
sudo systemctl restart ato-monitor.service
sudo systemctl status ato-monitor.service
```

### Step 5: Update Home Assistant

See `home-assistant-3sensors/` folder for config snippets to add.

---

## 📝 What Gets Modified

### Key Changes to ato_monitor.py:

**1. Sensor Data Structure**
```python
# OLD (single sensor):
current_temperature = None

# NEW (3 sensors):
temp_sensors = {
    'display': {...},
    'sump': {...},
    'ato': {...}
}
```

**2. Detection Function**
```python
# Finds all 3 sensors automatically
def find_all_temp_sensors():
    sensors = glob.glob('/sys/bus/w1/devices/28-*')
    # Auto-assign or use manual IDs
```

**3. Reading Function**
```python
# Reads all 3 sensors in one loop
def read_all_temperatures():
    for sensor_key in temp_sensors:
        # Read each sensor
        # Apply individual calibration
```

**4. MQTT Publishing**
```python
# Publishes all temperature data
client.publish("aquarium/temp/display", ...)
client.publish("aquarium/temp/sump", ...)
client.publish("aquarium/temp/display_sump_diff", ...)
```

**5. Alert Logic**
```python
# Enhanced temperature alerts
# Temperature difference monitoring
if abs(display_temp - sump_temp) > TEMP_DIFF_WARNING:
    # Alert!
```

---

## 🏠 Home Assistant Changes

### New Sensors to Add

Add to your `configuration.yaml`:

```yaml
mqtt:
  sensor:
    # Display Tank (6 sensors)
    - name: "Display Tank Temperature"
      state_topic: "aquarium/temp/display"
      ...
    
    - name: "Display Tank Temperature Raw"
      state_topic: "aquarium/temp/display_raw"
      ...
    
    - name: "Display Tank 24h Average"
      state_topic: "aquarium/temp/display_stats"
      value_template: "{{ value_json.avg_24h }}"
      ...
    
    # Sump (6 sensors)
    - name: "Sump Temperature"
      state_topic: "aquarium/temp/sump"
      ...
    
    # Temperature Difference
    - name: "Display Sump Temp Difference"
      state_topic: "aquarium/temp/display_sump_diff"
      ...
  
  number:
    # 3 Calibration controls
    - name: "Display Tank Temp Calibration"
      command_topic: "aquarium/temp/display_calibration_set"
      ...
```

**Total new entities: ~15**

Full config in: `home-assistant-3sensors/configuration_3sensors.yaml`

---

## 📊 Dashboard Update

### Add New Tab

Copy the "All Temperatures" tab from `dashboard_3sensors.yaml`

**What it includes:**
- 3 temperature gauges
- Temperature difference indicator
- 24h comparison chart
- Individual calibration controls
- Color-coded alerts

---

## ✅ Verification Steps

### 1. Check Sensors Detected

```bash
# Should show 3 sensors
ls /sys/bus/w1/devices/28-*
```

### 2. Check Script Running

```bash
sudo systemctl status ato-monitor.service

# Should show:
# "Found 3 temperature sensors"
```

### 3. Check MQTT Messages

```bash
mosquitto_sub -h YOUR_HA_IP -t 'aquarium/temp/#' -v
```

Should see:
```
aquarium/temp/display 24.5
aquarium/temp/sump 24.3
aquarium/temp/display_sump_diff 0.2
```

### 4. Check Home Assistant

Developer Tools → States → Search "temp"

Should see:
- `sensor.display_tank_temperature`
- `sensor.sump_temperature`
- `sensor.display_sump_temp_difference`

---

## 🔧 Troubleshooting

### Only 2 Sensors Detected

**Check:**
1. All 3 sensors wired to GPIO 4?
2. All sensors powered (3.3V)?
3. Pull-up resistor installed?

**Solution:**
```bash
# Test each sensor
for sensor in /sys/bus/w1/devices/28-*/w1_slave; do
    echo "Sensor: $sensor"
    cat "$sensor" | grep "t="
done
```

### Auto-Detect Assigns Wrong Sensors

**Solution:**
Use manual assignment in config.py:

```python
AUTO_DETECT_SENSORS = False
TEMP_SENSOR_DISPLAY_ID = "28-actual-id-here"
TEMP_SENSOR_SUMP_ID = "28-actual-id-here"
TEMP_SENSOR_ATO_ID = "28-actual-id-here"
```

Find IDs by touching each sensor and seeing which temperature changes!

### Script Won't Start After Patch

**Solution:**
```bash
# Check logs
journalctl -u ato-monitor.service -n 50

# Restore backup if needed
cp ato_monitor_original.py ato_monitor.py
sudo systemctl restart ato-monitor.service
```

### Temperature Difference Always High

**Solution:**
Calibrate each sensor individually:
1. Use reference thermometer
2. Set offset for each sensor
3. Re-check difference

---

## 📦 File Structure

```
ato-aquarium-monitor/
├── ato_monitor.py          (original - keep as backup)
├── ato_monitor_3sensors.py (new version)
├── config_3sensors.py      (example config)
├── patch_3sensors.sh       (auto-patch script)
├── 3_SENSORS_README.md     (this file)
├── MULTI_SENSOR_WIRING.md  (wiring guide)
└── home-assistant-3sensors/
    ├── configuration_3sensors.yaml
    └── dashboard_3sensors.yaml
```

---

## ⚡ Quick Command Reference

```bash
# Find sensors
ls /sys/bus/w1/devices/28-*

# Test sensors
cat /sys/bus/w1/devices/28-*/w1_slave

# Run patch
bash patch_3sensors.sh

# Restart service
sudo systemctl restart ato-monitor.service

# View logs
journalctl -u ato-monitor.service -f

# Check MQTT
mosquitto_sub -h YOUR_HA_IP -t 'aquarium/temp/#' -v
```

---

## 🎯 What to Expect

### After Installation:

**Home Assistant entities:**
- ✅ Display Tank Temperature
- ✅ Sump Temperature  
- ✅ ATO Temperature (existing, kept)
- ✅ Display-Sump Difference
- ✅ 3 calibration controls
- ✅ Stats for each sensor

**Dashboard:**
- ✅ New "All Temperatures" tab
- ✅ 3 gauges side-by-side
- ✅ Comparison chart
- ✅ Difference indicator

**Alerts:**
- ✅ Critical temps on Display/Sump
- ✅ Temperature difference warnings
- ✅ Rapid temp change detection

---

## 🆘 Need Help?

1. Check `MULTI_SENSOR_WIRING.md` for wiring
2. Check `3_SENSOR_UPGRADE_GUIDE.md` for details
3. View logs: `journalctl -u ato-monitor.service -f`
4. Test MQTT: `mosquitto_sub -h IP -t 'aquarium/#'`

---

**Ready to install! Choose your path and let's get 3 sensors running! 🌡️🌡️🌡️**
