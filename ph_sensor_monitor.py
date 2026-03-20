# ============================================
# Project     : pH Sensor Monitor
#               with I2C LCD Display
# Author      : C. P. Ravi
# Company     : Aislyn Technologies Pvt. Ltd.
# Hardware    : Raspberry Pi + Analog pH Sensor
#               + ADS1115 ADC + 16x2 I2C LCD
# Description : Reads pH value from analog
#               pH sensor using ADS1115 ADC
#               and displays result on LCD
#               with water quality status
# ============================================

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from RPLCD.i2c import CharLCD

# ── LCD Configuration ─────────────────────
I2C_ADDRESS = 0x27
I2C_PORT    = 1
LCD_COLS    = 16
LCD_ROWS    = 2

# ── pH Calibration Values ─────────────────
# Calibrate these values with your sensor!
PH_OFFSET   = 0.00   # Adjust if pH reading is off
VOLTAGE_REF = 4.096  # ADS1115 reference voltage

# ── pH Zones ──────────────────────────────
PH_ACIDIC   = 6.5    # Below 6.5 = Acidic
PH_NEUTRAL  = 7.5    # 6.5 to 7.5 = Neutral
                     # Above 7.5 = Alkaline


# ── Setup ─────────────────────────────────

def setup_adc():
    """Setup ADS1115 ADC for pH sensor reading."""
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    channel = AnalogIn(ads, ADS.P0)  # A0 pin
    return channel


def setup_lcd():
    """Initialise and return the LCD object."""
    lcd = CharLCD(
        i2c_expander='PCF8574',
        address=I2C_ADDRESS,
        port=I2C_PORT,
        cols=LCD_COLS,
        rows=LCD_ROWS,
        dotsize=8
    )
    lcd.clear()
    return lcd


# ── pH Reading Functions ──────────────────

def read_voltage(channel):
    """Read voltage from ADS1115 channel."""
    return channel.voltage


def voltage_to_ph(voltage):
    """
    Convert voltage to pH value.
    Formula based on standard pH sensor calibration.
    pH 7 = 2.5V (midpoint)
    Each pH unit = ~0.18V change
    """
    ph = 7 + ((2.5 - voltage) / 0.18)
    ph = ph + PH_OFFSET
    ph = round(ph, 2)
    return ph


def get_ph_status(ph):
    """
    Returns water quality status based on pH value.
    Acidic  → pH below 6.5
    Neutral → pH 6.5 to 7.5
    Alkaline → pH above 7.5
    """
    if ph < PH_ACIDIC:
        return "ACIDIC  ⚠️ "
    elif ph <= PH_NEUTRAL:
        return "NEUTRAL  ✅"
    else:
        return "ALKALINE ⚠️"


# ── LCD Functions ─────────────────────────

def show_welcome(lcd):
    """Display welcome screen."""
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("  pH Monitor    ")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("  Initializing..")
    time.sleep(2)
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("  Sensor Ready! ")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(" C. P. Ravi     ")
    time.sleep(2)
    lcd.clear()


def update_lcd(lcd, ph, status):
    """
    Update LCD with pH value and status.
    Row 0 → pH Value
    Row 1 → Water quality status
    """
    line1 = f"pH Value: {ph}".ljust(16)
    line2 = status[:16].ljust(16)
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1)
    lcd.cursor_pos = (1, 0)
    lcd.write_string(line2)


def show_goodbye(lcd):
    """Display goodbye screen."""
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("   Goodbye! :)  ")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("  C. P. Ravi    ")
    time.sleep(2)
    lcd.clear()


# ── Main Program ──────────────────────────

def main():
    print("=" * 40)
    print("  pH Sensor Monitor with LCD")
    print("  Author : C. P. Ravi")
    print("  Aislyn Technologies Pvt. Ltd.")
    print("=" * 40)

    # Initialize hardware
    channel = setup_adc()
    lcd = setup_lcd()

    # Show welcome screen
    show_welcome(lcd)

    print("[INFO] Reading pH... Press Ctrl+C to stop.\n")

    try:
        while True:
            # Read voltage from sensor
            voltage = read_voltage(channel)

            # Convert to pH value
            ph = voltage_to_ph(voltage)

            # Get water quality status
            status = get_ph_status(ph)

            # Print to terminal
            print(f"Voltage: {voltage:.3f}V  |  pH: {ph}  |  {status}")

            # Update LCD
            update_lcd(lcd, ph, status)

            # Read every 1 second
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user.")

    finally:
        show_goodbye(lcd)
        lcd.close(clear=True)
        print("[INFO] LCD cleared. Exited cleanly.")


if __name__ == "__main__":
    main()
