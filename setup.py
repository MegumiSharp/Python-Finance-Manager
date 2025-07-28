from setuptools import setup, find_packages

setup(
    name="python-finance-manager",
    version="0.1",
    description="A simple finance manager application",
    author="Your Name",
    author_email="simone.enselmi@gmail.com",
    packages= find_packages(),
    install_requires=[
        "customtkinter",
        "Pillow",
        "CTkTable",
        "tkinter",
        "json"
    ],
)