# 🧪 NT Labs Liquid Tests - Water Test System

## NT Labs Freshwater Test Kits

**Configured for:**
- NT Labs Ammonia Test Kit
- NT Labs Nitrite Test Kit
- NT Labs Nitrate Test Kit
- NT Labs pH Test Kit
- NT Labs GH & KH Test Kit (optional)

**Test Type:** Liquid reagent (drops into test tube)

---

## 📸 Camera Setup for Liquid Tests

### Differences from Test Strips:

```
Test Strips:
- Hold to camera
- Multiple pads visible
- Quick snapshot

Liquid Tests (NT Labs):
- Test tube in holder
- Single color per tube
- White background important
- Needs stable positioning
```

### Recommended Setup:

```
Camera View:
┌─────────────────────────┐
│                         │
│   ┌─┐ ┌─┐ ┌─┐ ┌─┐     │
│   │A│ │N│ │N│ │P│     │  ← Test tubes in rack
│   │m│ │i│ │a│ │H│     │
│   │m│ │t│ │t│ │ │     │
│   └─┘ └─┘ └─┘ └─┘     │
│                         │
│   White Background      │
│                         │
└─────────────────────────┘
```

---

## ⚙️ NT Labs Configuration

### config.yaml (NT Labs Liquid Tests):

```yaml
# NT Labs Freshwater Liquid Test Configuration

# Test tube positions (x1, y1, x2, y2)
# Each tube in a rack, white background
# Calibrate these for your camera angle
test_regions:
  ammonia: [150, 200, 200, 450]    # First tube
  nitrite: [250, 200, 300, 450]    # Second tube
  nitrate: [350, 200, 400, 450]    # Third tube
  ph: [450, 200, 500, 450]         # Fourth tube
  # Optional KH/GH tests
  kh: [550, 200, 600, 450]         # Fifth tube (optional)
  gh: [650, 200, 700, 450]         # Sixth tube (optional)

# NT Labs Color Charts - Freshwater
# These are calibrated for NT Labs reagents in test tubes
color_charts:
  
  # NT Labs Ammonia Test Kit (yellow to green)
  ammonia:
    [255, 255, 200]: 0.0      # Very pale yellow (safe)
    [255, 250, 180]: 0.1      # Pale yellow
    [255, 245, 160]: 0.25     # Light yellow
    [250, 240, 140]: 0.5      # Yellow
    [245, 235, 120]: 0.75     # Deeper yellow
    [240, 225, 100]: 1.0      # Yellow-green tint
    [230, 215, 90]: 1.5       # Yellow-green
    [220, 200, 80]: 2.0       # Green-yellow
    [210, 185, 75]: 3.0       # More green
    [200, 170, 70]: 4.0       # Green (danger)
    [190, 155, 65]: 6.0       # Dark green (very dangerous)
    [180, 140, 60]: 8.0       # Very dark green (critical)
  
  # NT Labs Nitrite Test Kit (clear to purple/pink)
  nitrite:
    [250, 250, 255]: 0.0      # Clear/very pale (safe)
    [245, 240, 250]: 0.05     # Very faint pink
    [240, 230, 245]: 0.1      # Faint pink
    [235, 220, 240]: 0.15     # Light pink
    [225, 210, 235]: 0.25     # Pink
    [215, 195, 230]: 0.5      # Medium pink
    [200, 180, 220]: 0.75     # Deeper pink
    [185, 160, 210]: 1.0      # Pink-purple
    [170, 145, 200]: 1.5      # Purple-pink
    [155, 130, 190]: 2.0      # Purple (danger)
    [140, 115, 180]: 3.0      # Dark purple (very dangerous)
    [125, 100, 170]: 5.0      # Very dark purple (critical)
  
  # NT Labs Nitrate Test Kit (clear to orange/red)
  nitrate:
    [255, 255, 250]: 0        # Clear (excellent)
    [255, 250, 240]: 5        # Very faint yellow
    [255, 245, 225]: 10       # Pale yellow
    [255, 240, 210]: 12.5     # Light yellow
    [255, 235, 195]: 20       # Yellow
    [250, 225, 175]: 25       # Deeper yellow
    [245, 215, 155]: 40       # Yellow-orange
    [240, 200, 135]: 50       # Light orange
    [230, 180, 115]: 80       # Orange
    [220, 160, 95]: 100       # Deep orange
    [210, 140, 75]: 150       # Orange-red
    [200, 120, 60]: 200       # Red-orange (very high)
  
  # NT Labs pH Test Kit (yellow to blue via green)
  ph:
    [255, 220, 100]: 6.0      # Yellow (acidic)
    [250, 225, 110]: 6.2      # Yellow
    [240, 230, 120]: 6.4      # Yellow-green
    [225, 235, 130]: 6.6      # Yellow-green
    [210, 235, 140]: 6.8      # Green-yellow
    [190, 235, 150]: 7.0      # Light green (neutral)
    [170, 230, 160]: 7.2      # Green
    [150, 225, 175]: 7.4      # Green-blue
    [130, 215, 190]: 7.6      # Blue-green
    [110, 205, 205]: 7.8      # Teal
    [90, 190, 220]: 8.0       # Light blue
    [75, 175, 230]: 8.2       # Blue (alkaline)
    [65, 160, 235]: 8.4       # Medium blue
    [55, 145, 240]: 8.6       # Deep blue
    [50, 130, 240]: 8.8       # Very deep blue
  
  # NT Labs KH Test Kit (optional - drop counting)
  # This uses drop counting, not color
  # Each drop = 1 dKH until color changes from blue to yellow
  kh:
    [100, 150, 220]: 0        # Blue (no KH)
    [255, 220, 100]: 1        # Yellow (after drops)
  
  # NT Labs GH Test Kit (optional - drop counting)
  # Each drop = 1 dGH until color changes from orange to green
  gh:
    [240, 160, 100]: 0        # Orange (no GH)
    [120, 200, 140]: 1        # Green (after drops)

# NT Labs specific settings
test_type: "liquid_reagent"
manufacturer: "NT Labs"
test_method: "color_matching"  # vs "drop_counting" for KH/GH

# Camera and lighting requirements
camera_requirements:
  background: "white"           # Essential for accurate colors
  lighting: "bright_white"      # 5000K-6500K LED
  tube_holder: "required"       # Keep tubes stable
  distance: "20-30cm"           # Camera to tubes
  
# Analysis settings optimized for liquid tests
analysis_settings:
  # Larger sampling area (entire tube visible)
  sample_percentage: 80         # Use 80% of tube region
  
  # More aggressive outlier removal (reflections on glass)
  outlier_removal: "aggressive"
  
  # Color space for better accuracy
  color_space: "LAB"            # Better than RGB for liquids
  
  # Confidence thresholds
  min_confidence: 75            # Lower than strips (liquids vary more)
  excellent_confidence: 88
  
  # Tube detection (optional - auto-find tubes)
  auto_detect_tubes: false      # Set true for automatic tube finding
  expected_tubes: 4             # Number of tubes expected

# Usage instructions
usage_notes: |
  NT Labs Liquid Test Procedure:
  1. Add reagent drops as per instructions
  2. Wait development time (usually 5-10 minutes)
  3. Place tubes in rack with white background
  4. Ensure good lighting (no shadows)
  5. Position rack in camera view
  6. Trigger analysis
  
  For KH/GH tests:
  - These use drop counting, not color matching
  - Manual entry recommended
  - Or use advanced drop detection (future feature)
```

