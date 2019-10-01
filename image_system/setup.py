from setuptools import setup

package_name = 'image_system'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        'image_system'
    ],
    install_requires=['setuptools'],
    data_files=[
        ('lib/' + package_name, ['package.xml'])
    ],
    zip_safe=True,
    author='ItoMasaki,MatsudaYamato',
    author_email='is0449sh@ed.ritsumei.ac.jp,is0476hv@ed.ritsumei.ac.jp',
    maintainer='ItoMasaki,MatsudaYamato',
    maintainer_email='is0449sh@ed.ritsumei.ac.jp,is0476hv@ed.ritsumei.ac.jp',
    keywords=['ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='image package for SPR',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_system = image_system:main',
        ],
    },
)
