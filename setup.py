from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='docov',
    version='0.0.3',
    description='Light-weight docstring coverage analysis for python modules', 
    long_description=long_description, 
    long_description_content_type='text/markdown', 
    url='https://github.com/ripaul/docov',
    author='Richard D. Paul',
    author_email='r.paul@fz-juelich.de',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='coverage, development',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['anybadge', 'argparse'],
    entry_points={
        'console_scripts': [
            'docov=docov:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/ripaul/docov/issues',
        'Source': 'https://github.com/ripaul/docov/',
    },
)
