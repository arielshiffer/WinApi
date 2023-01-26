"""
Author : Ariel Shiffer
Program name : Writing_Functions
Description : This program opens a file
and puts information from the database
dictionary into it in pickle encryption and
also gets information about the
database dictionary from the file.
Date : 26.1.23
"""
import logging
from pickle import loads, dumps
import win32file
from DataBase import *

FILE_NAME = "Writing_Functions.bin"


class WritingFunctions(Database):
    def __init__(self):
        """
        This function creates the initial file and puts
        all the information from the data base into it.
        """
        super().__init__()

    def set_value(self, key, value):
        """
        This function reads from the file and then
        updates.
        the values of the dictionary, then writes to the
        file again.
        :param key: The name of the key we want to add to
        the dictionary. String.
        :param value: The value we want to put to the
        certain key.String.
        :return: If the key and value added successfully
        return True else return False.
        """
        try:
            self.read_file()
            result = super().set_value(key, value)
            self.write_file()
            return result
        except OSError as err:
            logging.error(f"Data to File: Got Error {err}"
                          f" for the file {FILE_NAME}, returning False for failure")
            return False

    def get_value(self, key):
        """
        This function reads from the file to update
        the.
        database dict then gets the value of the
        inserted key from the dict.
        :param key: The key we want to get the
        value of from the dict.
        :return: The value of the inserted key. String.
        """
        self.read_file()
        return super().get_value(key)

    def delete_value(self, key):
        """
        This function reads the file to update the
        dictionary.
        then gets the value from the inserted key and
        deletes
        the key and value from the data base dict.
        :param key: The key we want to get the value of and
        delete from the dict. String.
        :return: The value from the key we wanted
        to delete. String.
        """
        self.read_file()
        result = super().delete_value(key)
        self.write_file()
        return result

    def read_file(self):
        """
        :return:
        """
        file = win32file.CreateFileW(FILE_NAME,
                                     win32file.GENERIC_READ,
                                     win32file.FILE_SHARE_READ,
                                   None, win32file.OPEN_ALWAYS, 0, None)
        logging.debug(f"Data to File: opens file to read {FILE_NAME}")
        try:
            info = win32file.ReadFile(file, 100000000)
            assert info[0] == 0
            self.dictionary = loads(info[1])
        except EOFError:
            self.dictionary = {}
        finally:
            win32file.CloseHandle(file)
            logging.debug(f"Data to File: load data to file {FILE_NAME}")

    def write_file(self):
        """
        :return:
        """
        logging.debug(f"Data to File: opens the file for write {FILE_NAME}")
        file = win32file.CreateFileW(FILE_NAME, win32file.GENERIC_WRITE,
                                     0, None, win32file.CREATE_ALWAYS, 0, None)
        try:
            win32file.WriteFile(file, dumps(self.dictionary))
            logging.debug(f"Data to file: dumps the data to the file {FILE_NAME}")
        finally:
            win32file.CloseHandle(file)


if __name__ == '__main__':
    logging.basicConfig(filename="Data_To_File.log",
                        filemode="a", level=logging.DEBUG)
