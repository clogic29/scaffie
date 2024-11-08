from setuptools import setup, find_packages

setup(
    name='scaffie',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # 필요한 의존 패키지
    author='clogic',
    author_email='choiseungil29@gmail.com',
    description='내가 쓸려고 만든 패키지',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/clogic/simple-scaffolder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
