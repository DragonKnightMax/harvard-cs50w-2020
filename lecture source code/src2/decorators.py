def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done running the function.")
    return wrapper


@announce
def hello():
    print("Hello, world!")

hello()
