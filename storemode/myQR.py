# import modules
import qrcode
from PIL import Image
import sys


class myQR:
    # _logo = _url = _output = ""
    # def __init__(self):
    #     args = sys.argv
    #     _logo = args[1]
    #     _url = args[2]
    #     _output = args[3]

    def generate(self, _logo, _url, _ouput):
        # taking image which user wants
        # in the QR code center
        # Logo_link = self._logo
        logo = Image.open(_logo)
        logo.crop()
        logo.thumbnail((1024, 1024))
        # taking base width
        basewidth = 100
        # adjust image size
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.FIXED)
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M
        )

        # taking url or text
        # adding URL or text to QRcode
        QRcode.add_data(_url)

        # generating QR code
        QRcode.make()

        # taking color name from user
        QRcolor = 'Black'

        # adding color to QR code
        QRimg = QRcode.make_image(fill_color=QRcolor, back_color="white").convert('RGB')

        # set size of QR code
        pos = (((QRimg.size[0] - logo.size[0]) // 2), ((QRimg.size[1] - logo.size[1]) // 2))

        # QRimg.paste(logo, pos)

        # save the QR code generated
        QRimg.save(_output)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # asyncio.run(getProduct())
    args = sys.argv
    _logo = args[1]
    _url = args[2]
    _output = args[3]

    _qr = myQR()
    _qr.generate(_logo, _url, _output)
    print('QR code generated!')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
