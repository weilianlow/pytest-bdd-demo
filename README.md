# pytest-bdd-demo
This project show cases backend testing using pytest-bdd.

## Installation
1. Git clone git repo.

2. Create a virtual environment in the root folder of the git repo.<br/>
**Note**: ```pip install virtualenv``` if ```pip freeze|grep virtualenv``` returns empty.
    ```sh
    # For Python 2
    virtualenv venv
   
    # For Python 3
    python3 -m venv venv
    ```
3. Configure your IDE's python interpreter with the virtual environment created from the previous step.<br/>
**Note**: You can ```pip install pytest-sugar``` to change the default look and feel of pytest.  
   ```sh
   # Pycharm
   Preferences → Project → Python Interpreter
   
   # VS Code
   ```
5. Install project dependencies via requirements.txt.
    ```sh
    # For Python 2
    pip install -r requirements.txt
   
    # For Python 3
    pip3 install -r requirements.txt
    ```
## Verifying your test
| Scope Level | Command                                            | Example                                                      |
|-------------|----------------------------------------------------|--------------------------------------------------------------|
| All         | pytest                                             | pytest                                                       |
| Folder      | pytest {folder}                                    | pytest tests/mixer/step_defs/                                |
| Module      | pytest {folder}/{module}                           | pytest tests/mixer/step_defs/test_ab_testing.py              |
| Scenario    | pytest {folder}/{module}::{scenario}               | pytest tests/mixer/step_defs/test_ab_testing.py::test_1      |
| Iteration   | pytest {folder}/{module}::{scenario}[{iteration}]  | pytest tests/mixer/step_defs/test_ab_testing.py::test_1[i-1] |

## Generate Report
   ```sh
    # Junit xml
    pytest --junitxml=reports.xml
   ```
