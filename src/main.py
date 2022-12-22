import argparse
import scripts.simulations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Personal Finance Explorer",
        description="Visually explore, query, and drill-down personal financial portfolios",
    )
    parser.add_argument(
        "--simulations",
        help="",
    )
    args = parser.parse_args()
    print(args)
    ...
