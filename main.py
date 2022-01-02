from machine import Pin, PWM
import math
import random
import time
import uasyncio

class RGB:
    r = 0
    g = 0
    b = 0

    def __init__(self, orig=None):
        if orig is None:
            return
        else:
            self.set( orig.r, orig.g, orig.b)

    def randomize(self):
        self.r = random.randrange(255)
        self.g = random.randrange(255)
        self.b = random.randrange(255)

    def set(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def get(self):
        return (self.r, self.g, self.b)

    def dump(self):
        print((self.r, self.g, self.b))

PWM_FREQ_HZ = 1000

# sign = lambda a: (a>0) - (a<0)
# sign = lambda a: 1 - (a <= 0)
def sign(x):
    if (x >=0):
        return 1
    else:
        return -1

def ease_in_expo(x):
    return 0 if x == 0 else math.pow(2, 10 * x - 10)

def ease_out_expo(x):
    return 1 if x == 1 else 1 - math.pow(2, -10 * x)

def Blink(red, green, blue):

    # time.sleep_ms(1000)

    red.duty_u16(0)
    green.duty_u16(0)
    blue.duty_u16(0)
    time.sleep_ms(50)

    red.duty_u16(65535)
    green.duty_u16(65535)
    blue.duty_u16(65535)
    time.sleep_ms(50)

    red.duty_u16(0)
    green.duty_u16(0)
    blue.duty_u16(0)
    
    # time.sleep_ms(1000)

def InitPwmOnPin(pin):
    pwm = PWM(Pin(pin))
    pwm.duty_u16(0)
    pwm.freq(PWM_FREQ_HZ)
    return pwm

async def FadeInAndOut(pwm, timeInSeconds):
    duty = 0
    direction = 1
    delayTimeInMilliseconds = int(round(timeInSeconds / 255 * PWM_FREQ_HZ, 0));
    for _ in range(2 * 256):
        duty += direction
        if duty > 255:
            duty = 255
            direction = -1
        elif duty < 0:
            duty = 0
            direction = 1
        pwm.duty_u16(duty * duty)
        await uasyncio.sleep_ms(delayTimeInMilliseconds // 2)

async def PulseOut(pwm, pulseTimeInSeconds):
    grain = 255
    delayTimeInMilliseconds = int(round(pulseTimeInSeconds / grain * 1000, 0));
    for rampIndex in range(grain, 0, -1):
        brightness = int(ease_out_expo(rampIndex/grain) * grain)
        pwm.duty_u16(brightness * brightness)
        await uasyncio.sleep_ms(delayTimeInMilliseconds)

async def TransitionRGB(pwmr, pwmg, pwmb, startColor, endColor, timeInMs):

    # print()
    # print("From {0} to {1}".format(startColor.get(), endColor.get()))

    ColorToDC = lambda x: x*x

    frames = timeInMs

    redStartingDutyCycle = ColorToDC(startColor.r)
    redEndingDutyCycle = ColorToDC(endColor.r)
    redSteps = redEndingDutyCycle - redStartingDutyCycle
    redStepsPerFrame = int(redSteps/frames)

    grnStartingDutyCycle = ColorToDC(startColor.g)
    grnEndingDutyCycle = ColorToDC(endColor.g)
    grnSteps = grnEndingDutyCycle - grnStartingDutyCycle
    grnStepsPerFrame = int(grnSteps/frames)

    bluStartingDutyCycle = ColorToDC(startColor.b)
    bluEndingDutyCycle = ColorToDC(endColor.b)
    bluSteps = bluEndingDutyCycle - bluStartingDutyCycle
    bluStepsPerFrame = int(bluSteps/frames)

    # print("rsteps: {0}, rstepsPerFrame:{1}".format(redSteps, redStepsPerFrame))
    # print("gsteps: {0}, gstepsPerFrame:{1}".format(grnSteps, grnStepsPerFrame))
    # print("bsteps: {0}, bstepsPerFrame:{1}".format(bluSteps, bluStepsPerFrame))

    redDutyCycle = redStartingDutyCycle
    grnDutyCycle = grnStartingDutyCycle
    bluDutyCycle = bluStartingDutyCycle

    for _ in range(frames):
        redDutyCycle += redStepsPerFrame
        grnDutyCycle += grnStepsPerFrame
        bluDutyCycle += bluStepsPerFrame

        pwmr.duty_u16(redDutyCycle)
        pwmg.duty_u16(grnDutyCycle)
        pwmb.duty_u16(bluDutyCycle)

        time.sleep_us(1000)

    print("actual:{0}, expected:{1}".format((redDutyCycle, grnDutyCycle, bluDutyCycle), 
                                            (redEndingDutyCycle, grnEndingDutyCycle, bluEndingDutyCycle)))

    pwmr.duty_u16(redEndingDutyCycle)
    pwmg.duty_u16(grnEndingDutyCycle)
    pwmb.duty_u16(bluEndingDutyCycle)

async def main():
    onboardLed = Pin(25, Pin.OUT)
    for _ in range(4):
        onboardLed.toggle()
        time.sleep_ms(125)

    red = InitPwmOnPin(0)
    green = InitPwmOnPin(1)
    blue = InitPwmOnPin(2)

    startColor = RGB()
    endColor = RGB()
    endColor.set(128, 128, 128)

    for _ in range(1000):
        await uasyncio.create_task(
            TransitionRGB(red, green, blue, startColor, endColor, 5_000))
        startColor = RGB(endColor)
        endColor.randomize()

    endColor = RGB()
    await uasyncio.create_task(
        TransitionRGB(red, green, blue, startColor, endColor, 5_000))

    red.deinit
    green.deinit
    blue.deinit

    for _ in range(8):
        onboardLed.toggle()
        time.sleep_ms(125)

uasyncio.run(main())