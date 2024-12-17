import unittest

if __name__ == "__main__":
    tests = unittest.TestLoader().discover("./tests/")
    test_runner = unittest.runner.TextTestRunner()
    test_runner.run(tests)