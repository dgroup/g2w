import argparse  # pragma: no cover
import requests  # pragma: no cover
import os  # pragma: no cover

# @todo #/DEV Fetch users data from worksection in order to get mapping between
#  Gitlab and WS users. It should be a class, which is collection and each
#  element is a user that represents json user from worksection.

from g2w import Push


def main() -> None:  # pragma: no cover
    # @todo #/DEV Delete argument parser from the method below. It was
    #  generated automatically and not helpful.
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
    # @todo #/DEV Choose a simple REST API framework for pure python without
    #  any massive frameworks like django or flask. Add few tests and ensure
    #  that's it easy to test.
    # @todo #/DEV Invoke worksection REST API in order to test the E2E concept
    #  https://realpython.com/api-integration-in-python/
    #  https://worksection.com/faq/api-start.html
    print(os.environ.get("HOME", "/home/username/"))
    # @todo #/DEV Use environments variable for access to particular
    #  Worksection endpoints. It would be easier to config external urls on
    #  container level.
    print(Push().html({"user": "Tom"}))
    users = requests.get(os.environ["WS_USERS_LIST"]).json()
    print(users)


if __name__ == "__main__":  # pragma: no cover
    main()
