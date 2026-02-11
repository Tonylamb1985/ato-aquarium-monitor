# 🏠 Home Assistant Configuration

This folder contains Home Assistant configuration files for the ATO Aquarium Monitor.

## 📁 Files Included

1. **configuration.yaml** - MQTT sensors, switches, automations

## 📊 Dashboard Setup

Due to the size and complexity of the 6-tab dashboard (over 3,000 lines of YAML), I recommend building it step-by-step rather than providing pre-made files.

### Quick Dashboard Creation

**Option 1: Use Home Assistant UI (Recommended)**

1. Go to **Settings** → **Dashboards**
2. Click **Add Dashboard**
3. Name: "Aquarium ATO"
4. Add tabs manually using the cards below

**Option 2: Use the Original Project Documentation**

The complete project documentation (`ATO_Aquarium_Monitor_Project.md`) contains all dashboard YAML in the original design.

## 🎨 Dashboard Tabs Overview

### Tab 1: Overview
**Essential Cards:**
- Current temperature gauge
- Reservoir level gauge  
- Today's usage
- Real-time evaporation rate (24h)
- Pump state indicator
- Enable/disable monitoring switch

**Quick Start:**
```yaml
type: entities
entities:
  - entity: sensor.ato_tank_temperature
  - entity: sensor.ato_reservoir_level
  - entity: sensor.ato_daily_usage
  - entity: sensor.ato_rate_24_hours
  - entity: switch.ato_monitoring_enable
```

### Tab 2: Analytics
**Cards:**
- 30-day usage history chart
- Evaporation rate comparison (all timeframes)
- Weekly trends

**Requires:** ApexCharts Card (HACS)

### Tab 3: Settings
**Cards:**
- Monitoring controls
- Manual pump override
- Calibration inputs
- Alert threshold display
- System diagnostics

### Tab 4: Calibration
**Cards:**
- Auto-calibration status
- Confidence meter
- Calibration history table
- Refill recording

### Tab 5: Advanced
**Cards:**
- Seasonal statistics
- Alerts history
- Pump performance tracking

### Tab 6: Temperature
**Cards:**
- Temperature charts
- 24h/7d statistics
- Calibration interface
- Alert thresholds

## 🔧 Installation Steps

### Step 1: Add MQTT Configuration

1. Open your Home Assistant `configuration.yaml`
2. Copy the contents of `configuration.yaml` from this folder
3. Paste at the end of your file
4. **Important:** Update `YOUR_PHONE` in automations:
   ```yaml
   # Find this line:
   service: notify.mobile_app_YOUR_PHONE
   
   # Replace with your actual device, example:
   service: notify.mobile_app_tonys_phone
   ```
5. Check configuration: **Developer Tools** → **YAML** → **Check Configuration**
6. Restart Home Assistant

### Step 2: Verify Entities

1. Go to **Developer Tools** → **States**
2. Search for `ato`
3. You should see 30+ entities like:
   - `sensor.ato_tank_temperature`
   - `sensor.ato_reservoir_level`
   - `switch.ato_monitoring_enable`
   - etc.

### Step 3: Install Required Frontend Components (for fancy dashboards)

1. Install **HACS** if you haven't: https://hacs.xyz/docs/setup/download
2. Go to **HACS** → **Frontend**
3. Install:
   - **ApexCharts Card** (for charts)
   - **Card Mod** (for styling)
   - **Layout Card** (for layouts) - optional

### Step 4: Create Basic Dashboard

**Simple 1-Tab Dashboard (5 minutes):**

1. Go to **Settings** → **Dashboards**
2. Click **Add Dashboard**
3. Name: "Aquarium ATO"
4. Edit Dashboard → Add Card
5. Choose **Entities Card**
6. Add these entities:
   ```
   - sensor.ato_tank_temperature
   - sensor.ato_reservoir_level
   - sensor.ato_reservoir_percent
   - sensor.ato_daily_usage
   - sensor.ato_rate_24_hours
   - sensor.ato_calibrated_l_activation
   - sensor.ato_calibration_confidence
   - switch.ato_monitoring_enable
   - switch.ato_manual_pump
   ```
7. Save

You now have a functional dashboard!

### Step 5: Build Advanced Dashboard (Optional)

Once the basic dashboard works, you can add:
- Gauge cards for visual indicators
- History graphs
- ApexCharts for detailed analytics
- Custom styling with Card Mod

## 📱 Mobile App Notifications

To receive alerts on your phone:

1. Install **Home Assistant Companion App** on your phone
2. Log in to your Home Assistant
3. The app will automatically register as a notification target
4. Find your device name in:
   - **Settings** → **Devices & Services** → **Mobile App**
5. Update automations in `configuration.yaml` with your device name

Example device names:
- `mobile_app_tonys_phone`
- `mobile_app_pixel_7`
- `mobile_app_iphone`

## 🎨 Customization

### Change Update Frequency

Default: Stats publish every 5 minutes

To change, edit `ato_monitor.py`:
```python
# Find this line (around line 1420):
if int(time.time()) % 300 == 0:  # 300 = 5 minutes

# Change to (example: 2 minutes):
if int(time.time()) % 120 == 0:  # 120 = 2 minutes
```

### Customize Notification Channels

Edit the automations to add channels:
```yaml
data:
  channel: "ATO Alerts"  # Creates separate notification category
  importance: high        # Android: high, max, low
  priority: high          # iOS priority
```

### Add More Sensors

You can create template sensors for custom calculations:

```yaml
template:
  - sensor:
      - name: "ATO Water Cost Today"
        unit_of_measurement: "$"
        state: >
          {{ (states('sensor.ato_daily_usage') | float * 0.002) | round(2) }}
        # Assuming $0.002 per liter
```

## 🔍 Troubleshooting

### Entities Not Appearing

1. Check MQTT integration is configured
2. Verify Mosquitto broker is running
3. Check Developer Tools → MQTT → Listen to: `aquarium/#`
4. Should see messages flowing

### Automations Not Firing

1. Check automation is enabled
2. Verify mobile app is registered
3. Test with: **Developer Tools** → **Services** → `notify.mobile_app_YOUR_DEVICE`

### Dashboard Cards Not Loading

1. Clear browser cache (Ctrl+Shift+R)
2. Check HACS components are installed
3. View browser console (F12) for errors

## 📚 Resources

- **Home Assistant Docs:** https://www.home-assistant.io/docs/
- **MQTT Integration:** https://www.home-assistant.io/integrations/mqtt/
- **Dashboard Cards:** https://www.home-assistant.io/dashboards/
- **ApexCharts Card:** https://github.com/RomRider/apexcharts-card
- **Card Mod:** https://github.com/thomasloven/lovelace-card-mod

## 💡 Tips

- Start with basic dashboard, add complexity later
- Use **Developer Tools** → **Template** to test templates
- Check **Developer Tools** → **States** to see entity values
- Use **Settings** → **System** → **Logs** for error messages

---

**Need help? Check the main project documentation or open an issue on GitHub!** 🐠💙
