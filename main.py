from machine import Pin, PWM
import time
import easings as ea
from RGB import RGB

PWM_FREQ_HZ = 1_000

def sign(x):
    if (x >=0):
        return 1
    else:
        return -1

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
        time.sleep(delayTimeInMilliseconds // 2)

async def PulseOut(pwm, pulseTimeInSeconds):
    grain = 255
    delayTimeInMilliseconds = int(round(pulseTimeInSeconds / grain * 1000, 0));
    for rampIndex in range(grain, 0, -1):
        brightness = int(ea.ease_out_expo(rampIndex/grain) * grain)
        pwm.duty_u16(brightness * brightness)
        time.sleep(delayTimeInMilliseconds)

def TransitionRGB(pwmr, pwmg, pwmb, startColor, endColor, timeInMs, transition_fn):

    ColorToDC = lambda x: x*x

    frames = timeInMs

    redStartingDutyCycle = ColorToDC(startColor.r) * 1000
    redEndingDutyCycle = ColorToDC(endColor.r) * 1000
    redDistance = redEndingDutyCycle - redStartingDutyCycle

    grnStartingDutyCycle = ColorToDC(startColor.g) * 1000
    grnEndingDutyCycle = ColorToDC(endColor.g) * 1000
    grnDistance = grnEndingDutyCycle - grnStartingDutyCycle

    bluStartingDutyCycle = ColorToDC(startColor.b) * 1000
    bluEndingDutyCycle = ColorToDC(endColor.b) * 1000
    bluDistance = bluEndingDutyCycle - bluStartingDutyCycle

    redDutyCycle, grnDutyCycle, bluDutyCycle = (0,0,0)
    for frame in range(1, frames+1):
        scaleFactor = transition_fn(frame/frames)
        redDutyCycle = redStartingDutyCycle + int(redDistance * scaleFactor)
        bluDutyCycle = bluStartingDutyCycle + int(bluDistance * scaleFactor)
        grnDutyCycle = grnStartingDutyCycle + int(grnDistance * scaleFactor)

        pwmr.duty_u16(redDutyCycle // 1000)
        pwmg.duty_u16(grnDutyCycle // 1000)
        pwmb.duty_u16(bluDutyCycle // 1000)

        time.sleep_us(1000)

def TransitionColors(pwmr, pwmg, pwmb):
    startColor = RGB((0, 0, 0))
    endColor = RGB()
    endColor.randomFromPalette()

    for _ in range(1_000):
        TransitionRGB(pwmr, pwmg, pwmb, startColor, endColor, 3_500, ea.ease_out_sine)
        startColor = RGB((endColor.r, endColor.g, endColor.b))
        endColor.randomFromPalette()
        while (endColor == startColor):
            endColor.randomFromPalette()
    endColor = RGB()
    TransitionRGB(pwmr, pwmg, pwmb, startColor, endColor, 3_000, ea.ease_out_expo)

def breathe(pwmr, pwmg, pwmb, color):
        startColor = RGB((0,0,0))
        endColor = color
        TransitionRGB(pwmr, pwmg, pwmb, startColor, endColor, 2500, ea.ease_inout_cubic)
        time.sleep_ms(500)
        TransitionRGB(pwmr, pwmg, pwmb, endColor, startColor, 3000, ea.ease_out_cubic)
        time.sleep_ms(500)

def blink_led():
    onboardLed = Pin(25, Pin.OUT)
    for _ in range(4):
        onboardLed.toggle()
        time.sleep_ms(125)            

def main():
    blink_led()

    pwmr = InitPwmOnPin(0)
    pwmg = InitPwmOnPin(1)
    pwmb = InitPwmOnPin(2)

    color = RGB()
    color.dump()
    color.randomFromPalette()
    color.dump()
    color.darken()
    color.multiply(.1)
    for _ in range(500):
        breathe(pwmr, pwmg, pwmb, color)
        color.randomFromPalette()
        color.darken()
        color.multiply(.2)
        color.dump()
        print()


    pwmr.deinit
    pwmg.deinit
    pwmb.deinit

    blink_led()

main()