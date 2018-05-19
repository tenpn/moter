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

repl_parser = cmd_parsers.add_parser("repl", help="continually run commands")

options = mote_parser.parse_args()

def off(args):
    if args.targets == "pixel":
        m.set_pixel(args.channel, args.led, 0, 0, 0)
    elif args.targets == "channel":
        for p in range(16):
            m.set_pixel(args.channel, p, 0, 0 ,0)
    elif args.targets == "all":
        m.clear()

def on(args):
    if args.targets == "pixel":
        m.set_pixel(args.channel, args.led, args.color[0], args.color[1], args.color[2])
    elif args.targets == "channel":
        for p in range(16):
            m.set_pixel(args.channel, p, args.color[0], args.color[1], args.color[2])
    elif args.targets == "all":
        for c in range(1, 5):
            for p in range(16):
                m.set_pixel(c, p, args.color[0], args.color[1], args.color[2])

def run(args):
    if args.cmd == "off":
        off(args)
    elif args.cmd == "on":
        on(args)
    m.show()
                
if options.cmd == "repl":
    while True:
        try:
            text = raw_input(">")
            cmd = mote_parser.parse_args(text.split())
            run(cmd)
        except SystemExit as e:
            print e
else:
    run(options)
