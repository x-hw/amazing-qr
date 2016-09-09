# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'MyQR',
    version = '1.0.0',
    keywords = ('qr', 'qrcode', 'qr code', 'artistic', 'animated', 'gif'),
    description = 'Generater for amazing qr codes. Including Common, Artistic and Animated qr codes.',
    long_description = '''
        Overview
        ===============
        It can generate common qr-code, artistic qr-code (black & white or colorized), animated qr-code (black & white or colorized).

        Usage
        ===============
        myqr words
             [-h]
             [-v {1,2,3,...,40}]
             [-l {L, M, Q, H}]
             [-p image_filename]
             [-c]
             [-con contrast_value]
             [-bri brightness_value]

        More
        ===============
        Please visit 'Home Page' blow for examples and details.
 
 
 
 
    ''',

    author = 'sylnsfar',
    author_email = 'sylnsfar@gmail.com',
    url = 'https://github.com/sylnsfar/qrcode',
    download_url = 'https://github.com/sylnsfar/qrcode',

    install_requires = [
        'imageio >= 1.5',
        'numpy >= 1.11.1',
        'Pillow>=3.3.1'
    ],
    packages = ['MyQR', 'MyQR.mylibs'],
    
    license = 'GPLv3',
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    entry_points = {
        'console_scripts': [
            'myqr = MyQR.__main__:run',
        ],
    }
)
