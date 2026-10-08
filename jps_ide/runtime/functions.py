"""
JPS Script Builtin Functions
Handles built-in functions such as print().
"""

def jps_print(args, output_callback=print):
    formatted_args = []
    for arg in args:
        formatted_args.append(str(arg))
    msg = " ".join(formatted_args)
    output_callback(msg)
    return msg
