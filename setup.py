from setuptools import setup, find_packages

setup(
    name='tron-shell',
    version='2.1',
    description='Universal Microcontroller Flashing Tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='ROOTCASTLE ENGINEERING INNOVATION',
    author_email='engineering@rootcastle.com',
    url='https://github.com/rootcastle-engineering/tron-shell',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyserial>=3.5',
        'pyusb>=1.2.1',
        'esptool>=4.5',
        'intelhex>=2.3.0',
        'pyyaml>=6.0',
        'colorama>=0.4.6'
    ],
    entry_points={
        'console_scripts': [
            'tron=bin.tron:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: System :: Hardware'
    ],
    license='Apache License 2.0',
    keywords='microcontroller flashing atmega esp32 tron bootloader'
)