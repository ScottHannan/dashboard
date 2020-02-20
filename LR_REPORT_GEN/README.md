# LoadRunner Automated Report Generator (LARG) 

LARG is a web service that is used to automate the generation of Loadrunner reports.

## Linux/MacOS Installation -- TO RUN LOCALLY -- LARG is hosted on AWS

[LARG is here] _ currently down _ 

First we must install the Python package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages for LARG.

If you have [HomeBrew](https://brew.sh/) installed you can use the following to install pip, otherwise make your way to the HomeBrew link:


IN YOUR TERMINAL

```bash
brew install pip
```

Secondly we must create a python virtual environment which will require [python3](https://www.python.org/downloads/):
So go ahead and install python3 as well.

```bash
brew install python3
```

OK ---- so now we have python3 and pip package manager. NEXT we need to create a virtual environment for which to run python in. 

We are using [virtualenv](https://virtualenv.pypa.io/en/latest/)

Using pip:

```bash
pip install virtualenv

virtualenv venv --distribute

python3 -m venv /path/to/venv_name #the environment you want to create

```

Next we navigate to our virtual env and run the following to activate it:

```bash
. bin/activate
```

You should see ![Image of venv](./assets/venv.jpg)

To check your version of python3 to see if it the latest:

```bash
python3 --version
``` 

Lastly for setup we will install the packages necessary for the running of LARG using pip:

```bash
pip install -r /path/to/requirements.txt # should be LR_REPORT_GEN/requirements.txt
```

You should be all setup. Now all there is left to do is execute: 

#### Execution

```bash
python3 /LR_REPORT_GEN/lr_comp_gen.py
```

# LARG CSV GENERATOR 

In the folder LR_CSVs there is a script to take a loadrunner html summary and convert it to a CSV. It then uploads that CSV to AWS and updates the database.

### USAGE

To run all it needs is the path to an LR html summary:

```
python3 LR_html_to_csv.py "path/to/summary" #quotes are necessary
```
This is how  **ALL CSVs** should be uploaded to the database as it relies on the formatting of the name and of the data.





