# 📊 Complete Dashboard Installation Guide

## ✅ What You Have

**File:** `dashboard-complete.yaml` (900 lines)

This is the **complete 6-tab dashboard** with:
- ✅ Tab 1: Overview - Real-time monitoring
- ✅ Tab 2: Analytics - Charts and trends
- ✅ Tab 3: Settings - Controls and configuration
- ✅ Tab 4: Calibration - Auto-calibration status
- ✅ Tab 5: Advanced - Seasonal stats and alerts history
- ✅ Tab 6: Temperature - Detailed temperature monitoring

---

## 🚀 Quick Installation (5 minutes)

### Step 1: Install Required Components

**You MUST install these from HACS first:**

1. Go to **HACS** → **Frontend**
2. Click **Explore & Download Repositories**
3. Install:
   - ✅ **ApexCharts Card** (for charts)
   - ✅ **Card Mod** (for styling)
   - ✅ **Layout Card** (optional)

**Don't have HACS?** Install it first: https://hacs.xyz/docs/setup/download

### Step 2: Create Dashboard

1. **Settings** → **Dashboards**
2. Click **Add Dashboard**
3. **Name:** "Aquarium ATO"
4. **Icon:** `mdi:fish`
5. Click **Create**

### Step 3: Add Dashboard YAML

1. Open your new "Aquarium ATO" dashboard
2. Click **⋮** (3 dots top right)
3. Click **Edit Dashboard**
4. Click **⋮** (3 dots again)
5. Click **Raw Configuration Editor**
6. **Delete everything** in the editor
7. Open `dashboard-complete.yaml`
8. **Copy ALL content** (Ctrl+A, Ctrl+C)
9. **Paste** into the editor (Ctrl+V)
10. Click **Save**
11. Done! 🎉

---

## 🎨 What You'll See

### Tab 1: Overview
- Current temperature gauge
- Reservoir level gauge
- Today's usage statistics
- 24-hour evaporation chart
- Rate comparison (1h, 6h, 24h)
- Monitoring enable/disable controls
- Live pump status (pulses when running!)
- Active alerts (if any)
- Calibration confidence meter

### Tab 2: Analytics
- 30-day water usage chart
- Multi-rate comparison chart (1h through 30d)
- Weekly statistics cards
- 7-day reservoir depletion trend
- Average daily usage calculations

### Tab 3: Settings
- Safety controls (monitoring on/off)
- Manual pump override
- Refill recording interface
- Temperature calibration tools
- System information display
- Alert thresholds documentation

### Tab 4: Calibration
- Current calibration value gauge
- Confidence percentage meter
- Activations since last refill
- Calibration status with color coding:
  - 🟢 Green: 70-100% (excellent)
  - 🟡 Yellow: 40-69% (good)
  - 🔴 Red: 0-39% (need more data)
- Refill recording controls
- How auto-calibration works explanation

### Tab 5: Advanced
- Current season display with emoji
- Seasonal color-coded cards
- System statistics (alerts, pump cycles)
- Critical alert warnings (if active)
- Maintenance schedule checklist

### Tab 6: Temperature
- Current temperature gauge
- Status card with color coding
- 24-hour temperature trend chart
- 7-day temperature history
- 24h min/max/average statistics
- Sensor calibration interface
- Temperature guidelines for different fish

---

## 🎨 Dashboard Features

### Dynamic Styling
- **Color-coded temperature:**
  - 🔴 Red: Critical (<20°C or >30°C)
  - 🟡 Yellow: Warning (20-22°C or 28-30°C)
  - 🟢 Green: Perfect (24-26°C)

- **Seasonal colors:**
  - ☀️ Summer: Orange/Yellow
  - ❄️ Winter: Blue
  - 🌸 Spring: Green
  - 🍂 Autumn: Orange/Red

- **Pulsing pump indicator:** When pump is running, it pulses!

- **Confidence meter:** Changes color based on calibration quality

### Responsive Design
- Works on desktop, tablet, and mobile
- Cards stack vertically on small screens
- Optimized for touch interfaces

---

## 🔧 Customization

### Change Colors

Find these sections in the YAML and modify colors:

```yaml
card_mod:
  style: |
    ha-card {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      # Change the hex colors above
    }
```

### Adjust Gauge Ranges

