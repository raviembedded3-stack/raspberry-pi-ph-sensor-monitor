# 🧪 Raspberry Pi pH Sensor Monitor

Monitor water quality in real-time using pH sensor,
ADS1115 ADC and 16x2 I2C LCD Display!

## 📋 Description
This project reads analog pH sensor values using
ADS1115 ADC connected to Raspberry Pi and displays
pH value and water quality status on 16x2 I2C LCD.

## ✨ Features
- 🧪 Real-time pH value monitoring
- 🟢 NEUTRAL  → pH 6.5 to 7.5
- 🔴 ACIDIC   → pH below 6.5
- 🔵 ALKALINE → pH above 7.5
- 📟 Live LCD display with status
- ⚡ Reads every 1 second

## 🛠️ Hardware Required
- Raspberry Pi
- Analog pH Sensor
- ADS1115 ADC Module
- 16x2 I2C LCD Display (PCF8574)
- Jumper Wires

## 📌 Connection Diagram
### ADS1115 to Raspberry Pi
| ADS1115 Pin | Raspberry Pi |
|-------------|-------------|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO 2 (Pin 3) |
| SCL | GPIO 3 (Pin 5) |
| A0 | pH Sensor Output |

### LCD to Raspberry Pi
| LCD Pin | Raspberry Pi |
|---------|-------------|
| VCC | 5V |
| GND | GND |
| SDA | GPIO 2 (Pin 3) |
| SCL | GPIO 3 (Pin 5) |

## 🔰 pH Status Zones
| Zone | pH Range | Status |
|------|----------|--------|
| 🔴 Acidic | Below 6.5 | ⚠️ Warning |
| 🟢 Neutral | 6.5 to 7.5 | ✅ Good |
| 🔵 Alkaline | Above 7.5 | ⚠️ Warning |

## 💻 Libraries Required
```bash
