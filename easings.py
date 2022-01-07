import math

def ease_out_quad(x):
    return 1 - (1 - x) * (1 - x)

def ease_out_cubic(x):
    return 1 - pow(1 - x, 3)

def ease_inout_quint(x):
    return 16 * math.pow(x, 5) if x < 0.5 else 1 - math.pow(-2 * x + 2, 5) / 2

def ease_inout_cubic(x):
    return 4 * x * x * x  if x < 0.5  else 1 - pow(-2 * x + 2, 3) / 2

def ease_in_expo(x):
    return 0 if x == 0 else math.pow(2, 10 * x - 10)

def ease_out_expo(x):
    return 1 if x == 1 else 1 - math.pow(2, -10 * x)

def ease_inout_expo(x):
    if (x == 0):
        return 0
    if (x == 1):
        return 1
    if (x < 0.5):
        return pow(2, 20 * x - 10) / 2
    else:
        return (2 - pow(2, -20 * x + 10)) / 2

def ease_in_sine(x):
      return math.sin((x * math.pi) / 2)

def ease_inout_sine(x):
    return -(math.cos(math.pi * x) - 1) / 2

def ease_out_sine(x):
    return math.sin((x * math.pi) / 2)    

def ease_linear(x): return x