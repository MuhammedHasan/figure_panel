from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = [
    'setuptools',
    'svgutils',
    'svglib',
    'cairosvg',
    'click'
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest']

setup(
    name='figure_panel',
    version='0.0.1',

    author="M. Hasan Çelik",
    author_email='muhammedhasancelik@gmail.com',
    url='https://github.com/muhammedhasan/figure_paper',

    keywords=['figure panel', 'plotting', 'publication'],
    description="Create publication ready figure panels from svg files.",

    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    license="MIT license",
    long_description=readme + '\n',
    long_description_content_type='text/markdown',

    install_requires=requirements,
    setup_requires=setup_requirements,

    entry_points='''
        [console_scripts]
        figure_panel=figure_panel.main:cli_figure_panel
    ''',
    packages=find_packages(include=['lapa*']),
    include_package_data=True,

    test_suite='tests',
    tests_require=test_requirements,
)
