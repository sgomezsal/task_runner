# Task Runner CLI

## Overview
Task Runner is a command-line interface (CLI) designed to facilitate task management based on the Getting Things Done (GTD) methodology. It allows users to efficiently manage their tasks directly from the terminal without the need for an external GUI application. The CLI is built using Python and is designed to be lightweight and dependency-free, ensuring it runs smoothly on any system with Python installed.

## Installation

### Cloning the Repository
To install Task Runner, you first need to clone the repository:
```bash
git clone git@github.com:sgomezsal/task_runner.git
```

### Setting Up
Since Task Runner is a Python-based script that does not rely on external libraries, you can start using it right after cloning. However, make sure Python is installed on your system.

## Usage
To start using Task Runner, navigate to the cloned directory and run the script from your terminal:
```bash
cd task_runner
python main.py [arguments]
```

You can access a list of commands and their descriptions by running:
```bash
python main.py --help
```

## Contributing
Contributions to Task Runner are welcome! Here are some of the ways you can contribute:
- Reporting bugs
- Suggesting enhancements
- Submitting pull requests with fixes and improvements

### Development Notes
- **Aesthetic and Performance Improvements:** Future updates aim to enhance the user interface and the overall performance of the application.
- **Cross-Platform Compatibility:** There is a plan to adapt Task Runner for use on multiple platforms by integrating Farmdroid.

### Untracking the .app_data Folder
If you clone this repository and start adding your tasks, you might notice the `.app_data` directory showing up in your Git status. To avoid tracking changes in this directory, run the following command:
```bash
find .app_data -type f -exec git update-index --assume-unchanged {} \;
```
This command will mark all files under `.app_data` as unchanged, so Git will ignore them in future commits.

## License
This project is released under the [MIT License](LICENSE).

## Contact
For any further questions or feedback, please don't hesitate to contact [Sergio Gomez Salazar](mailto:sgomez@example.com).

### Notes:
- **License:** You should include a LICENSE file in your repository if it's not already there. I've assumed MIT, which is common for open-source projects, but you should choose the license that best fits your project.
- **Contact Information:** I added a placeholder email address; please replace it with your actual contact information.
- **Repository URL:** Double-check the repository clone command to ensure it’s correct and accessible by others.
  
This README should help get users started with your project and encourage contributions from the community.
