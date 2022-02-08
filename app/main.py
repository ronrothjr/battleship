import argparse
from battleship import Battleship


def get_args():
    parser = argparse.ArgumentParser(
        description="A File Watcher that executes the specified tests"
        )
    parser.add_argument('--ai_v_ai', action='store', required=False,
                        help='Run an AI versus AI game')
    parser.add_argument('--watch', action='store', required=False,
                        help='Watch as the AI v AI game slowly plays out')
    parser.add_argument('--orientation', action='store', required=False,
                        help='Display grids in landscape or portrait')
    return parser.parse_args()

def main():
    args = get_args()
    Battleship().play_a_game(ai_v_ai=args.ai_v_ai, watch=args.watch, orientation=args.orientation)

if __name__ == '__main__':
    main()