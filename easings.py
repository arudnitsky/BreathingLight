import math

def ease_inout_quint(x):
    return 16 * math.pow(x, 5) if x < 0.5 else 1 - math.pow(-2 * x + 2, 5) / 2

def ease_in_expo(x):
    return 0 if x == 0 else math.pow(2, 10 * x - 10)

def ease_out_expo(x):
    return 1 if x == 1 else 1 - math.pow(2, -10 * x)
