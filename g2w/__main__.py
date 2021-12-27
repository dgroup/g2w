import argparse  # pragma: no cover

from . import BaseClass, base_function  # pragma: no cover


def main() -> None:  # pragma: no cover
    """
    The main function executes on commands:
    `python -m g2w` and `$ g2w `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    parser = argparse.ArgumentParser(
        description="g2w.",
        epilog="Enjoy the g2w functionality!",
    )
    # This is required positional argument
    parser.add_argument(
        "name",
        type=str,
        help="The username",
        default="dgroup",
    )
    # This is optional named argument
    parser.add_argument(
        "-m",
        "--message",
        type=str,
        help="The Message",
        default="Hello",
        required=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Optionally adds verbosity",
    )
    args = parser.parse_args()
    print(f"{args.message} {args.name}!")
    if args.verbose:
        print("Verbose mode is on.")

    # @todo #/DEV Create a REST endpoint that receives the Gitlab push
    #  notification through the web-hook (https://bit.ly/3sGueNt)
    print("Executing main function")
    # @todo #/DEV Choose a simple REST API framework for pure python without any massive
    #  frameworks like django or flask. Add few tests and ensure that's it easy to test.
    base = BaseClass()
    print(base.base_method())
    print(base_function())
    print("End of main function")
    # @todo #/DEV Invoke worksection REST API in order to test the E2E concept
    #  https://realpython.com/api-integration-in-python/
    #  https://worksection.com/faq/api-start.html


if __name__ == "__main__":  # pragma: no cover
    main()
