import argparse
import scripts.strategyInvoker

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Personal Finance Explorer",
        description="Visually explore, query, and drill-down personal financial portfolios",
    )

    parser.add_argument(
        "--seed",
        help="Seed simulations",
        action="store_const",
        dest="simulation_seed",
        const=True,
    )
    parser.add_argument(
        "-sim",
        "--simulations",
        help="Run all simulations",
        action="store_const",
        const=True,
    )
    args = parser.parse_args()
    print(args)
    if args.simulation_seed:
        scripts.strategyInvoker.seed()
    if args.simulations == True:
        scripts.strategyInvoker.run_all_strategies()
