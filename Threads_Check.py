"""
Author : Ariel Shiffer
Program name : threads_check
Description : This program is
checking different situation
and overloading the database with
threading.
Date : 26.1.23
"""

from synchronization import Synchronization
from Writing_Functions import WritingFunctions
import win32process
from win32event import WaitForSingleObject as Join,\
    INFINITE
import logging

FILE_NAME = "Threads_Check.bin"
SIZE = 1000


def check_write_function(s):
    """
    This function overload the database and writes
    to it 150 times.
    :param s: A synchronization object.
    :return: Nothing, just checks the functions,
    if there is an error it will pop up.
    """
    logging.debug('begins check writing')
    for number in range(150):
        assert s.set_value(number, number)


def check_read_function(s):
    """
        This function overload the database and reads
        from it 150 times.
        :param s: A synchronization object.
        :return: Nothing, just checks the functions,
        if there is an error it will pop up.
        """
    logging.debug('begins check writing')
    for number in range(150):
        assert (number == s.get_value(number))


def main():
    """
    checks the reader and the writer methods.
    running them simultaneously
    using win32process.
    return: None
    """
    logging.debug("Begins checking for process:")
    s = Synchronization(WritingFunctions())
    logging.info("checking simple writing")
    p1 = win32process.beginthreadex(None, SIZE,
                                    check_write_function, (s,), 0)[0]
    assert Join(p1, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")

    logging.info("checking read")
    p1 = win32process.beginthreadex(None, SIZE,
                                    check_read_function, (s,), 0)[0]
    assert Join(p1, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")

    logging.info("checking multi reads")
    threads = []
    for i in range(5):
        t = win32process.beginthreadex(None, SIZE,
                                       check_read_function, (s,), 0)[0]
        threads.append(t)
    for i in threads:
        assert Join(i, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")

    logging.info("checking read against writing")
    p1 = win32process.beginthreadex(None, SIZE,
                                    check_read_function, (s,), 0)[0]
    p2 = win32process.beginthreadex(None, SIZE,
                                    check_write_function, (s,), 0)[0]
    assert Join(p1, INFINITE) == 0
    assert Join(p2, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")

    logging.info("checking write against reading")
    p1 = win32process.beginthreadex(None, SIZE,
                                    check_write_function, (s,), 0)[0]
    p2 = win32process.beginthreadex(None, SIZE,
                                    check_read_function, (s,), 0)[0]
    assert Join(p1, INFINITE) == 0
    assert Join(p2, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")

    logging.info("checking load")
    threads = []
    for i in range(15):
        t = win32process.beginthreadex(None, SIZE,
                                       check_read_function, (s,), 0)[0]
        threads.append(t)
    for i in range(5):
        p = win32process.beginthreadex(None, SIZE,
                                       check_write_function, (s,), 0)[0]
        threads.append(p)
    for i in threads:
        assert Join(i, INFINITE) == 0
    logging.info("Check successful")
    logging.debug(f"\n" + "=" * 70 + "\n")

    logging.info("checking if the values stayed the same")
    p = win32process.beginthreadex(None, SIZE,
                                   check_read_function, (s,), 0)[0]
    assert Join(p, INFINITE) == 0
    logging.info("Check successful")


if __name__ == '__main__':
    logging.basicConfig(filename="CheckThread.log",
                        filemode="a", level=logging.DEBUG)
    main()
