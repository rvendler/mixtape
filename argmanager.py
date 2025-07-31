import argparse
import sys
from typing import Any, Optional, Type # Import Type for type hinting cls

class ArgManager:
    """
    Manages command-line arguments parsed by argparse.

    This class uses class methods and variables to provide a single point
    of access to parsed command-line arguments throughout an application.
    It needs to be initialized once with the results from ArgumentParser.parse_args().
    """
    _args: Optional[argparse.Namespace] = None
    _initialized: bool = False

    @classmethod
    def init(cls: Type['ArgManager'], parsed_args: argparse.Namespace) -> None:
        """
        Initializes the ArgManager with parsed arguments.

        This method should be called once, typically at the start of the
        application after parsing arguments with argparse.

        Args:
            parsed_args: The Namespace object returned by parser.parse_args().

        Raises:
            RuntimeError: If the ArgManager is already initialized.
            TypeError: If parsed_args is not an argparse.Namespace instance.
        """
        if cls._initialized:
            # You might want to log a warning instead, or allow re-initialization
            # depending on your specific needs. Raising an error enforces single init.
            raise RuntimeError("ArgManager has already been initialized.")

        if not isinstance(parsed_args, argparse.Namespace):
            raise TypeError("parsed_args must be an instance of argparse.Namespace")

        cls._args = parsed_args
        cls._initialized = True
        print("ArgManager initialized.", file=sys.stderr) # Optional: for debugging

    @classmethod
    def get_arg(cls: Type['ArgManager'], arg_name: str) -> Any:
        """
        Retrieves the value of a specific command-line argument.

        Args:
            arg_name: The name of the argument (as defined in argparse,
                      e.g., 'input_file' for parser.add_argument('--input-file', ...)).

        Returns:
            The value of the requested argument.

        Raises:
            RuntimeError: If the ArgManager has not been initialized via init().
            AttributeError: If the requested argument name does not exist in the
                           parsed arguments.
        """
        if not cls._initialized or cls._args is None:
            raise RuntimeError("ArgManager has not been initialized. Call init() first.")

        if hasattr(cls._args, arg_name):
            return getattr(cls._args, arg_name)
        else:
            return None
#            raise AttributeError(f"Argument '{arg_name}' not found in parsed arguments.")

    @classmethod
    def is_initialized(cls: Type['ArgManager']) -> bool:
        """Checks if the ArgManager has been initialized."""
        return cls._initialized

    @classmethod
    def get_namespace(cls: Type['ArgManager']) -> argparse.Namespace:
        """
        Returns the entire Namespace object containing all arguments.

        Use this if you need access to the whole collection of arguments.

        Returns:
            The argparse.Namespace object stored during initialization.

        Raises:
            RuntimeError: If the ArgManager has not been initialized via init().
        """
        if not cls._initialized or cls._args is None:
             raise RuntimeError("ArgManager has not been initialized. Call init() first.")
        return cls._args

# --- Example Usage ---

# Assume the above class is saved as 'arg_manager.py'

# main_script.py
if __name__ == "__main__":
    # 1. Setup the Argument Parser
    parser = argparse.ArgumentParser(
        description="A script demonstrating the ArgManager class."
    )
    parser.add_argument(
        "-i", "--input-file",
        required=True,
        help="Path to the input data file."
    )
    parser.add_argument(
        "-o", "--output-file",
        default="output.txt",
        help="Path where results should be saved (default: output.txt)."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true", # Stores True if flag is present, False otherwise
        help="Enable verbose output."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="A threshold value for processing (default: 0.5)."
    )

    # 2. Parse the arguments
    # parse_args() will use sys.argv[1:] by default
    args = parser.parse_args()

    # 3. Initialize the ArgManager *ONCE*
    try:
        ArgManager.init(args)
    except (RuntimeError, TypeError) as e:
        print(f"Failed to initialize ArgManager: {e}")
        sys.exit(1) # Exit if initialization fails

    # 4. Now call functions that rely on the arguments
    print("\n--- Calling process_data ---")
    process_data()

    print("\n--- Calling summarize_results ---")
    summarize_results()

    print("\n--- Accessing another arg directly in main ---")
    try:
        thresh = ArgManager.get_arg('threshold')
        print(f"Threshold value: {thresh}")
    except (AttributeError, RuntimeError) as e:
         print(f"Error accessing threshold: {e}")

    print("\nScript finished.")