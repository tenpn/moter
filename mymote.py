from mote import Mote
import time
import random

m = Mote()
m.configure_channel(1, 16, True)
m.configure_channel(2, 16, False)
m.configure_channel(3, 16, False)
m.configure_channel(4, 16, False)

m.clear()

last_r = 0
last_g = 0
last_b = 0

while True:
    for c in range(1, 5):
        for p in range(16):
            while True:
                r = random.choice([0, 127, 255])
                g = random.choice([0, 127, 255])
                b = random.choice([0, 127, 255])
                if (r != g or r != b or g != b) and (r != last_r and b != last_b and g != last_g):
                    break

            m.set_pixel(c, p, r, g, b)
            last_r = r
            last_g = g
            last_b = b
            # clear next pixel ready for next loop
            if p < 15:
                m.set_pixel(c, p+1, 0, 0, 0)
            m.show()
            time.sleep(0.05)
            pass
        time.sleep(0.05)
    m.show()
    time.sleep(0.05)
