"""
ATO Aquarium Monitor - Configuration File (3 Temperature Sensors)
Copy this file to config.py and update with your settings
"""

# ============================================================================
# MQTT BROKER CONFIGURATION
# ============================================================================
MQTT_BROKER = "192.168.1.100"  # Your Home Assistant IP address
MQTT_PORT = 1883
MQTT_USER = "your_mqtt_username"  # MQTT username
MQTT_PASS = "your_mqtt_password"  # MQTT password

# ============================================================================
# GPIO PIN CONFIGURATION (BCM numbering)
# ============================================================================
FLOAT_PIN = 17  # Float switch input (GPIO 17, Pin 11)
PUMP_PIN = 27   # Relay control output (GPIO 27, Pin 13)

# Temperature sensors use GPIO 4 (Pin 7) - all DS18B20 on same 1-Wire bus
# Individual sensors identified by their unique IDs

# ============================================================================
# DS18B20 SENSOR CONFIGURATION
# ============================================================================
# After connecting sensors, run: ls /sys/bus/w1/devices/28-*
# Copy the full IDs and paste below

# Sensor 1: ATO Reservoir (original)
TEMP_SENSOR_ATO_ID = "28-xxxxxxxxxxxx"  # Replace with actual ID
TEMP_SENSOR_ATO_NAME = "ATO Reservoir"

# Sensor 2: Main Display Tank
TEMP_SENSOR_DISPLAY_ID = "28-xxxxxxxxxxxx"  # Replace with actual ID
TEMP_SENSOR_DISPLAY_NAME = "Display Tank"

# Sensor 3: Sump
TEMP_SENSOR_SUMP_ID = "28-xxxxxxxxxxxx"  # Replace with actual ID
TEMP_SENSOR_SUMP_NAME = "Sump"

# If you want auto-detection instead of manual IDs:
AUTO_DETECT_SENSORS = True  # Set to False to use manual IDs above

# ============================================================================
# TANK & RESERVOIR CONFIGURATION
# ============================================================================
RESERVOIR_CAPACITY = 23.0       # Reservoir capacity in liters
LITERS_PER_ACTIVATION = 1.0     # Initial estimate (will auto-calibrate)

# ============================================================================
# FILE PATHS (Data storage)
# ============================================================================
HISTORY_FILE = "/home/pi/ato_history.pkl"
CALIBRATION_FILE = "/home/pi/ato_calibration.pkl"
ALERTS_HISTORY_FILE = "/home/pi/ato_alerts_history.pkl"
PUMP_PERFORMANCE_FILE = "/home/pi/ato_pump_performance.pkl"
TEMP_HISTORY_FILE = "/home/pi/ato_temp_history.pkl"
TEMP_CALIBRATION_FILE = "/home/pi/ato_temp_calibration.pkl"

# ============================================================================
# ALERT THRESHOLDS
# ============================================================================
MAX_ACTIVATIONS_PER_HOUR = 3    # Alert if more activations in 1 hour
MIN_HOURS_BETWEEN = 4           # Alert if activations too frequent
MAX_HOURS_BETWEEN = 36          # Alert if no activations for this long
MAX_DAILY_USAGE = 6.0           # Maximum liters per day (adjust for season)
LOW_RESERVOIR_WARNING = 5.0     # Alert when reservoir drops below this
MAX_FILL_DURATION = 30          # Maximum pump runtime in seconds (safety)

# ============================================================================
# TEMPERATURE THRESHOLDS (°Celsius)
# ============================================================================
# These apply to Display Tank and Sump (main monitoring)
# ATO reservoir temp is tracked but doesn't trigger alerts

# Display Tank & Sump thresholds
TEMP_MIN_WARNING = 22.0   # Low temperature warning
TEMP_MAX_WARNING = 28.0   # High temperature warning
TEMP_MIN_CRITICAL = 20.0  # Critical low temperature (emergency)
TEMP_MAX_CRITICAL = 30.0  # Critical high temperature (emergency)

# Temperature difference alert (Display vs Sump)
TEMP_DIFF_WARNING = 2.0   # Alert if display and sump differ by this much
TEMP_DIFF_CRITICAL = 3.0  # Critical alert for temp difference

# ============================================================================
# SEASONAL ADJUSTMENTS (Optional)
# ============================================================================
# You can adjust MAX_DAILY_USAGE by season if needed:
# SUMMER_MAX_DAILY_USAGE = 8.0
# WINTER_MAX_DAILY_USAGE = 4.0