---

## 🎨 Enhanced Python Script for Liquid Tests

### Modifications to water_test_analyzer.py:

Add this specialized method for NT Labs:

```python
def analyze_liquid_test_tube(self, image, region):
    """
    Specialized analysis for liquid tests in tubes
    Different from test strips - accounts for:
    - Glass reflections
    - Tube curvature
    - Liquid transparency
    - Background bleeding
    """
    
    x1, y1, x2, y2 = region
    tube_roi = image[y1:y2, x1:x2]
    
    # Convert to LAB color space (better for liquids)
    lab_roi = cv2.cvtColor(tube_roi, cv2.COLOR_RGB2LAB)
    
    # Extract center 80% to avoid edges (glass reflection)
    h, w = tube_roi.shape[:2]
    margin_h = int(h * 0.1)
    margin_w = int(w * 0.1)
    center_roi = lab_roi[margin_h:-margin_h, margin_w:-margin_w]
    
    # Find the most representative color (mode, not mean)
    # Liquids have more uniform color than strips
    pixels = center_roi.reshape(-1, 3).astype(np.float32)
    
    # Use clustering to find dominant color
    from sklearn.cluster import KMeans
    
    # Find 3 dominant colors
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    # Get the most common cluster
    labels = kmeans.labels_
    unique, counts = np.unique(labels, return_counts=True)
    dominant_cluster = unique[np.argmax(counts)]
    
    # Get color of dominant cluster
    dominant_color_lab = kmeans.cluster_centers_[dominant_cluster]
    
    # Convert back to RGB
    dominant_color_lab = dominant_color_lab.reshape(1, 1, 3).astype(np.uint8)
    dominant_color_rgb = cv2.cvtColor(dominant_color_lab, cv2.COLOR_LAB2RGB)
    result_color = tuple(dominant_color_rgb[0, 0])
    
    # Also calculate standard deviation (quality check)
    cluster_pixels = pixels[labels == dominant_cluster]
    std_dev = np.std(cluster_pixels, axis=0)
    color_uniformity = 100 - min(100, np.mean(std_dev))
    
    return result_color, color_uniformity
```

