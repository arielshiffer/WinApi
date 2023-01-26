"""
Author : Ariel Shiffer
Program name : synchronazation
Description : This program is dealing
with the sync of the threads/processes
by using locks.
Date : 26.1.23
"""
import logging
from win32event import CreateSemaphore,\
    CreateMutex, ReleaseSemaphore, ReleaseMutex,\
    WaitForSingleObject, INFINITE

NAME_READ = "read"
NAME_WRITE = "write"


class Synchronization:
    def __init__(self, data_base):
        """
        This function gets the mode of the lock,
        if True -> threads else -> multiprocessing
        then build the matching set of locks.
        :param data_base: A database object.
        """
        super().__init__()
        self.dictionary = data_base
        self.write = CreateMutex(None, False, NAME_WRITE)
        self.read = CreateSemaphore(None, 10, 10, NAME_READ)

    def set_value(self, key, value):
        """
        This function gets the write lock and all the
        reading locks, then updates the dictionary then
        releasing all the locks.
        :param key: The name of key we want to insert.
        String.
        :param value: The value we want to insert to the key.
        String.
        :return: If the key and value added
        successfully -> True if not -> False.
        """
        WaitForSingleObject(self.write, INFINITE)
        for i in range(10):
            WaitForSingleObject(self.read, INFINITE)
        logging.debug("Sync_DataBase: self write - acquired")
        result = self.dictionary.set_value(key, value)
        ReleaseSemaphore(self.read, 10)
        ReleaseMutex(self.write)
        logging.debug("Sync_DataBase: self write - released")
        return result

    def get_value(self, key):
        """
        This function gets one reading lock, then
        gets the value from the certain key then
        release the lock.
        :param key: The key we want to get the value of.
        String.
        :return: The value of the certain key. String.
        """
        WaitForSingleObject(self.read, INFINITE)
        logging.debug("Sync_DataBase:  self read - acquired")
        result = self.dictionary.get_value(key)
        ReleaseSemaphore(self.read, 1)
        logging.debug("Sync_DataBase:  self read - released")
        return result

    def delete_value(self, key):
        """
        This function gets the write lock and all the
        reading locks, then deletes the key and gets its
        value then release all the locks.
        :param key: The certain key we want to get the
        value of and then delete. String.
        :return: The value of the inserted key. String.
        """
        WaitForSingleObject(self.read, INFINITE)
        logging.debug("Sync_DataBase: self write - acquired")
        self.dictionary.delete_value(key)
        ReleaseMutex(self.write)
        logging.debug("Sync_DataBase: self write - released")

    def __str__(self):
        """
        This function gets a reading lock then gets a
        description of the status of the database dict,
        then releases the lock.
        :return: The status of the database dict.
        String.
        """
        return f'The dictionary: {self.dictionary}'


if __name__ == '__main__':
    logging.basicConfig(filename="synchronization.log",
                        filemode="a", level=logging.DEBUG)
