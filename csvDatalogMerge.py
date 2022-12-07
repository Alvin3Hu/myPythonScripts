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
        description=f"To merge the csv data logs from ATE test result\n"
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
                        metavar='DIR',
                        help='output destination directory\n'
                             'default: current work dir',
                        )
    parser.add_argument('--ate_model',
                        '-m',
                        default='Chroma3380P',
                        choices=['Chroma3380P', 'ST25XX'],
                        help='select ate tester model\n'
                             'default: Chroma3380P',
                        )
    parser.add_argument("--version",
                        action='version',
                        version=__version__,
                        )
    return parser.parse_args()


class OutputContent:
    """
    Collect the content from every csv file,
    and generate the merged csv datalog.
    """

    __headline = [
                  "LOG_DIR",
                  "LOG_NAME",
                  "LOG_SIZE",
                  "LOG_CTIME",
                  ]

    @classmethod
    def add_head_item(cls, item):
        cls.__headline.append(str(item))

    @classmethod
    def add_head_item_list(cls, item_list):
        item_list = [str(x) for x in item_list]
        cls.__headline.extend(item_list)

    @classmethod
    def get_head_item_count(cls):
        return len(cls.__headline)

    @classmethod
    def get_head_item_list(cls):
        return tuple(cls.__headline)

    def __init__(self, log_file):
        self.__log_file = Path(log_file)
        self.__dir = str(self.__log_file.parent)
        self.__name = str(self.__log_file.stem)
        self.__size = str(self.__log_file.stat().st_size)
        self.__ctime = time.ctime(self.__log_file.stat().st_ctime)
        self.__data = [
            self.__dir,
            self.__name,
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
    def size(self):
        return self.__size

    @property
    def ctime(self):
        return self.__ctime

    def add_data(self, data):
        self.__data.append(str(data))

    def add_data_list(self, data_list):
        data_list = [str(x) for x in data_list]
        self.__data.extend(data_list)

    def get_line_content_list(self):
        return tuple(self.__data)


class CsvProcessor:
    """
    Collect and merge the csv files
    """

    def __init__(self, ate_model, output_dir=None):
        self.__ate_model = ate_model
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

        time_str = (("{:0>2}" * 3 + '-' + "{:0>2}" * 3)
                       .format(time_stamp.tm_year % 2000,
                               time_stamp.tm_mon,
                               time_stamp.tm_mday,
                               time_stamp.tm_hour,
                               time_stamp.tm_min,
                               time_stamp.tm_sec))
        output_name = ("{}_csvMerged_{}.csv".format(self.__output_dir.parent.name, time_str))

        return self.__output_dir.joinpath(output_name)

    def __add_report_head(self, csv_file):
        """
        Parse the first csv file in __log_file_list,
        and generate the headline into OutputContent class.
        """
        if 'Chroma3380P' == self.__ate_model:
            with open(csv_file, 'r') as csv_handler:
                lines = csv_handler.readlines()

            # find the row index of location line
            location_row_index = -1
            for index in range(len(lines)):
                if match(r'^Serial#', lines[index]):
                    location_row_index = index

            if -1 == location_row_index:
                raise AssertionError("location row not matched in file '{}'"
                                     .format(csv_file))

            location_line = \
                [str(x) for x in lines[location_row_index].rstrip(',\n').split(',')]
            test_suite_line = \
                [str(x) for x in lines[location_row_index-5].rstrip(',\n').split(',')]
            test_spec_line = \
                [str(x) for x in lines[location_row_index-4].rstrip(',\n').split(',')]
            headline = ['-'.join(x) for x in zip(test_suite_line, test_spec_line)]

            for i in range(len(headline)):
                if '-' == headline[i]:
                    headline[i] = location_line[i]

            OutputContent.add_head_item_list(headline)

        elif 'ST25XX' == self.__ate_model:
            print("WARN: ate_model '{}' not support yet!!".format(self.__ate_model))
        else:
            raise AttributeError ("'{}' ate_model not support!".format(self.__ate_model))

        print("MSG: generate merged csv headline successfully --")

    def __parse_chroma3380p_csv(self, csv_path):
        """
        Parse csv from Chroma3380P ATE test result,
        and store the info into the __report_database.
        """
        # get the data content from csv
        with open(csv_path, 'r') as csv_handler:
            lines = csv_handler.readlines()

        match_serial = False
        data_line_count = 0
        for line in lines:
            if match_serial:
                data_item_list = line.rstrip(',\n').split(',')
                data_content = OutputContent(csv_path)
                data_content.add_data_list(data_item_list)

                # store the data_content into report_database
                line_content = data_content.get_line_content_list()
                self.__report_database.append(line_content)

                # check if line_content item count equal headline
                head_item_count = data_content.get_head_item_count()
                if not len(line_content) == head_item_count:
                    print("WARN: data line content count '{}' less than headline '{}' in file '{}'!"
                          .format(len(line_content), head_item_count, csv_path))

                # count data line
                data_line_count += 1

            elif match(r'^Serial#,', line):
                match_serial = True
            else:
                continue

        if data_line_count > 0:
            print("MSG: {} file process {} data line successfully --".format(csv_path, data_line_count))
        else:
            print("WARN: {} file process failed !!".format(csv_path))


    def __parse_st25xx_csv(self, csv_path):
        """
        Parse csv from ST25xx ATE test result,
        and store the info into the __report_database.
        """
        # TODO: finish parsing csv from ST25XX.
        print("WARN: ate_model '{}' not support yet!!".format(self.__ate_model))

    def merge_csv_files(self):
        """
        Catch the data from every csv file,
        and store them into __report_database.
        """
        for csv in self.__log_file_list:
            try:
                self.__add_report_head(csv)
            except AssertionError:
                print("WARN: get headline failed in file '{}'!!".format(csv))
                continue
            else:
                break

        if 'Chroma3380P' == self.__ate_model:
            for csv in self.__log_file_list:
                self.__parse_chroma3380p_csv(csv)
        elif 'ST25XX' == self.__ate_model:
            for csv in self.__log_file_list:
                self.__parse_st25xx_csv(csv)
        else:
            raise AttributeError ("'{}' ate_model not support!".format(self.__ate_model))

    def add_log_file(self, file_path):
        """
        Add log_file into self.__log_file_list,
        and check if the log_file is legal.
        """
        log_file = Path(file_path).resolve()
        if log_file.exists() and log_file.is_file():
            self.__log_file_list.append(log_file)
            print("MSG: load file {} successfully --".format(log_file))
        else:
            print("WARN: load file {} failed !!".format(log_file))

    def generate_report(self):
        """
        Generate report according to output file
        """
        with open(self.__output_file, 'w') as out_handler:
            # write headline in report
            headline = OutputContent.get_head_item_list()
            out_handler.writelines(','.join(headline) + '\n')
            # write data line in report
            for line in self.__report_database:
                out_handler.writelines(','.join(line) + '\n')

        print("MSG: generate {} file successfully --".format(self.__output_file))

    @staticmethod
    def state_print(state: str = None):
        """
        Print for process
        """

        proc_str = '*' * 20

        if state:
            proc_str += ("{} => {}".format(PurePath(__file__).stem, state))

        print("{:*<100s}".format(proc_str))


if __name__ == '__main__':

    debug_mode = False
    # record start of time
    start_time = time.time()
    # parse args
    args = cli_help()

    proc = CsvProcessor(args.ate_model, args.out_dir)

    proc.state_print('start')

    proc.state_print('load files')
    if args.file:
        for file in args.file:
            proc.add_log_file(file)

    proc.state_print('load files in dir')
    if args.dir:
        in_dir = args.dir
        if Path(in_dir).is_dir():
            print("MSG: enter dir '%s' --" % in_dir)
        else:
            raise FileNotFoundError("input dir '%s' not exist !!!" % in_dir)

        file_list = []
        [file_list.append(str(f)) for f in Path(in_dir).glob('*.csv')]

        for file in file_list:
            proc.add_log_file(file)

    proc.state_print('merge csv files')

    proc.merge_csv_files()

    proc.state_print('output report')

    proc.generate_report()

    proc.state_print('finished')

    # Calc used time
    end_time = time.time()
    print("MSG: used time is {:.6f} s.".format(end_time - start_time))