---

## 📊 Dashboard Tab - Water Testing

### Add to dashboard-MEGA-all-upgrades.yaml:

```yaml
# ==========================================================================
# TAB 10: WATER TESTING (NT Labs Liquid Tests)
# ==========================================================================
- title: Water Testing
  path: water_testing
  icon: mdi:test-tube
  cards:
    # Header
    - type: markdown
      content: |
        # 🧪 Water Testing - NT Labs
        Liquid reagent tests with automated analysis
      card_mod:
        style: |
          ha-card {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            text-align: center;
            font-size: 1.2em;
          }
    
    # Quick Actions
    - type: horizontal-stack
      cards:
        - type: custom:mushroom-template-card
          primary: "Take Test Photo"
          secondary: "Position tubes & capture"
          icon: mdi:camera
          icon_color: blue
          tap_action:
            action: call-service
            service: script.aquarium_water_test_snapshot
        
        - type: custom:mushroom-template-card
          primary: "Last Test"
          secondary: >
            {% set time = state_attr('sensor.water_test_confidence', 'timestamp') %}
            {% if time %}
              {{ as_timestamp(time) | timestamp_custom('%b %d, %I:%M %p') }}
            {% else %}
              Never
            {% endif %}
          icon: mdi:clock-outline
          icon_color: grey
        
        - type: custom:mushroom-template-card
          primary: "Test Status"
          secondary: >
            {% set conf = states('sensor.water_test_confidence')|float(0) %}
            {% if conf >= 88 %}🟢 Excellent
            {% elif conf >= 75 %}🟡 Good
            {% else %}🔴 Retake
            {% endif %}
            ({{ conf }}%)
          icon: mdi:clipboard-check
          icon_color: >
            {% set conf = states('sensor.water_test_confidence')|float(0) %}
            {% if conf >= 88 %}green
            {% elif conf >= 75 %}yellow
            {% else %}red
            {% endif %}
    
    # Current Test Results
    - type: entities
      title: 📋 Current Test Results
      show_header_toggle: false
      entities:
        # Ammonia
        - type: custom:mushroom-template-card
          primary: "Ammonia (NH3)"
          secondary: >
            {{ states('sensor.aquarium_ammonia_test') }} ppm
          icon: mdi:molecule
          icon_color: >
            {% set val = states('sensor.aquarium_ammonia_test')|float(0) %}
            {% if val == 0 %}green
            {% elif val <= 0.25 %}yellow
            {% elif val <= 0.5 %}orange
            {% else %}red
            {% endif %}
          badge_icon: >
            {% set conf = state_attr('sensor.aquarium_ammonia_test', 'confidence')|float(0) %}
            {% if conf >= 88 %}mdi:check-circle
            {% elif conf >= 75 %}mdi:alert-circle
            {% else %}mdi:close-circle
            {% endif %}
          badge_color: >
            {% set conf = state_attr('sensor.aquarium_ammonia_test', 'confidence')|float(0) %}
            {% if conf >= 88 %}green
            {% elif conf >= 75 %}yellow
            {% else %}red
            {% endif %}
          tap_action:
            action: more-info
          multiline_secondary: true
        
        - entity: sensor.aquarium_ammonia_test
          name: "  └─ Confidence"
          secondary_info: attribute
          attribute: confidence
          icon: mdi:gauge
        
        - type: divider
        
        # Nitrite
        - type: custom:mushroom-template-card
          primary: "Nitrite (NO2)"
          secondary: >
            {{ states('sensor.aquarium_nitrite_test') }} ppm
          icon: mdi:water-alert
          icon_color: >
            {% set val = states('sensor.aquarium_nitrite_test')|float(0) %}
            {% if val == 0 %}green
            {% elif val <= 0.15 %}yellow
            {% elif val <= 0.5 %}orange
            {% else %}red
            {% endif %}
          badge_icon: >
            {% set conf = state_attr('sensor.aquarium_nitrite_test', 'confidence')|float(0) %}
            {% if conf >= 88 %}mdi:check-circle
            {% elif conf >= 75 %}mdi:alert-circle
            {% else %}mdi:close-circle
            {% endif %}
          badge_color: >
            {% set conf = state_attr('sensor.aquarium_nitrite_test', 'confidence')|float(0) %}
            {% if conf >= 88 %}green
            {% elif conf >= 75 %}yellow
            {% else %}red
            {% endif %}
        
        - entity: sensor.aquarium_nitrite_test
          name: "  └─ Confidence"
          secondary_info: attribute
          attribute: confidence
          icon: mdi:gauge
        
        - type: divider
        
        # Nitrate
        - type: custom:mushroom-template-card
          primary: "Nitrate (NO3)"
          secondary: >
            {{ states('sensor.aquarium_nitrate_test') }} ppm
          icon: mdi:water
          icon_color: >
            {% set val = states('sensor.aquarium_nitrate_test')|float(0) %}
            {% if val <= 20 %}green
            {% elif val <= 40 %}yellow
            {% elif val <= 80 %}orange
            {% else %}red
            {% endif %}
          badge_icon: >
            {% set conf = state_attr('sensor.aquarium_nitrate_test', 'confidence')|float(0) %}
            {% if conf >= 88 %}mdi:check-circle
            {% elif conf >= 75 %}mdi:alert-circle
            {% else %}mdi:close-circle
            {% endif %}
          badge_color: >
            {% set conf = state_attr('sensor.aquarium_nitrite_test', 'confidence')|float(0) %}
            {% if conf >= 88 %}green
            {% elif conf >= 75 %}yellow
            {% else %}red
            {% endif %}
        
        - entity: sensor.aquarium_nitrate_test
          name: "  └─ Confidence"
          secondary_info: attribute
          attribute: confidence
          icon: mdi:gauge
        
        - type: divider
        
        # pH
        - type: custom:mushroom-template-card
          primary: "pH Level"
          secondary: >
            {{ states('sensor.aquarium_ph_test') }}
          icon: mdi:ph
          icon_color: >
            {% set val = states('sensor.aquarium_ph_test')|float(7.0) %}
            {% if val >= 6.5 and val <= 7.5 %}green
            {% elif val >= 6.0 and val <= 8.0 %}yellow
            {% else %}orange
            {% endif %}
          badge_icon: >
            {% set conf = state_attr('sensor.aquarium_ph_test', 'confidence')|float(0) %}
            {% if conf >= 88 %}mdi:check-circle
            {% elif conf >= 75 %}mdi:alert-circle
            {% else %}mdi:close-circle
            {% endif %}
          badge_color: >
            {% set conf = state_attr('sensor.aquarium_ph_test', 'confidence')|float(0) %}
            {% if conf >= 88 %}green
            {% elif conf >= 75 %}yellow
            {% else %}red
            {% endif %}
        
        - entity: sensor.aquarium_ph_test
          name: "  └─ Confidence"
          secondary_info: attribute
          attribute: confidence
          icon: mdi:gauge
    
    # Safety Assessment
    - type: custom:mushroom-template-card
      primary: "Water Safety Assessment"
      secondary: >
        {% set amm = states('sensor.aquarium_ammonia_test')|float(0) %}
        {% set nit = states('sensor.aquarium_nitrite_test')|float(0) %}
        {% set nat = states('sensor.aquarium_nitrate_test')|float(0) %}
        {% set ph = states('sensor.aquarium_ph_test')|float(7.0) %}
        
        {% if amm > 0.5 or nit > 0.5 %}
        🚨 DANGER - Immediate water change needed!
        {% elif amm > 0.25 or nit > 0.25 %}
        ⚠️ WARNING - Water change recommended
        {% elif nat > 80 %}
        🟡 CAUTION - Nitrate high, water change soon
        {% elif ph < 6.0 or ph > 8.5 %}
        ⚠️ WARNING - pH out of safe range
        {% else %}
        ✅ SAFE - All parameters within range
        {% endif %}
      icon: >
        {% set amm = states('sensor.aquarium_ammonia_test')|float(0) %}
        {% set nit = states('sensor.aquarium_nitrite_test')|float(0) %}
        {% if amm > 0.5 or nit > 0.5 %}mdi:alert-octagon
        {% elif amm > 0.25 or nit > 0.25 %}mdi:alert
        {% else %}mdi:shield-check
        {% endif %}
      icon_color: >
        {% set amm = states('sensor.aquarium_ammonia_test')|float(0) %}
        {% set nit = states('sensor.aquarium_nitrite_test')|float(0) %}
        {% if amm > 0.5 or nit > 0.5 %}red
        {% elif amm > 0.25 or nit > 0.25 %}orange
        {% else %}green
        {% endif %}
      card_mod:
        style: |
          :host {
            {% set amm = states('sensor.aquarium_ammonia_test')|float(0) %}
            {% set nit = states('sensor.aquarium_nitrite_test')|float(0) %}
            {% if amm > 0.5 or nit > 0.5 %}
            --card-mod-icon: mdi:alert-octagon;
            animation: pulse 2s infinite;
            {% endif %}
          }
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
          }
    
    # Test History Chart
    - type: custom:apexcharts-card
      header:
        show: true
        title: 📈 30-Day Test History
      graph_span: 30d
      apex_config:
        chart:
          height: 300
        yaxis:
          - id: toxic
            title:
              text: "Ammonia/Nitrite (ppm)"
            min: 0
            max: 2
          - id: nitrate
            opposite: true
            title:
              text: "Nitrate (ppm)"
            min: 0
          - id: ph
            opposite: true
            title:
              text: "pH"
            min: 6
            max: 9
        annotations:
          yaxis:
            - y: 0.25
              y2: 2
              yAxisIndex: 0
              fillColor: '#fee2e2'
              opacity: 0.3
              label:
                text: 'Danger Zone'
      series:
        - entity: sensor.aquarium_ammonia_test
          name: Ammonia
          yaxis_id: toxic
          color: '#ef4444'
          stroke_width: 3
          show:
            legend_value: false
        
        - entity: sensor.aquarium_nitrite_test
          name: Nitrite
          yaxis_id: toxic
          color: '#f59e0b'
          stroke_width: 3
          show:
            legend_value: false
        
        - entity: sensor.aquarium_nitrate_test
          name: Nitrate
          yaxis_id: nitrate
          color: '#10b981'
          stroke_width: 2
          show:
            legend_value: false
        
        - entity: sensor.aquarium_ph_test
          name: pH
          yaxis_id: ph
          color: '#3b82f6'
          stroke_width: 2
          show:
            legend_value: false
    
    # Testing Guidelines
    - type: markdown
      title: 📚 NT Labs Testing Guide
      content: |
        ### Freshwater Test Schedule
        
        **New Tank (0-6 weeks):**
        - Daily ammonia & nitrite tests
        - Every 3 days: nitrate & pH
        
        **Established Tank:**
        - Weekly: All parameters
        - After water change: Verify parameters
        - After adding fish: Monitor for 1 week
        
        **Safe Ranges (Freshwater):**
        - Ammonia: 0 ppm (any level is toxic!)
        - Nitrite: 0 ppm (any level is toxic!)
        - Nitrate: <20 ppm (ideal), <40 ppm (acceptable)
        - pH: 6.5-7.5 (tropical), species-dependent
        
        **Danger Signs:**
        - 🔴 Ammonia >0.25 ppm = Emergency water change
        - 🔴 Nitrite >0.25 ppm = Emergency water change
        - 🟡 Nitrate >80 ppm = Large water change needed
        - 🟡 pH <6.0 or >8.5 = Investigate & correct
    
    # Analysis Details
    - type: entities
      title: 🔬 Analysis Details
      entities:
        - entity: sensor.water_test_confidence
          name: Overall Confidence
          icon: mdi:gauge
        
        - type: custom:mushroom-template-card
          primary: "Processing"
          secondary: >
            {{ state_attr('sensor.water_test_confidence', 'processing_time_seconds') }}s
            ({{ state_attr('sensor.water_test_confidence', 'processor') }})
          icon: mdi:speedometer
          icon_color: green
        
        - type: custom:mushroom-template-card
          primary: "Last Analysis"
          secondary: >
            {% set time = state_attr('sensor.water_test_confidence', 'timestamp') %}
            {% if time %}
              {{ as_timestamp(time) | timestamp_custom('%A, %B %d at %I:%M %p') }}
            {% else %}
              No tests recorded
            {% endif %}
          icon: mdi:calendar-clock
          icon_color: blue
    
    # Manual Entry Override (for drop tests)
    - type: entities
      title: ✍️ Manual Entry (KH/GH Drop Tests)
      entities:
        - type: custom:mushroom-template-card
          primary: "Manual Test Entry"
          secondary: "For KH/GH drop-counting tests"
          icon: mdi:pencil
          icon_color: grey
        
        - entity: input_number.manual_kh_test
          name: KH (dKH)
          icon: mdi:water-plus
        
        - entity: input_number.manual_gh_test
          name: GH (dGH)
          icon: mdi:water-check
        
        - type: button
          name: "Record Manual Tests"
          icon: mdi:content-save
          action_name: SAVE
          tap_action:
            action: call-service
            service: script.record_manual_water_tests

# Add these to configuration.yaml for manual KH/GH
input_number:
  manual_kh_test:
    name: "KH Manual Test Result"
    min: 0
    max: 20
    step: 1
    unit_of_measurement: "dKH"
    icon: mdi:water-plus
  
  manual_gh_test:
    name: "GH Manual Test Result"
    min: 0
    max: 30
    step: 1
    unit_of_measurement: "dGH"
    icon: mdi:water-check

script:
  record_manual_water_tests:
    alias: "Record Manual Water Tests"
    sequence:
      - service: mqtt.publish
        data:
          topic: "aquarium/water_test/kh"
          payload: >
            {
              "value": {{ states('input_number.manual_kh_test') }},
              "unit": "dKH",
              "method": "manual",
              "timestamp": "{{ now().isoformat() }}"
            }
          retain: true
      
      - service: mqtt.publish
        data:
          topic: "aquarium/water_test/gh"
          payload: >
            {
              "value": {{ states('input_number.manual_gh_test') }},
              "unit": "dGH",
              "method": "manual",
              "timestamp": "{{ now().isoformat() }}"
            }
          retain: true
      
      - service: notify.mobile_app_YOUR_PHONE
        data:
          title: "✅ Manual Tests Recorded"
          message: >
            KH: {{ states('input_number.manual_kh_test') }} dKH
            GH: {{ states('input_number.manual_gh_test') }} dGH
```

