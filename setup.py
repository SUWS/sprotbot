
from setuptools import setup, find_packages

setup(name = "sprotbot",
      description = "A bot for sending out SUWS emails.",
      packages = find_packages(),
      author = "Darren Richardson",
      version = "1",
      install_requires = [
            "boto3==1.4.4",
            "click==6.7"
      ],)
