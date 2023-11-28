import argparse

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

    if args.simulation_seed:
        import scripts.seed

        scripts.seed.seed("./tickers.txt")
    if args.simulations == True:
        import scripts.strategyInvoker

        scripts.strategyInvoker.run_all_strategies()
    else:
        print("No arguments specified. Use `-h` to see supported arguments")
