from .CLI import CLI
import sys
import fire


def main() -> None:
    try:
        fire.Fire(CLI)
    except Exception as e:
        print(f"Erreur : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
