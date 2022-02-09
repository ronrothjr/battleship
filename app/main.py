import argparse
from menu import Menu


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
    Menu().display_main_menu()

if __name__ == '__main__':
    main()
