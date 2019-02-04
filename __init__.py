#!/usr/bin/env python
# handy little library for interfacing with an 2 line 16 char lcd panel from rpi
# this was modified a bit from the code found here https://github.com/sunfounder/Sunfounder_SuperKit_Python_code_for_RaspberryPi/blob/master/13_lcd1602.py
import RPi.GPIO as GPIO
import time

class lcd1602:

    _lcd_rs = None
    _lcd_e  = None
    _lcd_d4 = None
    _lcd_d5 = None
    _lcd_d6 = None
    _lcd_d7 = None

    _lcd_char = True    # Character mode
    _lcd_cmd = False   # Command mode
    _lcd_chars = 16    # Characters per line (16 max)
    _lcd_line_1 = 0x80 # LCD memory location for 1st line
    _lcd_line_2 = 0xC0 # LCD memory location 2nd line

    # LCD = lcd1602(7, 8, 25, 24, 23, 18)
    def __init__(self, rs_pin, e_pin, d4, d5, d6, d7):
        self._lcd_rs = rs_pin
        self._lcd_e = e_pin
        self._lcd_d4 = d4
        self._lcd_d5 = d5
        self._lcd_d6 = d6
        self._lcd_d7 = d7

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
        GPIO.setup(self._lcd_rs, GPIO.OUT)
        GPIO.setup(self._lcd_e, GPIO.OUT)
        GPIO.setup(self._lcd_d4, GPIO.OUT)
        GPIO.setup(self._lcd_d5, GPIO.OUT)
        GPIO.setup(self._lcd_d6, GPIO.OUT)
        GPIO.setup(self._lcd_d7, GPIO.OUT)

        self.lcd_write_raw(0x33,self._lcd_cmd) # Initialize
        self.lcd_write_raw(0x32,self._lcd_cmd) # Set to 4-bit mode
        self.lcd_write_raw(0x06,self._lcd_cmd) # Cursor move direction
        self.lcd_write_raw(0x0C,self._lcd_cmd) # Turn cursor off
        self.lcd_write_raw(0x28,self._lcd_cmd) # 2 line display
        self.lcd_write_raw(0x01,self._lcd_cmd) # Clear display
        time.sleep(0.0005)     # Delay to allow commands to process

    def __del__(self):
        self.lcd_write_raw(0x01, self._lcd_cmd)
        GPIO.cleanup()

    # I mean technically don't call this unless you know what you're doing
    def _lcd_toggle_enable(self):
        time.sleep(0.0005)
        GPIO.output(self._lcd_e, True)
        time.sleep(0.0005)
        GPIO.output(self._lcd_e, False)
        time.sleep(0.0005)

    def lcd_write_raw(self, bits, mode):
        # High bits
        GPIO.output(self._lcd_rs, mode) # RS

        GPIO.output(self._lcd_d4, False)
        GPIO.output(self._lcd_d5, False)
        GPIO.output(self._lcd_d6, False)
        GPIO.output(self._lcd_d7, False)
        if bits&0x10==0x10:
            GPIO.output(self._lcd_d4, True)
        if bits&0x20==0x20:
            GPIO.output(self._lcd_d5, True)
        if bits&0x40==0x40:
            GPIO.output(self._lcd_d6, True)
        if bits&0x80==0x80:
            GPIO.output(self._lcd_d7, True)

        # Toggle 'Enable' pin
        self._lcd_toggle_enable()

        # Low bits
        GPIO.output(self._lcd_d4, False)
        GPIO.output(self._lcd_d5, False)
        GPIO.output(self._lcd_d6, False)
        GPIO.output(self._lcd_d7, False)
        if bits&0x01==0x01:
            GPIO.output(self._lcd_d4, True)
        if bits&0x02==0x02:
            GPIO.output(self._lcd_d5, True)
        if bits&0x04==0x04:
            GPIO.output(self._lcd_d6, True)
        if bits&0x08==0x08:
            GPIO.output(self._lcd_d7, True)

        self._lcd_toggle_enable()

    def lcd_write(self, message, line=1):
        if line == 1:
            lcd_row = self._lcd_line_1
        else:
            lcd_row = self._lcd_line_2
        message = message.ljust(self._lcd_chars," ")

        self.lcd_write_raw(lcd_row, self._lcd_cmd)

        for i in range(self._lcd_chars):
            self.lcd_write_raw(ord(message[i]),self._lcd_chr)


lcd = lcd1602(7, 8, 25, 24, 23, 18)
print dir(lcd)
lcd.lcd_write("test", 1)
