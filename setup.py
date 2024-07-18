from setuptools import setup, find_packages

setup(
    name="ShareXpress",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt5",
        # Adicione outras dependências necessárias aqui
    ],
    entry_points={
        'console_scripts': [
            'sharexpress = main:main',  # Ajuste conforme necessário
        ],
    },
    author="Weslei Ferreira Santos",
    author_email="wesleiferreira608@gmail.com",
    description="Um aplicativo para enviar arquivos entre dispositivos",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