---

## 📸 Camera Setup Instructions

### Physical Setup:

```
Equipment Needed:
├─ Test tube rack (holds 4-6 tubes)
├─ White background (poster board)
├─ LED light (5000K-6500K, "daylight")
├─ Camera positioned 20-30cm from tubes
└─ Stable mounting (no movement)

Layout:
                Camera
                  ↓
    ┌─────────────────────────┐
    │                         │
    │    LED Light Strip      │
    │         ↓               │
    │   ┌─┐ ┌─┐ ┌─┐ ┌─┐     │
    │   │ │ │ │ │ │ │ │     │
    │   └─┘ └─┘ └─┘ └─┘     │
    │                         │
    │   White Background      │
    │   (Poster Board)        │
    └─────────────────────────┘
```

### Lighting:

```yaml
Recommended:
- LED strip (5000K-6500K)
- Position above tubes
- Diffused (not direct)
- No shadows on tubes

Avoid:
- Yellow incandescent
- Direct sunlight
- Fluorescent (flickers)
- Mixed lighting sources
```

---

## 🎯 Calibration for NT Labs

### Step 1: Create Reference Tests

```python
# Run known tests to calibrate
1. Mix distilled water (known 0 ppm)
2. Take photo
3. Note RGB values
4. Repeat for control solutions
5. Update config.yaml
```

