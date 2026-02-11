# 📸 Images & Screenshots

This folder contains visual documentation for the ATO Aquarium Monitor project.

## Recommended Images to Add

### Hardware Setup Photos

1. **hardware-setup.jpg**
   - Complete system photo showing Pi, relay, sensors
   - Labeled components
   - Professional quality

2. **wiring-diagram.png**
   - Clear diagram of all connections
   - Color-coded wires
   - Pin labels

3. **ds18b20-installed.jpg**
   - Temperature sensor in aquarium
   - Proper waterproof installation

4. **relay-module.jpg**
   - Close-up of relay wiring
   - IN1 connection visible

### Dashboard Screenshots

5. **dashboard-overview.png**
   - Main overview tab
   - Show live data
   - All charts visible

6. **dashboard-analytics.png**
   - Analytics tab screenshot
   - Historical trends

7. **dashboard-temperature.png**
   - Temperature monitoring tab

8. **mobile-screenshot.png**
   - How dashboard looks on mobile

### Process Photos

9. **installation-steps.jpg**
   - Step-by-step installation photos

10. **calibration-process.jpg**
    - Shows calibration interface

## How to Add Images

### Option 1: GitHub Web Interface

1. Navigate to this folder on GitHub
2. Click "Add file" → "Upload files"
3. Drag & drop your images
4. Commit changes

### Option 2: Git Command Line

```bash
cd /path/to/ato-aquarium-monitor/images

# Add your images
cp ~/Pictures/hardware-setup.jpg .
cp ~/Pictures/dashboard-screenshot.png .

# Commit
git add *.jpg *.png
git commit -m "Add hardware and dashboard images"
git push
```

## Image Guidelines

### File Naming

- Use lowercase
- Hyphen-separated words
- Descriptive names
- Example: `raspberry-pi-wiring.jpg`

### File Formats

- **Photos:** `.jpg` or `.jpeg`
- **Screenshots:** `.png`
- **Diagrams:** `.png` or `.svg`

### File Sizes

- Compress images before uploading
- Target: < 500KB per image
- Use tools like TinyPNG.com

### Quality

- Minimum 1280x720 resolution
- Good lighting
- Clear focus
- Horizontal orientation preferred

## Creating Wiring Diagrams

### Tools

- **Fritzing** - Circuit diagrams
- **Draw.io** - Block diagrams  
- **Inkscape** - Vector graphics

### Example Fritzing Diagram

```
Components needed:
- Raspberry Pi 3 (breadboard view)
- DS18B20 sensor
- 8-ch relay module
- Resistor (4.7kΩ)
- Jumper wires

Connect and export as PNG
```

## README Usage

Once images are added, update main README.md:

```markdown
## Hardware Setup

![Hardware Setup](images/hardware-setup.jpg)

## Dashboard Preview

![Dashboard](images/dashboard-overview.png)

## Wiring Diagram

![Wiring](images/wiring-diagram.png)
```

## Tips

- Take photos BEFORE everything is mounted
- Use macro mode for close-ups
- Natural lighting is best
- Clean up workspace before photos
- Annotate images with labels

---

**After adding images, your repository will look much more professional! 📸✨**
