from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='hamza khan',
    author_email='y7hamzakhanswati@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)