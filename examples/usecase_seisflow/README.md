# Simpy workflow with EnTK

## Requirements (local machine)

* python >= 2.7 (< 3.0)
* python-pip
* python-virtualenv
* git
* all dependencies of specfem_mockup are met

## Installation

* The instructions in this document are relative to $HOME, feel free to pick your own data locations.

* You will first need to create a virtual environment. This is to avoid conflict between packages required for this example and local system packages. 

```bash
virtualenv $HOME/myenv
source $HOME/myenv/bin/activate
```

* You now need to install specific branches of [radical.pilot](https://github.com/radical-cybertools/radical.pilot) and [radical.ensemblemd](https://github.com/radical-cybertools/radical.ensemblemd). Some of the features required for this project are in the development branch and would be released soon.


Radical pilot installation:

```bash
cd $HOME
git clone https://github.com/radical-cybertools/radical.pilot.git
cd radical.pilot
git checkout usecase/vivek
pip install .
```

Ensemble toolkit installation:

```bash
cd $HOME
git clone https://github.com/radical-cybertools/radical.ensemblemd.git
cd radical.ensemblemd
git checkout usecase/seisflow
pip install .
```

## Executing the example (local execution only now)

```bash
cd $HOME
cd radical.ensemblemd/examples/usecase_adap_sampling
RADICAL_ENTK_VERBOSE=info python runme.py
```

## Looking at the output

The output is produced in ```$HOME/radical.pilot.sandbox```. Check the last folder created in this 
directory starting with ```rp.session.*```. There exist folders named ```unit.00*``` representing each task. The folder contains the actual commands executed in a shell script, standard error, standard output and any input, intermediate and output data of the executed task.