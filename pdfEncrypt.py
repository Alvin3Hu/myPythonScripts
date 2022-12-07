from PyPDF2 import PdfFileWriter, PdfFileReader
import base64
import os
import warnings


# global var definition
warnings.filterwarnings("ignore")
pdfFl = r'E:\AhuWorkFiles\02_Office\01_Company\02_Introduction\鲸鱼微电子介绍_WanNianXin.pdf'
plainText = "WanNianXin"
outFlSffx = "Enc"
debug = True
debug = False

def scriptPrint(scriptName: str, state: str):
    print('*'*10, scriptName + ' => ' + state, '*'*10)

def varMsgPrint(varName: str, var):
    print("MSG: %10s -> " %(varName), var)

def varDbgPrint(varName: str, var):
    print("DBG: %14s = " % (varName), var)


# sub function
def getCipher(plain: str):
    cipher = ''

    # pre-encoding cipher
    plainLen = len(plain)
    if 1 == plainLen % 3:
        cipher = 'W' + plain + 'M'
    elif 2 == plainLen % 3:
        cipher = plain + 'M'
    else:
        cipher = plain

    if debug:
        varDbgPrint('cipher', cipher)


    # cipher reversed
    cipher = cipher[::-1]
    if debug:
        varDbgPrint('cipher', cipher)

    # encoding cipher by base64
    bCipher = cipher.encode('utf-8')
    bCipherBase64 = base64.b64encode(bCipher)
    cipher = bCipherBase64.decode('utf-8')
    if debug:
        varDbgPrint('cipher', cipher)

    return cipher

def pdfEncrypt(pdfFl: str, cipher: str, outFlSffx: str):
    # get file path and name
    flPath = os.path.dirname(pdfFl)
    flName = os.path.basename(pdfFl)
    flSffx= os.path.splitext(flName)[1]
    flName = os.path.splitext(flName)[0]
    outFlName = flName

    if '' != outFlSffx:
        outFlName = outFlName + '_' + outFlSffx

    if flSffx != '.pdf':
        raise Exception("ERR: the file isn't pdf, pls check it!")

    outFl = os.path.join(flPath, outFlName+flSffx)

    if debug:
        varDbgPrint('flPath', flPath)
        varDbgPrint('flName', flName)
        varDbgPrint('flSffx', flSffx)
        varDbgPrint('outFlName', outFlName)
        varDbgPrint('outFl', outFl)


    pdfReader = PdfFileReader(pdfFl)
    pdfWriter = PdfFileWriter()

    for page in range(pdfReader.getNumPages()):
        pdfWriter.addPage(pdfReader.getPage(page))
    pdfWriter.encrypt(cipher)  # setting password
    with open(outFl, 'wb') as out:
        pdfWriter.write(out)

    return 1


# main
scriptPrint('pdfEncrypt', 'start')
varMsgPrint('input file', pdfFl)
varMsgPrint('company', plainText)
varMsgPrint('out suffix', outFlSffx)

cipherText = getCipher(plainText)
if '' == cipherText:
    raise ValueError("ERR: the cipher text get failed!")
else:
    varMsgPrint('cipher', cipherText)
try:
    pdfEncrypt(pdfFl, cipherText, outFlSffx)
except:
    scriptPrint('pdfEncrypt', 'FAILED')
else:
    scriptPrint('pdfEncrypt', 'passed')
finally:
    scriptPrint('pdfEncrypt', 'finished')


