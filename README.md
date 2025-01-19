# Quine-McCluskey Minimization Tool

## Introduction

This repository contains a tool for minimizing Boolean functions using the Quine-McCluskey algorithm. The tool is designed with three main components:
- `documentation.py`: Contains the documentation for the implementation of the Quine-McCluskey algorithm.
- `cli.py`: A command line interface allowing users to input minterms, don't-cares, and variables to get the minimized Boolean function.
- `app.py`: A desktop application built using Tkinter, providing a graphical interface for the minimization process.

## Files

### documentation.py
This file includes comprehensive documentation of the implementation of the Quine-McCluskey algorithm used in this tool. It covers the theory, steps involved in the algorithm, and the implementation details.

### cli.py
A command line interface that:
- Prompts users to input minterms, don't-cares, and variables. If variables are not provided, it defaults to A, B, C, D.
- Displays the minimized Boolean function based on user input.

#### Usage:
python cli.py

Follow the prompts to enter your minterms, don't-cares, and variables.

### app.py
A graphical user interface (GUI) application built using Tkinter. This application provides an easy-to-use interface for users to input minterms, don't-cares, and variables, and view the minimized Boolean function.

#### Usage:
python app.py
This will launch the Tkinter-based desktop application.

## Installation
Clone the repository:

git clone https://github.com/yourusername/quine-mccluskey.git
cd quine-mccluskey
Install the required packages:

pip install -r requirements.txt


## Features
- Documentation: Detailed documentation of the Quine-McCluskey algorithm.

- CLI: Command Line Interface for users who prefer text-based interaction.

- GUI: Desktop application for users who prefer graphical interfaces.

## Contributing
We welcome contributions! Please follow these steps:

- Fork the repository.

- Create a new branch (git checkout -b feature-branch).

- Commit your changes (git commit -m 'Add new feature').

- Push to the branch (git push origin feature-branch).

- Create a new pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
Special thanks to all the contributors(Myself 😅) and users who helped improve this project!


This `README.md` covers the introduction, file descriptions, usage instructions, installation, features, contributing guidelines, license information, and acknowledgements. You can customize it further based on your specific needs. 😊 
