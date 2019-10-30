from setuptools import setup

package_name = 'sound_system'

setup(
    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        'sound_system'
    ],
    install_requires=['setuptools'],
    data_files=[
        ('lib/' + package_name, ['package.xml']),
        ('lib/' + package_name+'/module',
         ['module/module_QandA.py',
          'module/module_pico.py',
          'module/module_angular.py',
          'module/module_detect.py',
          'module/module_beep.py',
          'module/module_count.py'
          ]),
        ('lib/sound_system/dictionary/',
         ['dictionary/hey_ducker.dict',
          'dictionary/hey_ducker.gram',
          'dictionary/new_spr_question.dict',
          'dictionary/new_spr_question.gram',
          'dictionary/yes_no.dict',
          'dictionary/yes_no.gram',
          ]),
        ('lib/sound_system/beep/',
         ['beep/speech.wav',
          'beep/start.wav',
          'beep/stop.wav'
          ]),
        ('lib/sound_system/dictionary/QandA',
            ['dictionary/QandA/qanda.csv']),
        ('lib/sound_system/log',
            ['log/log.txt'])
    ],
    zip_safe=True,
    author='HiroseChihiro',
    author_email='rr0111fx@ed.ritsumei.ac.jp',
    maintainer='ItoMasaki,MatsudaYamto',
    maintainer_email='is0449sh@ed.ritsumei.ac.jp,is0476hv@ed.ritsumei.ac.jp',
    keywords=['ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='sound package for SPR',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sound_system = sound_system:main',
        ],
    },
)