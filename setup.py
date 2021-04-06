# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='amzqr',
    version='0.0.2',
    keywords='qr qrcode amazing artistic animated gif colorized',
    description='Generater for amazing QR Codes. Including Common, Artistic and Animated QR Codes.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='hw',
    author_email='xhaowen.xu@gmail.com',
    url='https://github.com/hwxhw/amazing-qr',
    download_url='https://github.com/hwxhw/amazing-qr',
    project_urls={
        "Bug Tracker": "https://github.com/hwxhw/amazing-qr/issues",
    },
    install_requires=[
        'imageio >= 1.5',
        'numpy >= 1.11.1',
        'Pillow>=3.3.1'
    ],
    packages=['amzqr', 'amzqr.mylibs'],
    license='GPLv3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    entry_points={
        'console_scripts': [
            'amzqr=amzqr.terminal:main',
        ],
    },
    python_requires=">=3",
)