### Step 2: Position Calibration

```bash
# Find tube positions
1. Place tubes in rack
2. Take test photo
3. Open in image editor
4. Note pixel coordinates
5. Update config.yaml test_regions
```

---

## ✅ Installation Checklist

**Hardware:**
- [ ] Camera positioned
- [ ] Test tube rack
- [ ] White background
- [ ] LED lighting (daylight)
- [ ] Stable setup (no wobble)

**Software:**
- [ ] Update config.yaml with NT Labs colors
- [ ] Add liquid test analysis method
- [ ] Add Water Testing dashboard tab (Tab 10)
- [ ] Add manual entry inputs (KH/GH)
- [ ] Restart Home Assistant

**Calibration:**
- [ ] Take reference photos
- [ ] Update tube positions
- [ ] Test with known samples
- [ ] Verify accuracy
- [ ] Adjust colors if needed

---

## 🎉 Summary

**NT Labs Liquid Test System:**

✅ **Dedicated Dashboard Tab** - Tab 10: Water Testing  
✅ **NT Labs Color Charts** - Calibrated for their reagents  
✅ **Liquid Test Analysis** - Optimized for tubes (not strips)  
✅ **Safety Assessment** - Auto-warnings for dangerous levels  
✅ **30-Day History** - Track all parameters over time  
✅ **Manual Entry** - For KH/GH drop tests  
✅ **Testing Guidelines** - Built into dashboard  

**Complete freshwater monitoring with NT Labs tests! 🧪✨**
