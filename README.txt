
How to connect up DS18B20 sensors using Raspbian, and optionally
display on a web page, generic 16x2 LCD, or Nokia 5110 LCD display
and wire the pieces up to a breadboard.

Adafruit libraries are used for the LCD displays.

# for gpio (https://github.com/adafruit/Adafruit_Python_GPIO)
git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
cd Adafruit_Python_GPIO
sudo python setup.py install

# for nokia (https://github.com/adafruit/Adafruit_Nokia_LCD)
sudo python setup.py install
also requires python-imaging (apt-get install)
