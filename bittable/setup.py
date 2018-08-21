from setuptools import setup, find_packages

setup(  
    name = "coderspider",  
    version = "0.1",  
    py_modules = ["spider","dbconfig"],  
    packages=find_packages(exclude=['tmp/*', 'test/*']),
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.yaml', '*.txt'],
        # include any *.msg files found in the 'hello' package, too:
        # 'hello': ['*.msg'],
    },
    author = "feilaoda",  
    author_email = "azhenglive@gmail.com",  
    url = "http://easyspider",  
    description = "news for coders",  
    )     

