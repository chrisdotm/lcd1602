# lcd1602
Mostly a modified version of [this](https://github.com/sunfounder/Sunfounder_SuperKit_Python_code_for_RaspberryPi/blob/master/13_lcd1602.py)

Turned it into a class you can import from another bit of python code.

Example usage:
`
LCD = lcd1602(7, 8, 25, 24, 23, 18)
LCD.lcd_write("SOME text HERE!") // writes SOME text HERE! on the first line of the LCD
LCD.lcd_write("More text :)", 2) // writes More text :) on the second line of the LCD
LCD.lcd_write("other!!!", 1) // writes other!!! on the first line of the LCD
`
