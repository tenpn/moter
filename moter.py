from mote import Mote
import argparse

m = Mote()
m.configure_channel(1, 16, True)
m.configure_channel(2, 16, False)
m.configure_channel(3, 16, False)
m.configure_channel(4, 16, False)

def add_targeting(parent):
    targeting_parsers = parent.add_subparsers(help="led targeting", dest="targets")
    
    all_parser = targeting_parsers.add_parser('all', help="target every led")
    
    pixel_parser = targeting_parsers.add_parser('pixel', help="target one pixel")
    pixel_parser.add_argument("channel", type=int)
    pixel_parser.add_argument("led", type=int)
    
    channel_parser = targeting_parsers.add_parser('channel', help="target every led on a channel")
    channel_parser.add_argument("channel", type=int)
    
mote_parser = argparse.ArgumentParser(description='adjust mote sticks via command line')
cmd_parsers = mote_parser.add_subparsers(dest="cmd")

on_parser = cmd_parsers.add_parser("on", help="turn on leds")
add_targeting(on_parser)
on_parser.add_argument("color", nargs=3, type=int, help="takes three numbers 0-255 for RGB", default=[255, 255, 255])

off_parser = cmd_parsers.add_parser("off", help="turn off leds")
add_targeting(off_parser)

options = mote_parser.parse_args()

def off():
    if options.targets == "pixel":
        m.set_pixel(options.channel, options.led, 0, 0, 0)
    elif options.targets == "channel":
        for p in range(16):
            m.set_pixel(options.channel, p, 0, 0 ,0)
    elif options.targets == "all":
        m.clear()

def on():
    if options.targets == "pixel":
        m.set_pixel(options.channel, options.led, options.color[0], options.color[1], options.color[2])
    elif options.targets == "channel":
        for p in range(16):
            m.set_pixel(options.channel, p, options.color[0], options.color[1], options.color[2])
    elif options.targets == "all":
        for c in range(1, 5):
            for p in range(16):
                m.set_pixel(c, p, options.color[0], options.color[1], options.color[2])

if options.cmd == "repl":
    pass
else:
    if options.cmd == "off":
        off()
    elif options.cmd == "on":
        on()
    m.show()
