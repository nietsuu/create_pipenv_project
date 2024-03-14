if __name__ == "__main__":
    import sys
    from PROJECT_NAME import main
    from PROJECT_NAME.entry_point import main_wrapper

    try:
        sys.exit(main_wrapper(main))
    except KeyboardInterrupt:
        sys.exit(0)
