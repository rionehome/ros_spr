from setuptools import setup

package_name = 'image_system'

setup(

    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        'image_system',
    ],
    data_files=[
        ('lib/' + package_name, ['package.xml']),
        ('lib/' + package_name+'/detect_modules/detect_human',
         ['detect_modules/detect_human/CocoPoseNet.py',
          'detect_modules/detect_human/FaceNet.py',
          'detect_modules/detect_human/HandNet.py',
          'detect_modules/detect_human/detect_human.py',
          'detect_modules/detect_human/entity.py',
          'detect_modules/detect_human/pose_detector.py',
          ]),
        ('lib/'+package_name+'/detect_modules/detect_sex',
         ['detect_modules/detect_sex/classifier.py',
          'detect_modules/detect_sex/detect_sex.py',
          'detect_modules/detect_sex/model.py'
          ]),
        ("lib/" + package_name + "/model",
            [
                "model/cifier_adam.npz",
                "model/coco_posenet.npz",
                "model/haarcascade_frontalface_alt.xml",
                "model/haarcascade_frontalface_default.xml"
            ]
        )
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='ItoMasaki',
    author_email='is0449sh@ed.ritsumei.ac.jp',
    maintainer='ItoMasaki',
    maintainer_email='is0449sh@ed.ritsumei.ac.jp',
    keywords=['ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='image syste is made using ROS2',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'image_system=image_system:main'
        ],
    },
)
