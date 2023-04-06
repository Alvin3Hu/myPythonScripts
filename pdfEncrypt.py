__version__ = '1.0'
"""History
Version    Date         Author          Description
1.0        20230406     Alvin3Hu        Initial
"""

import argparse
import pathlib
import time
from pathlib import *
from PyPDF2 import PdfWriter, PdfReader
import base64


def cli_help() -> argparse.Namespace:
    """
    Parameter description by argparse lib.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=f"To encrypt the pdf file\n"
                    f"| By Alvin \n"
                    f"| Ver {__version__}"
    )
    parser.add_argument('company',
                        help='which one company the pdf files are encrypted for',
                        )
    parser.add_argument('--file',
                        '-f',
                        nargs='+',
                        type=Path,
                        help='pdf source file',
                        )
    parser.add_argument('--dir',
                        '-d',
                        nargs='+',
                        type=Path,
                        help='directory including pdf source files',
                        )
    parser.add_argument('--out_dir',
                        '-o',
                        type=Path,
                        default=Path.cwd(),
                        metavar='DIR',
                        help='output destination directory\n'
                             'default: current work dir',
                        )
    parser.add_argument('--debug',
                        '-g',
                        action="store_true",
                        help='debug log print',
                        )
    parser.add_argument("--version",
                        action='version',
                        version=__version__,
                        )
    return parser.parse_args()


class PdfEncryptProc:
    """
    Collect and parse the bench test log for report generation.
    """

    def __init__(self, company, output_dir, debug_mode):
        self.state_print('start')

        self.__debug = debug_mode
        self.__varMsgPrint('debug', self.__debug)
        self.__company = company
        self.__varMsgPrint('company', self.__company)
        self.__cipher = self.__get_cipher()
        self.__varMsgPrint('cipher', self.__cipher)

        self.__output_dir = ""
        if output_dir:
            self.__output_dir = Path(output_dir).resolve()
            self.__check_output_dir()
        else:
            self.__output_dir = Path.cwd()
        self.__varMsgPrint('output_dir', self.__output_dir)

        self.__pdf_file_list = []

    def __check_output_dir(self):
        """
        Check if the output dir is exists and make its parent dir if not exists.
        """
        output_dir = Path(self.__output_dir)

        if output_dir.exists():
            pass
        else:
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except FileExistsError:
                pass
            else:
                print("WARN: output dir '{}' not exists and to be created automatically !"
                      .format(output_dir))

    def __varMsgPrint(self, varName: str, var):
        print("MSG: %10s -> " %(varName), var)

    def __varDbgPrint(self, varName: str, var):
        print("DBG: %14s = " % (varName), var)

    def __get_cipher(self) -> str:
        """
        Generate the cipher refer to company name.
        """
        plain = self.__company
        cipher = ''

        # pre-encoding cipher
        plainLen = len(plain)
        if 1 == plainLen % 3:
            cipher = 'W' + plain + 'M'
        elif 2 == plainLen % 3:
            cipher = plain + 'M'
        else:
            cipher = plain
        if self.__debug:
            self.__varDbgPrint('cipher_src', cipher)

        # cipher reversed
        cipher = cipher[::-1]
        if self.__debug:
            self.__varDbgPrint('reverse', cipher)

        # encoding cipher by base64
        bCipher = cipher.encode('utf-8')
        bCipherBase64 = base64.b64encode(bCipher)
        cipher = bCipherBase64.decode('utf-8')

        if self.__debug:
            self.__varDbgPrint('cipher', cipher)

        return cipher

    def add_pdf_file(self, file_path):
        """
        Add pdf source file into self.__pdf_file_list,
        and check if the pdf file is legal.
        """
        pdf_file = Path(file_path).resolve()
        if pdf_file.exists() and pdf_file.is_file():
            self.__pdf_file_list.append(pdf_file)
            print("MSG: load file {} successfully --".format(pdf_file))
        else:
            print("WARN: load file {} failed !!".format(pdf_file))

    def encrypt_pdf_files(self):
        """
        Encrypt all the pdf files in the __pdf_file_list.
        """
        for pdfFl in self.__pdf_file_list:
            flFullPath = Path(pdfFl)
            flPath = flFullPath.parent
            flName = flFullPath.stem
            flSffx = flFullPath.suffix
            outFlName = flName + '_' + self.__company

            if flSffx != '.pdf':
                raise Exception("ERR: the file isn't pdf, pls check it!")

            outFl = self.__output_dir.joinpath(outFlName+flSffx)

            if self.__debug:
                self.__varDbgPrint('flFullPath', flFullPath)
                self.__varDbgPrint('flPath', flPath)
                self.__varDbgPrint('flName', flName)
                self.__varDbgPrint('flSffx', flSffx)
                self.__varDbgPrint('outFlName', outFlName)
                self.__varDbgPrint('outFl', outFl)

            pdfReader = PdfReader(pdfFl)
            if pdfReader.is_encrypted:
                print("ERR: file {} encrypt failed, because had been encrypted before!".format(pdfFl))
            else:
                pdfWriter = PdfWriter()

                for page in range(len(pdfReader.pages)):
                    pdfWriter.add_page(pdfReader.pages[page])

                if '' == self.__cipher:
                    raise ValueError("ERR: the cipher text get failed!")

                pdfWriter.encrypt(self.__cipher)  # setting password
                with open(outFl, 'wb') as out:
                    pdfWriter.write(out)
                print("MSG: output file {} successfully --".format(outFl))

        return 1

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

    proc = PdfEncryptProc(args.company, args.out_dir, args.debug)

    proc.state_print('load files')
    if args.file:
        for file in args.file:
            proc.add_pdf_file(file)

    proc.state_print('load files in dir')
    if args.dir:
        for in_dir in args.dir:
            if Path(in_dir).is_dir():
                print("MSG: enter dir '%s' --" % in_dir)
            else:
                raise FileNotFoundError("input dir '%s' not exist !!!" % in_dir)

            file_list = []
            [file_list.append(str(f)) for f in Path(in_dir).glob('*.pdf')]

            for file in file_list:
                proc.add_pdf_file(file)

    proc.state_print('pdf encrypt')

    proc.encrypt_pdf_files()

    proc.state_print('finished')

    # Calc used time
    end_time = time.time()
    print("MSG: used time is {:.6f} s.".format(end_time - start_time))
