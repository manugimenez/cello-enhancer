import argparse

def main():
    parser = argparse.ArgumentParser(description="Cello Design Optimizer")
    # parser.add_argument('-x', '--x-center', type=float, required=True)
    # parser.add_argument('-y', '--y-center', type=float, required=True)
    # parser.add_argument('values', type=float, nargs='*')
    parser.add_argument("verilog", help="path to the verilog file describing the circuit")
    parser.add_argument("ucf", help="path to the UCF file listing parts available")
    parser.add_argument("n", help="max number of components that can be modified during optimization")
    args = parser.parse_args()
    # x(args.x_center, args.y_center, args.values)


if __name__ == '__main__':
    main()