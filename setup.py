from setuptools import setup

setup(name='ymlai87416_common',
        version='1.0',
        description='For my daily use',
        url='https://github.com/ymlai87416/ymlai87416_common',
        author='ymlai87416',
        author_email='ymlai87416@gmail.com',
        license='copyright',
        packages=['ymlai87416_common', 'ymlai87416_common.data'],
        install_requires=[
            'PyYAML', 'pandas', 'pandas-datareader',
            'alpaca-trade-api',
            'google-api-core',
            'google-api-python-client',
            'google-auth',
            'google-auth-httplib2',
            'google-auth-oauthlib',
            'googleapis-common-protos',
            'yfinance',
            'pandas_datareader',
        ],
        zip_safe=False
)