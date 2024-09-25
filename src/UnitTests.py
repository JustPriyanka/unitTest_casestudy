import unittest
import wrapper
import HashHelper
import glob

class HashLibraryTests(unittest.TestCase):

    def setUp(self):
        """
        This function runs before every test to initialize the library.
        Ensures that hashInit is called first.
        """
        print("\nInitializing library with hashInit")
        self.lib = wrapper.loadHashLibrary("../extLib/libhash.so")
        returnCode = wrapper.hashInit(self.lib)
        if returnCode != 0:
            raise Exception(f"hashInit failed with return code: {returnCode}")

    def tearDown(self):
        """
        This function runs after every test to terminate the library.
        Ensures that hashTerminate is called last.
        """
        print("\nTerminating library with hashTerminate")
        returnCode = wrapper.hashTerminate(self.lib)
        if returnCode != 0:
            print(f"hashTerminate failed with return code: {returnCode}")

    def test_hash_directory(self):
        """
        Test for the hashDirectory function with a valid directory path.
        """
        print("Running test for hashDirectory")
        directory_path = "."
        print("List of files to be hashed....")
        print(glob.glob(directory_path+"/*.*"))
        returnCode, ID = wrapper.hashDirectory(self.lib, directory_path)
        if returnCode == 0:
            ret = HashHelper.waitforHashDirectory(self.lib, ID)
            if (ret):
                HashHelper.readhashLog(self.lib)
                wrapper.hashStop(self.lib, ID)
        self.assertEqual(returnCode, 0, f"hashDirectory was successful with return code: {returnCode}")


    def test_hash_directory_external_path_failure(self):
        """
        Failure test for the hashDirectory function with a valid external directory path e.g. /home/arin/PycharmProjects/autoTestHid/testfiels but does not work as expected
        """
        print("Running test for hashDirectory")
        directory_path = "/home/arin/PycharmProjects/autoTestHid/testfiels"
        print("List of files to be hashed....")
        print(glob.glob(directory_path+"/*.*"))
        returnCode, ID = wrapper.hashDirectory(self.lib, directory_path)
        if returnCode == 0:
            ret = HashHelper.waitforHashDirectory(self.lib, ID)
            if (ret):
                 self.assertEqual("initrd.img" in HashHelper.returnhashLogLine(self.lib), True, "hashDirectory was failure with a pre-defined value: initrd.img")
                 wrapper.hashStop(self.lib, ID)

    def test_hash_directory_incorrect_external_path_failure(self):
            """
            Failure test for the hashDirectory function with an incorrect external directory path e.g. /home/arin/PycharmProjects/incorrect/path but does not work as expected
            """
            print("Running test for hashDirectory")
            directory_path = "/home/arin/PycharmProjects/incorrect/path"
            print("List of files to be hashed....")
            print(glob.glob(directory_path + "/*.*"))
            returnCode, ID = wrapper.hashDirectory(self.lib, directory_path)
            if returnCode == 0:
                ret = HashHelper.waitforHashDirectory(self.lib, ID)
                if (ret):
                    self.assertEqual("initrd.img" in HashHelper.returnhashLogLine(self.lib), True,
                                     "hashDirectory was failure with a pre-defined value: initrd.img")
                    wrapper.hashStop(self.lib, ID)


    def test_hash_directory_src_path_failure(self):
        """
        Failure test for the hashDirectory function with a directory path which is under the current directory path e.g. ../testfiels but does not work as expected
        """
        print("Running test for hashDirectory")
        directory_path = "../testfiels"
        print("List of files to be hashed....")
        print(glob.glob(directory_path+"/*.*"))
        returnCode, ID = wrapper.hashDirectory(self.lib, directory_path)
        if returnCode == 0:
            ret = HashHelper.waitforHashDirectory(self.lib, ID)
            if (ret):
                 self.assertEqual("mysqld_multi.server" in HashHelper.returnhashLogLine(self.lib) or "mysql.server" in HashHelper.returnhashLogLine(self.lib),
                                  False, "hashDirectory was failure: did not read and hash the correct file")
                 wrapper.hashStop(self.lib, ID)

    def test_hash_stop(self):
        """
        Test for stopping an operation using a valid operation ID.
        """
        print("Running test for hashStop...")
        directory_path = "."
        returnCode, opID = wrapper.hashDirectory(self.lib, directory_path)
        if returnCode == 0:
            HashHelper.waitforHashDirectory(self.lib, opID)
            # Simulate stopping the operation
            stopReturnCode = wrapper.hashStop(self.lib, opID)
            self.assertEqual(stopReturnCode, 0, f"hashStop failed with return code: {stopReturnCode}")
        else:
            self.fail(f"hashDirectory failed to start operation. Return code: {returnCode}")

    def test_hash_read_next_log_line(self):
        """
        Test for reading the next log line, ensuring the log is not empty.
        """
        print("Running test for hashReadNextLogLine...")
        directory_path = "."
        returnCode, opID = wrapper.hashDirectory(self.lib, directory_path)
        if returnCode == 0:
            HashHelper.waitforHashDirectory(self.lib, opID)
            readNextLineReturnCode, logLine = wrapper.hashReadNextLogLine(self.lib)
            if readNextLineReturnCode == 4:
                print("Log is empty, skipping further tests for log reading.")
            else:
                self.assertEqual(readNextLineReturnCode, 0,
                                 f"hashReadNextLogLine failed with return code: {readNextLineReturnCode}")
                print(f"Log Line: {logLine}")
            wrapper.hashStop(self.lib, opID)

    def test_hash_status(self):
        """
        Test for checking the status of an ongoing operation.
        """
        print("Running test for hashStatus...")
        directory_path = "."
        returnCode, opID = wrapper.hashDirectory(self.lib, directory_path)
        if returnCode == 0:
            HashHelper.waitforHashDirectory(self.lib, opID)
            # Check the status of the operation
            statusReturnCode, opRunning = wrapper.hashStatus(self.lib, opID)
            self.assertEqual(statusReturnCode, 0, f"hashStatus failed with return code: {statusReturnCode}")
            print(f"Operation Running: {opRunning}")
        else:
            self.fail(f"hashDirectory failed to start operation. Return code: {returnCode}")


if __name__ == "__main__":
    unittest.main()