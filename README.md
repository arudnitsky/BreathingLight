### Breathing Light
I wanted to make a "breathing" light, like the [sleep LED](https://www.youtube.com/watch?v=ZT6siXyIjvQ) on some devices, but with the ability to change color palettes. I also wanted it bright enough to actually give off enough light, but small enough to sit unobtrusively on a shelf.

I had a [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/). I found a short strip of 5050 LEDs similar to [these](https://www.amazon.com/5050-LED-Strip-Waterproof-SUPERNIGHT/dp/B00COE78EQ/) in my junk collection, and 3 IRLZ734N MOSFETs to drive the LEDs. I also wanted to refresh my soldering skills, so I made a breadboard-pluggable switch for a hard reset button out of a piece of Vero board and male headers. I made the cable and cable ends out of male and female headers, hot glue, and some heatshrink tubing. The cable came from an old 40-conductor ribbon cable, and I simply pulled off four conductors. Initially I tried to strip the end with an Exacto knife, but found that my [Klein Tools 11061 wire strippers](https://www.kleintools.com/catalog/combination-cutting-tools/wire-stripper-and-cutter-self-adjusting) cleanly stripped off the insulation on the cable.

I wrote the code in Python, and as you can tell, I'm on the steep upward part of the learning curve. The color palettes I found at [cpt-city](http://soliton.vm.bytemark.co.uk/pub/cpt-city/index.html). The easing code I took from [easings.net](https://easings.net/).

Finally, I designed a circuit board that fit everything inside the jar, but thankfully decided to stop before investing too much more time.

### Lessons Learned:
- For a $4 microcontroller, the [Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) is a powerful embedded device, with a strong ecosystem and [great documentation](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html).
- [MicroPython](https://docs.micropython.org/en/latest/) is a well-supported Python port with a full library that runs on a [huge range of microcontrollers](https://www.micropython.org/download/).
- Using pulse-width modulation to drive LED brightness is a huge pain in the ass. Don't do it. Really. Use [individually addressable LEDs](https://www.youtube.com/watch?v=HO6xQMR8naw) instead.
- Converting between integer 0...65535 pulse-width duty cycle values, float 0.0...1.0 brightness values, and integer 0-255 RGB color values was, well, interesting.
- Playing with embedded code and electronics is a wonderful rabbit hole.


### Media
| | |
|---|---| 
|![alt text](https://github.com/arudnitsky/Pico5050/blob/main/media/2.jpeg)| ![alt text](https://github.com/arudnitsky/Pico5050/blob/main/media/1.jpeg) |
|![alt text](https://github.com/arudnitsky/Pico5050/blob/main/media/3.jpeg)| ![alt text](https://github.com/arudnitsky/Pico5050/blob/main/media/4.jpeg) |
|![alt text](https://github.com/arudnitsky/Pico5050/blob/main/media/5.jpeg)| |

https://user-images.githubusercontent.com/2124863/205462517-ccc45f77-9c2c-4bcf-836d-283cf72ebd0d.mp4

