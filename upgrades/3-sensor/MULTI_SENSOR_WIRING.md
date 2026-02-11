# 🌡️ Multiple DS18B20 Sensors - Wiring Guide

## Overview

You can connect **multiple DS18B20 sensors** on the **same 1-Wire bus** (GPIO 4).
All sensors share the same 3 wires: VCC, GND, and Data.

## Your Setup

1. **Sensor 1:** ATO Reservoir (original)
2. **Sensor 2:** Main Display Tank (new)
3. **Sensor 3:** Sump (new)

---

## Wiring Diagram

```
                    Raspberry Pi
                    GPIO 4 (Pin 7)
                         │
                      4.7kΩ Pull-up
                         │
                    ┌────┴────┐
                    │         │
             ┌──────┴─┐  ┌────┴──────┐  ┌────────┐
             │ Sensor │  │  Sensor   │  │ Sensor │
             │   1    │  │     2     │  │   3    │
             │  ATO   │  │  Display  │  │  Sump  │
             └────────┘  └───────────┘  └────────┘
             
    Yellow   Yellow      Yellow
    (Data)   (Data)      (Data)
       │        │           │
       └────────┴───────────┴──── GPIO 4 (Pin 7)
       
    Red      Red         Red
    (VCC)    (VCC)       (VCC)
       │        │           │
       └────────┴───────────┴──── 3.3V (Pin 1)
       
    Black    Black       Black
    (GND)    (GND)       (GND)
       │        │           │
       └────────┴───────────┴──── GND (Pin 6)
```

## Detailed Wiring

### All Sensors Connect to Same Pins:

| Wire Color | All Sensors Connect To |
|------------|------------------------|
| **Yellow** (Data) | GPIO 4 (Pin 7) |
| **Red** (VCC) | 3.3V (Pin 1) |
| **Black** (GND) | GND (Pin 6) |

### Pull-up Resistor

**One 4.7kΩ resistor** between:
- GPIO 4 (Data line)
- 3.3V (VCC)

**Note:** You only need ONE pull-up resistor for all sensors!

---

## Physical Connection Methods

### Method 1: Terminal Block (Recommended)

Use a small terminal block to connect multiple wires:

```
Terminal Block on Breadboard:

[3.3V] ──┬── Red 1
         ├── Red 2
         └── Red 3

[GND]  ──┬── Black 1
         ├── Black 2
         └── Black 3

[GPIO4]──┬── Yellow 1
         ├── Yellow 2
         └── Yellow 3
         └── 4.7kΩ to 3.3V
```

### Method 2: Solder Junction

For permanent installation:
1. Strip all yellow wires
2. Twist together
3. Solder junction
4. Heat shrink
5. Connect to GPIO 4

### Method 3: Breadboard

Perfect for testing:
1. Insert Pi GPIO pins into breadboard
2. Connect all sensors to same rails
3. Easy to add/remove sensors

---

## Finding Sensor IDs

After connecting all sensors:

```bash
# List all detected sensors
ls /sys/bus/w1/devices/28-*

# You should see 3 sensors:
# 28-0123456789ab
# 28-0123456789cd
# 28-0123456789ef
```

### Identify Which is Which

**Method 1: Temperature Difference**
```bash
# Read each sensor
cat /sys/bus/w1/devices/28-0123456789ab/w1_slave
cat /sys/bus/w1/devices/28-0123456789cd/w1_slave
cat /sys/bus/w1/devices/28-0123456789ef/w1_slave

# Touch one sensor with warm finger
# Re-read - the one that changed is the one you touched!
```

**Method 2: One at a Time**
1. Connect only Sensor 1 → note ID
2. Add Sensor 2 → note new ID
3. Add Sensor 3 → note new ID

**Method 3: Label Them**
Use a label maker or masking tape on each sensor wire!

---

## Configuration

### Option 1: Auto-Detection (Recommended)

Edit `config.py`:
```python
AUTO_DETECT_SENSORS = True
```

Script will auto-detect all sensors and assign them alphabetically by ID.
Display order in Home Assistant:
1. First ID = Display Tank
2. Second ID = Sump
3. Third ID = ATO Reservoir

### Option 2: Manual Assignment

Edit `config.py`:
```python
AUTO_DETECT_SENSORS = False

TEMP_SENSOR_DISPLAY_ID = "28-0123456789ab"
TEMP_SENSOR_SUMP_ID = "28-0123456789cd"
TEMP_SENSOR_ATO_ID = "28-0123456789ef"
```

---

## Testing

```bash
# Test all sensors detected
python3 << 'EOF'
import glob

sensors = glob.glob('/sys/bus/w1/devices/28-*')
print(f"Found {len(sensors)} sensors:")

for sensor in sensors:
    sensor_id = sensor.split('/')[-1]
    
    # Read temperature
    with open(f'{sensor}/w1_slave', 'r') as f:
        lines = f.readlines()
        
    if lines[0].strip()[-3:] == 'YES':
        temp_pos = lines[1].find('t=')
        if temp_pos != -1:
            temp = float(lines[1][temp_pos+2:]) / 1000.0
            print(f"  {sensor_id}: {temp:.2f}°C")
    else:
        print(f"  {sensor_id}: Read error")
EOF
```

Expected output:
```
Found 3 sensors:
  28-0123456789ab: 24.56°C
  28-0123456789cd: 24.81°C
  28-0123456789ef: 23.12°C
```

---

## Troubleshooting

### Only 1 or 2 Sensors Detected

**Check:**
1. All yellow wires connected to GPIO 4?
2. All red wires to 3.3V?
3. All black wires to GND?
4. 4.7kΩ pull-up resistor installed?
5. Sensor not damaged?

**Try:**
- Check continuity with multimeter
- Swap sensors to find faulty one
- Ensure good connections (solder if crimped)

### Sensors Show 85°C or -127°C

**85°C = Not initialized**
- Power cycle Pi
- Check pull-up resistor value

**-127°C = Communication error**
- Reduce cable length (< 3m per sensor)
- Use stronger pull-up (2.2kΩ instead of 4.7kΩ)
- Add separate resistor to each sensor

### Readings Fluctuate Wildly

**Solutions:**
1. Use shielded cable for longer runs
2. Keep sensor wires away from power cables
3. Add 0.1µF capacitor across VCC and GND at each sensor
4. Reduce cable length

---

## Cable Length Limits

| Total Cable Length | Pull-up Resistor | Notes |
|--------------------|------------------|-------|
| < 3m total | 4.7kΩ | Standard |
| 3-10m total | 2.2kΩ | Stronger pull-up |
| 10-20m total | 1.5kΩ | Use shielded cable |
| > 20m | Not recommended | Unreliable |

**For your setup:** 
- ATO Reservoir: Short cable (< 1m)
- Display Tank: Medium cable (1-3m)
- Sump: Medium cable (1-3m)
- **Total: ~5m** → Use 4.7kΩ or 2.2kΩ resistor

---

## Power Considerations

Each DS18B20 draws ~1.5mA max.

**3 sensors = 4.5mA** (well within Pi's capability)

Safe to power from Pi's 3.3V pin ✅

---

## Best Practices

✅ **DO:**
- Use waterproof sensors for tank/sump
- Label each sensor cable
- Use terminal blocks for easy maintenance
- Keep cables organized
- Test each sensor before permanent installation

❌ **DON'T:**
- Mix 3.3V and 5V sensors
- Exceed recommended cable lengths
- Run sensor cables parallel to power cables
- Skip the pull-up resistor

---

**Your 3-sensor setup is ready to wire! 🌡️🌡️🌡️**
