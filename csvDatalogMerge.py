__version__ = '3.0'
"""History
Version    Date         Author          Description
3.0        20221214     Alvin3Hu        1.Replace modify time with create time of csv file;
                                        2.Add extend attribute for '--dir' parameter to support multi dir process at
                                          the same time.
                                        3.Change '-' into ':' in head items of output report headline,
                                          and add the unit info at the end of every head item;
                                        4.Comment the unit conversion message print;
                                        5.Add line number info in warning of data line item count doesn't match
                                          the headline;
"""

import argparse
import pathlib
import re
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
                        nargs='+',
                        type=Path,
                        help='directory including test log files',
                        )
    parser.add_argument('--out_dir',
                        '-o',
                        type=Path,
                        default=Path.cwd(),
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
    parser.add_argument('--head_file',
                        '-hf',
                        default='',
                        help='file for generating the headline of output report',
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
                  "LOG_MTIME",
                  ]


    # for unit conversion
    __units = ['','','','']
    __unit_type_list = [
        'V',  # voltage
        'A',  # current
        'W',  # power
        'S',  # time
        'HZ',  # frequency
        'R', 'OHM',  # resistance
        'LSB',  # Least Significant Bit
        'DB',  # DeciBel
        'DBM',  # DeciBel per Milli watt
    ]
    __factor_dict = {
        'M': 1e+6,
        'K': 1e+3,
        'k': 1e+3,
        '': 1,
        'm': 1e-3,
        'u': 1e-6,
        'n': 1e-9,
        'p': 1e-12,
        'f': 1e-15,
    }

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

    @classmethod
    def add_unit(cls, unit):
        unit = str(unit).replace(' ','')
        unit_split = cls.__unit_split(unit)
        if unit_split is None:
            print("WARN: unit '{}' is not recognizable!!".format(unit))
        cls.__units.append(unit)

    @classmethod
    def add_unit_list(cls, unit_list):
        for unit in unit_list:
            cls.add_unit(unit)

    @classmethod
    def __unit_split(cls, unit):
        """
        Split the unit into unit factor and unit type.
        """
        unit_factor = ""
        unit_type = ""
        if "" == unit:
            return "", None
        elif len(unit) == 1:
            if unit.lower() in cls.__factor_dict:
                return unit, None

        # if len(unit) > 1 and unit just have only 1 char but not factor
        for t in cls.__unit_type_list:
            if t in unit.upper():
                unit_type = t
                matched = re.match(r'^(\w)?{}$'.format(t), unit, re.IGNORECASE)
                if matched is None:
                    print("WARN: unit factor matched failed in '{}' !!".format(unit))
                    return None
                else:
                    if not matched.group(1) is None:
                        unit_factor = matched.group(1)
                        if not unit_factor in cls.__factor_dict:
                            print("WARN: unit factor '{}' is not recognizable !!".format(unit))
                            return None

        return unit_factor, unit_type

    def __init__(self, log_file):
        self.__log_file = Path(log_file)
        self.__dir = str(self.__log_file.parent)
        self.__name = str(self.__log_file.stem)
        self.__size = str(self.__log_file.stat().st_size)
        self.__mtime = time.ctime(self.__log_file.stat().st_mtime)
        self.__data = [
            self.__dir,
            self.__name,
            self.__size,
            self.__mtime,
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
        return self.__mtime

    def __unit_conversion(self, data, unit):
        """
        Data conversion refer to current unit and predefined unit.
        """
        # if no data
        if '' == data:
            return data

        # if data is not a digit, so it won't be calculated
        float_data = 0
        try:
            float_data = float(data)
        except ValueError:
            print("WARN: the data '{}' not a digit !!".format(data))
            return data

        # get the predefined unit
        next_data_index = len(self.__data)
        predefined_unit = self.__units[next_data_index]

        # delete the empty char in unit
        unit = unit.replace(' ','')
        if predefined_unit == unit:
            return data

        # data conversion if unit is not equal to predefined unit
        # get unit type and factor
        unit_factor = ""
        unit_type = ""
        unit_split = self.__unit_split(unit)
        if not unit_split is None:
            unit_factor = unit_split[0]
            unit_type = unit_split[1]
        else:
            print("WARN: unit factor and type matched failed in '{}' !!".format(unit))
            return data

        # get predefined unit type and factor
        predefined_unit_factor = ""
        predefined_unit_type = ""
        unit_split = self.__unit_split(predefined_unit)
        if not unit_split is None:
            predefined_unit_factor = unit_split[0]
            predefined_unit_type = unit_split[1]
        else:
            print("WARN: predefined unit factor and type matched failed in '{}' !!".format(predefined_unit))
            return data

        if unit_type == predefined_unit_type:
            float_data = float_data * self.__factor_dict[unit_factor] / self.__factor_dict[predefined_unit_factor]
            float_data = float("{:.6f}".format(float_data))
            # next_head_item = self.__headline[next_data_index]
            # print("MSG: '{} {}' is converted into '{} {}' for '{}' --"
            #       .format(data, unit, float_data, predefined_unit, next_head_item))
            return float_data
        else:
            print("WARN: different between the types of unit '{}' and predefined unit '{}' !!"
                  .format(unit, predefined_unit))
            return data

    def add_data(self, data, unit):
        new_data = self.__unit_conversion(data, unit)
        if new_data is None:
            self.__data.append(str(data))
        else:
            self.__data.append(str(new_data))

    def add_data_list(self, data_list, unit_list):
        for index in range(len(data_list)):
            self.add_data(data_list[index], unit_list[index])

    def get_line_content_list(self):
        return tuple(self.__data)


class CsvProcessor:
    """
    Collect and merge the csv files
    """

    def __init__(self, ate_model, output_dir, head_file):
        self.__ate_model = ate_model
        self.__output_dir = ""
        self.__head_file = ""

        if output_dir:
            self.__output_dir = Path(output_dir).resolve()
            self.__check_output_dir()
        else:
            self.__output_dir = Path.cwd()

        if head_file:
            self.__head_file = Path(head_file).resolve()

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

            unit_line = \
                [str(x) for x in lines[location_row_index].rstrip('\n').split(',')]
            test_suite_line = \
                [str(x) for x in lines[location_row_index-5].rstrip(',\n').split(',')]
            test_spec_line = \
                [str(x) for x in lines[location_row_index-4].rstrip(',\n').split(',')]
            headline = [':'.join(x) for x in zip(test_suite_line, test_spec_line)]

            for i in range(len(headline)):
                if ':' == headline[i]:
                    headline[i] = unit_line[i]
                    unit_line[i] = ''
                else:
                    headline[i] += ":{}".format(unit_line[i])

            OutputContent.add_head_item_list(headline)
            OutputContent.add_unit_list(unit_line)

        elif 'ST25XX' == self.__ate_model:
            print("WARN: ate_model '{}' not support yet!!".format(self.__ate_model))
        else:
            raise AttributeError ("'{}' ate_model not support!".format(self.__ate_model))

        print("MSG: generate merged csv headline successfully by {} --".format(csv_file))

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
        unit_item_list = []
        for i in range(len(lines)):
            line = lines[i]
            if match_serial:
                data_item_list = line.rstrip(',\n').split(',')
                data_content = OutputContent(csv_path)
                data_content.add_data_list(data_item_list, unit_item_list)

                # store the data_content into report_database
                line_content = data_content.get_line_content_list()
                self.__report_database.append(line_content)

                # check if line_content item count equal headline
                head_item_count = data_content.get_head_item_count()
                if not len(line_content) == head_item_count:
                    print("WARN: data line content count '{}' less than headline '{}' in file '{}' at line '{}'!"
                          .format(len(line_content), head_item_count, csv_path, i))

                # count data line
                data_line_count += 1

            elif match(r'^Serial#,', line):
                match_serial = True
                unit_item_list = line.rstrip('\n').split(',')

                # process the unit with '#' as suffix
                for index in range(len(unit_item_list)):
                    if unit_item_list[index].find('#') > 0:
                        unit_item_list[index] = ''
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
        if '' != self.__head_file:
            self.__add_report_head(self.__head_file)
        else:
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

    proc = CsvProcessor(args.ate_model, args.out_dir, args.head_file)

    proc.state_print('start')

    proc.state_print('load files')
    if args.file:
        for file in args.file:
            proc.add_log_file(file)

    proc.state_print('load files in dir')
    if args.dir:
        for in_dir in args.dir:
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
