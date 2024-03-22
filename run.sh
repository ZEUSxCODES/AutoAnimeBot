import argparse

def main(samedb):
    """Run the bot with the given database configuration."""
    # Your bot code here
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the bot")
    parser.add_argument("--samedb", action="store_true", help="Use the same database")
    args = parser.parse_args()
    main(args.samedb)


python3 bot.py --samedb