For temperature gauge:
```yaml
type: gauge
entity: sensor.ato_tank_temperature
min: 18  # Change minimum
max: 32  # Change maximum
```

### Modify Chart Timeframes

For 24-hour chart:
```yaml
graph_span: 24h  # Change to: 12h, 48h, 7d, etc.
```

### Add/Remove Cards

Delete any card section you don't want or duplicate sections to add more.

---

## ⚠️ Troubleshooting

### "Custom element doesn't exist: apexcharts-card"

**Solution:** Install ApexCharts Card from HACS
1. HACS → Frontend
2. Search "ApexCharts"
3. Install
4. Restart Home Assistant
5. Clear browser cache (Ctrl+Shift+R)

### "Custom element doesn't exist: card-mod"

**Solution:** Install Card Mod from HACS
1. HACS → Frontend
2. Search "Card Mod"
3. Install
4. Restart Home Assistant
5. Clear browser cache

### Charts Not Showing Data

**Possible causes:**
1. Entities don't have history yet (wait a few hours)
2. Recorder not enabled
3. Entity names don't match

**Check:**
- Developer Tools → States → Verify entity names
- Configuration → Recorder → Ensure enabled

### Cards Showing "Unknown" or "Unavailable"

**Solution:**
1. Check Raspberry Pi script is running
2. Verify MQTT messages: Developer Tools → MQTT → Listen: `aquarium/#`
3. Check entity names match exactly

### Dashboard Loads Slowly

**Solution:**
- Reduce `graph_span` in charts (from 30d to 7d)
- Remove some ApexCharts cards
- Disable Card Mod animations

---

## 📱 Mobile View

The dashboard is fully responsive! On mobile:
- Cards stack vertically
- Gauges resize automatically
- Charts adapt to screen width
- Touch-friendly buttons

**Tip:** Add to home screen for app-like experience:
1. Open dashboard on phone
2. Browser menu → "Add to Home Screen"
3. Creates icon on home screen

---

## 🎓 Advanced Tips

### Add More Sensors

You can add any Home Assistant entity:

```yaml
- type: entity
  entity: sensor.YOUR_SENSOR
  name: Custom Name
  icon: mdi:icon-name
```

### Create Conditional Cards

Show cards only when conditions are met:

```yaml
- type: conditional
  conditions:
    - entity: sensor.ato_reservoir_level
      state_not: "below"
      below: 5
  card:
    type: markdown
    content: "⚠️ Reservoir low!"
```

### Add Custom Templates

Use template cards for complex logic:

```yaml
- type: markdown
  content: |
    {% set level = states('sensor.ato_reservoir_level') | float %}
    {% if level < 5 %}
    🔴 Refill NOW!
    {% elif level < 10 %}
    🟡 Refill soon
    {% else %}
    🟢 Level OK
    {% endif %}
```

---

## 📊 Example: Simple Alternative Dashboard

If the full dashboard is too complex, here's a minimal version:

```yaml
title: ATO Simple
views:
  - title: Main
    cards:
      - type: entities
        entities:
          - sensor.ato_tank_temperature
          - sensor.ato_reservoir_level
          - sensor.ato_daily_usage
          - sensor.ato_rate_24_hours
          - switch.ato_monitoring_enable
      
      - type: history-graph
        entities:
          - sensor.ato_tank_temperature
        hours_to_show: 24
```

---

## 🆘 Need Help?

1. **Check the logs:**
   - Settings → System → Logs
   - Look for errors related to cards

2. **Validate YAML:**
   - Use online YAML validator
   - Check indentation (spaces, not tabs!)

3. **Browser console:**
   - Press F12
   - Check Console tab for errors

4. **Community:**
   - Home Assistant forums
   - Reddit: r/homeassistant
   - GitHub Issues

---

## ✅ Checklist

Before installing:
- [ ] HACS installed
- [ ] ApexCharts Card installed
- [ ] Card Mod installed
- [ ] All entities exist (check Developer Tools → States)
- [ ] MQTT working (messages flowing)
- [ ] Configuration.yaml added and HA restarted

After installing:
- [ ] Dashboard loads without errors
- [ ] Gauges show values
- [ ] Charts render
- [ ] Switches work
- [ ] Colors display correctly
- [ ] Mobile view works

---

**Your complete 6-tab dashboard is ready! Enjoy monitoring your aquarium! 🐠💙**

File: `dashboard-complete.yaml` (900 lines)
