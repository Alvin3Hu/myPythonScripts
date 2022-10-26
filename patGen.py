__version__ = '1.0'

# import os
# import warnings
import argparse
from pathlib import *
from re import *


def cli_help() -> argparse.Namespace:
    """
    Parameter description by argparse lib.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=f"To generate register configuration patterns for ATE application\n"
                    f"| By Alvin \n"
                    f"| Ver {__version__}"
    )
    parser.add_argument('--file',
                        '-f',
                        nargs='+',
                        type=argparse.FileType('r', encoding='UTF-8'),
                        help='register configuration list file',
                        )
    parser.add_argument('--dir',
                        '-d',
                        type=Path,
                        help='directory including register configuration list files',
                        )
    parser.add_argument('--out_dir',
                        '-o',
                        type=Path,
                        # default='source files directory',
                        metavar='DIR',
                        help='output destination directory',
                        )
    parser.add_argument('--ate_model',
                        '-m',
                        default='Chroma3380P',
                        choices=['Chroma3380P'],
                        help='select ate tester model',
                        )
    parser.add_argument("--version",
                        action='version',
                        version=__version__,
                        )
    return parser.parse_args()


def parse_reg_file(handle: open) -> list:
    """
    Parse reg config file return the reg operation list.
    """

    reg_wr_list = []
    with handle as f:
        for line in f.readlines():
            # if match(r'^\s*#', line):
            #     continue
            # elif match(r'^\s*//', line):
            #     continue
            if match(r'^\s*(set|read)_register_data', line):
                reg = match(r'(set|read)_register_data\((\w+)\s*,\s*(\w+)\)', line)

                reg_wr_str = "%s,%s" % (reg.group(2), reg.group(3))
                if reg.group(1) == 'set':
                    reg_wr_str = 'w,' + reg_wr_str
                else:
                    reg_wr_str = 'r,' + reg_wr_str

                reg_wr_list.append(reg_wr_str)

    return reg_wr_list


def hex2bin(hex_num: str, bit_count: int) -> str:
    """
    Convert a hexadecimal number to a binary number
    """

    bin_num = format(int(hex_num, 16), ">0%db" % bit_count)
    return bin_num


def update_body_content(file_content: list, reg_act: str, reg_addr_bin: str, reg_data_bin: str) -> list:
    """
    Update address and data of destined reg
    """

    addr_bin_list = []
    for bit in reg_addr_bin:
        addr_bin_list.append(bit)

    data_bin_list = []
    for bit in reg_data_bin:
        data_bin_list.append(bit)

    update_file_content = []
    for line in file_content:
        if line.find('a') + line.find('d') == -2:
            pass
        elif match(r'^\s*\*[\w\s]*a', line):
            updated_bit = addr_bin_list.pop(0)
            line = line.replace('a', updated_bit, 1)
        elif match(r'^\s*\*[\w\s]*d', line):
            updated_bit = data_bin_list.pop(0)
            if reg_act == 'r':
                if updated_bit == '1':
                    updated_bit = 'H'
                else:
                    updated_bit = 'L'
            line = line.replace('d', updated_bit, 1)
        update_file_content.append(line)

    if len(addr_bin_list) > 0:
        raise ValueError("reg_addr_bin '%s' length not matched with the pattern body !!!" % reg_addr_bin)
    if len(data_bin_list) > 0:
        raise ValueError("reg_data_bin '%s' length not matched with the pattern body !!!" % reg_data_bin)

    return update_file_content


def pat_content(protocol_type: str, test_item: str, reg_list: list, ate_model: str) -> list:
    """
    Generating pattern content according to reg_list and protocol type.
    """

    pat_file_content = []
    script_name = PurePath(__file__).stem
    script_path = PurePath(__file__).parent
    pat_template_path = script_path / script_name / ate_model
    pat_name = protocol_type + '_' + test_item

    # take pattern head
    with open(pat_template_path / (protocol_type + '_Head.pat'), 'r') as head_handle:
        lines = head_handle.readlines()
        for line in lines:
            if line.find('TestItem') > -1:
                line = line.replace('TestItem', pat_name)
            pat_file_content.append(line)

    # take pattern body
    for reg_wr in reg_list:
        reg_act, reg_addr, reg_data = reg_wr.split(',')

        reg_addr_bin = hex2bin(reg_addr, 8)
        reg_data_bin = hex2bin(reg_data, 16)

        if reg_act == 'w':
            body_handle = open(pat_template_path / (protocol_type + '_Write.pat'), 'r')
        elif reg_act == 'r':
            body_handle = open(pat_template_path / (protocol_type + '_Read.pat'), 'r')
        else:
            raise ValueError("reg_act '%s' is illegal !!!" % reg_act)
        body_content = update_body_content(body_handle.readlines(), reg_act, reg_addr_bin, reg_data_bin)

        pat_file_content.extend(body_content)

    # take pattern tail
    with open(pat_template_path / (protocol_type + '_Tail.pat'), 'r') as tail_handle:
        lines = tail_handle.readlines()
        pat_file_content.extend(lines)

    return pat_file_content


def pat_output(file_content: list, file_path: Path, file_name: str) -> bool:
    """
    Output pattern file towards destination directory.
    """

    if not Path(file_path).exists():
        Path.mkdir(file_path)
        print("WARN: file_path '%s' not exists and to be created automatically !" % file_path)

    out_file = file_path / file_name
    if Path(out_file).exists():
        print("WARN: out_file '%s' is exists , original file will be overwritten !" % out_file)

    with open(out_file, 'w') as f:
        f.writelines(file_content)

    return True


def pat_gen_file(handle: open, output_path: Path, ate_model: str) -> bool:
    """
    Parse source file and generated corresponding pattern file.
    """

    print("MSG: dealing with '%s' --" % handle.name)

    # parse protocol and test_item
    file_name = Path(handle.name).stem
    protocol, test_item = file_name.split('_', 1)

    # check output_path
    file_dir = Path(handle.name).parent
    if not Path(output_path).exists:
        output_path = file_dir

    reg_wr_list = parse_reg_file(handle)

    pat_file_content = pat_content(protocol, test_item, reg_wr_list, ate_model)

    out_file_name = file_name
    if ate_model == "Chroma3380P":
        out_file_name = out_file_name + '.pat'

    proc_result = pat_output(pat_file_content, output_path, out_file_name)

    return proc_result


def proc_print(state: str):
    """
    Print for process
    """

    script_name = PurePath(__file__).stem
    print('*'*10, script_name + ' => ' + state, '*'*10)


if __name__ == '__main__':

    # parse args
    args = cli_help()
    proc_print('start')

    out_dir = ''
    if args.out_dir:
        out_dir = args.out_dir
        if Path(out_dir).exists():
            print("MSG: output dir '%s' exists --" % out_dir)
        else:
            Path.mkdir(out_dir)
            print("WARN: output dir '%s' not exists and to be created automatically !" % out_dir)

    proc_print('files')
    if args.file:
        for file in args.file:
            pat_gen_file(file, out_dir, args.ate_model)

    proc_print('dir')
    if args.dir:
        in_dir = args.dir
        if Path(in_dir).is_dir():
            print("MSG: enter dir '%s' --" % in_dir)
        else:
            raise FileNotFoundError("input dir '%s' not exist !!!" % in_dir)

        file_list = []
        [file_list.append(str(f)) for f in Path(in_dir).glob('SPI*.txt')]
        [file_list.append(str(f)) for f in Path(in_dir).glob('I2C*.txt')]

        for file in file_list:
            file_handle = open(file, 'r')
            pat_gen_file(file_handle, out_dir, args.ate_model)

    proc_print('finished')
