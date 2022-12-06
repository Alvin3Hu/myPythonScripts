__version__ = '1.0'

import argparse
import pathlib
import time
from pathlib import *
from re import *


def cli_help() -> argparse.Namespace:
    """
    Parameter description by argparse lib.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=f"To parse the test log from ALPS test bench, and output the report\n"
                    f"| By Alvin \n"
                    f"| Ver {__version__}"
    )
    parser.add_argument('--file',
                        '-f',
                        nargs='+',
                        type=argparse.FileType('r', encoding='UTF-8'),
                        help='test log single file',
                        )
    parser.add_argument('--dir',
                        '-d',
                        type=Path,
                        help='directory including test log files',
                        )
    parser.add_argument('--out_dir',
                        '-o',
                        type=Path,
                        # default='source files directory',
                        metavar='DIR',
                        help='output destination directory',
                        )
    parser.add_argument('--test_item',
                        '-t',
                        default='MaxCodeStep',
                        choices=['MaxCodeStep', 'RX_SystemSNR'],
                        help='select ate tester model\n'
                             'default: MaxCodeStep',
                        )
    parser.add_argument('--device_version',
                        '-dev',
                        default='B1',
                        choices=['B0', 'B1'],
                        help='select device version\n'
                             'default: B1',
                        )
    parser.add_argument("--version",
                        action='version',
                        version=__version__,
                        )
    return parser.parse_args()


def proc_print(state: str = None):
    """
    Print for process
    """

    proc_str = '*' * 20

    if state:
        proc_str += ("{} => {}".format(PurePath(__file__).stem, state))

    print("{:*<100s}".format(proc_str))


class BenchTestData:
    """
    Collect and parse the bench test log for report generation.
    """

    def __init__(self, device_version, test_item, output_dir=None):
        self.__device_version = device_version
        self.__test_item = test_item
        self.__output_dir = ""
        if output_dir:
            self.__output_dir = Path(output_dir).resolve()
            self.__check_output_dir()
        else:
            self.__output_dir = Path.cwd()

        self.__output_file = self.__get_output_file()
        self.__log_file_list = []
        self.__report_database = []

    @property
    def output_file(self) -> pathlib.Path:
        return self.__output_file

    def __check_output_dir(self):
        """
        Check if the output dir is exists and make its parent dir if not exists.
        """
        output_dir = Path(self.__output_dir)

        if output_dir.exists():
            print("WARN: output file '{}' is exists, original file will be overwritten !"
                  .format(output_dir))
        else:
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except FileExistsError:
                pass
            else:
                print("WARN: output dir '{}' not exists and to be created automatically !"
                      .format(output_dir))

    def __get_output_file(self) -> pathlib.Path:
        """
        Generate the output file name refer to time,
        and output path is defined as work dir.
        """
        time_stamp = time.localtime()

        output_name = (("{:0>2}" * 3 + '-' + "{:0>2}" * 3)
                       .format(time_stamp.tm_year % 2000,
                               time_stamp.tm_mon,
                               time_stamp.tm_mday,
                               time_stamp.tm_hour,
                               time_stamp.tm_min,
                               time_stamp.tm_sec))
        output_name = ("BenchTestData_Report_{}.csv".format(output_name))

        return self.__output_dir.joinpath(output_name)

    class _LogLineContent:
        """
        As the per line content refer to log,
        and finally generating the report.
        """
        __head_line = [
                       "LOG_DIR",
                       "LOG_NAME",
                       "LOG_SUFFIX",
                       "LOG_SIZE",
                       "LOG_CTIME",
                       ]

        @classmethod
        def add_head_item(cls, item):
            cls.__head_line.append(str(item))

        @classmethod
        def get_head_item_count(cls):
            return len(cls.__head_line)

        @classmethod
        def get_head_item_list(cls):
            return tuple(cls.__head_line)

        def __init__(self, log_file):
            self.__log_file = Path(log_file)
            self.__dir = str(self.__log_file.parent)
            self.__name = str(self.__log_file.stem)
            self.__suffix = str(self.__log_file.suffix)
            self.__size = str(self.__log_file.stat().st_size)
            self.__ctime = time.ctime(self.__log_file.stat().st_ctime)
            self.__data = [
                           self.__dir,
                           self.__name,
                           self.__suffix,
                           self.__size,
                           self.__ctime,
                           ]

        @property
        def log_file(self):
            return self.__log_file

        @property
        def dir(self):
            return self.__dir

        @property
        def name(self):
            return self.__name

        @property
        def suffix(self):
            return self.__suffix

        @property
        def size(self):
            return self.__size

        @property
        def ctime(self):
            return self.__ctime

        def add_data(self, data):
            self.__data.append(str(data))

        def get_line_content_list(self):
            return tuple(self.__data)

    def __add_report_head(self):
        if 'MaxCodeStep' == self.__test_item:
            for num in range(32):
                head_name = ("ORI_DATA{}".format(num))
                self._LogLineContent.add_head_item(head_name)
            for num in range(32):
                head_name = ("DATA{}".format(num))
                self._LogLineContent.add_head_item(head_name)
            for num in range(31):
                head_name = ("DAT_DIF[{}]".format(num))
                self._LogLineContent.add_head_item(head_name)

            self._LogLineContent.add_head_item("DAT_DIF_MAX")
            self._LogLineContent.add_head_item("DAT_DIF_MIN")
        elif 'RX_SystemSNR' == self.__test_item:
            self._LogLineContent.add_head_item("DATA_MEAN")
            self._LogLineContent.add_head_item("NOISE")
            self._LogLineContent.add_head_item("SNR")
            self._LogLineContent.add_head_item("DATAx")
        else:
            raise AttributeError ("'{}' test_item not support!".format(self.__test_item))

    def __parse_codestep_log(self, file_path):
        """
        Parse the single log from MaxCodeStep test,
        and store the info into the __report_database.
        """
        # get the original data from log
        report_line = self._LogLineContent(file_path)
        original_data_list = []
        read_fifo_count = 4
        phase_count = 8
        phase_index = 0
        match_wait = False
        with open(file_path, 'r') as log_handler:
            lines = log_handler.readlines()
            for line in lines:
                if read_fifo_count > 0:
                    if match_wait:
                        if line.find('reg_addr:0xff') > 0:
                            read_reg = search(r'val:0x(\w+)', line)
                            reg_hex_value = read_reg.group(1)
                            reg_hex_value = "{:0>6s}".format(reg_hex_value)

                            # split the reg value into phase index and original data
                            if phase_index == int(reg_hex_value[0], 16):
                                original_data = int(reg_hex_value[1:], 16)
                                if int(reg_hex_value[1], 16) >= 8:
                                    original_data -= 2**20
                                original_data_list.append(original_data)
                                report_line.add_data(original_data)
                            else:
                                raise AssertionError("read phase index '{}' not match with targeted '{}'!!"
                                                     .format(reg_hex_value[0], phase_index))

                            # control the search process
                            phase_index += 1
                            if phase_count == phase_index:
                                phase_index = 0
                                read_fifo_count -= 1
                                match_wait = False
                        else:
                            continue
                    else:
                        # find start line for getting the original data
                        if line.find('wait') > -1:
                            match_wait = True
                        else:
                            continue
                else:
                    break

        # check if get enough original data
        if 0 == read_fifo_count:
            print("MSG: {} MaxCodeStep log parsed successfully --".format(file_path))
        else:
            raise AssertionError("get data count is '{}' less than '{}' in file '{}'!!"
                                 .format(len(original_data_list), read_fifo_count * phase_count, file_path))

        # calculate the code data according to original data
        code_list = []
        for data in original_data_list:
            code = data / 128.0
            report_line.add_data(code)
            code_list.append(code)

        # calculate the code step value according to code list
        code_step_value_list = []
        for index in range(31):
            delta = code_list[index] - code_list[index+1]
            report_line.add_data(delta)
            code_step_value_list.append(delta)

        # get the max code step value according to code step value list
        max_delta = max(code_step_value_list)
        if 'B0' == self.__device_version:
            max_delta = max(code_step_value_list[16:])
        report_line.add_data(max_delta)

        # get the min code step value according to code step value list
        min_delta = min(code_step_value_list)
        if 'B0' == self.__device_version:
            min_delta = min(code_step_value_list[16:])
        report_line.add_data(min_delta)

        # store the report_line into report_database
        head_item_count = self._LogLineContent.get_head_item_count()
        line_content = report_line.get_line_content_list()

        if len(line_content) == head_item_count:
            self.__report_database.append(line_content)
        else:
            print("WARN: data line content count '{}' less than headline '{}' in file '{}'!"
                  .format(len(line_content), head_item_count, file_path))

    def __parse_snr_log(self, file_path):
        """
        Parse the single log from RX_SystemSNR test,
        and store the info into the __report_database.
        """
        # TODO: finish the snr log parse.
        print("WARN: not support yet!!")

    def add_log_file(self, file_path):
        """
        Add log_file into self.__log_file_list,
        and check if the log_file is legal.
        """
        log_file = Path(file_path).resolve()
        if log_file.exists() and log_file.is_file():
            self.__log_file_list.append(log_file)

    def parse_log_files(self):
        """
        Parse all the files in the __log_file_list,
        and store the info into the __report_database.
        """
        self.__add_report_head()

        if 'MaxCodeStep' == self.__test_item:
            for log in self.__log_file_list:
                self.__parse_codestep_log(log)
        elif 'RX_SystemSNR' == self.__test_item:
            for log in self.__log_file_list:
                self.__parse_snr_log(log)
        else:
            raise AttributeError ("'{}' test_item not support!".format(self.__test_item))

    def generate_report(self):
        """
        Generate report according to output file
        """
        with open(self.__output_file, 'w') as out_handler:
            # write headline in report
            headline = self._LogLineContent.get_head_item_list()
            out_handler.writelines(','.join(headline) + '\n')
            # write data line in report
            for line in self.__report_database:
                out_handler.writelines(','.join(line) + '\n')


if __name__ == '__main__':

    debug_mode = False
    # record start of time
    start_time = time.time()
    start_cpu_time = time.perf_counter()
    # parse args
    args = cli_help()
    proc_print('start')

    bench_test_data = BenchTestData(args.device_version, args.test_item, args.out_dir)
    if debug_mode: print("DEBUG: output file is {}".format(bench_test_data.output_file))

    proc_print('load files')
    if args.file:
        for file in args.file:
            bench_test_data.add_log_file(file)

    proc_print('load files in dir')
    if args.dir:
        in_dir = args.dir
        if Path(in_dir).is_dir():
            print("MSG: enter dir '%s' --" % in_dir)
        else:
            raise FileNotFoundError("input dir '%s' not exist !!!" % in_dir)

        file_list = []
        [file_list.append(str(f)) for f in Path(in_dir).glob('*.txt')]

        for file in file_list:
            bench_test_data.add_log_file(file)

    proc_print('parse logs')

    bench_test_data.parse_log_files()

    proc_print('output report')

    bench_test_data.generate_report()

    proc_print('finished')

    # Calc used time
    end_time = time.time()
    end_cpu_time = time.perf_counter()
    print("MSG: used time is {:.6f} s.".format(end_time - start_time))
    # print("MSG: CPU used time is {:.6f} s.".format(end_cpu_time - start_cpu_time))
