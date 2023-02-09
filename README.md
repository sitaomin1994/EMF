# EMF
Experiment Management Framework for Scientific Research

## Introduction

EMF is a framework for managing scientific experiments. It includes functionality for batch experiment management, 
experiment process and results recording, and experiment results visualization.

## Setup

EMF is a template repo in github, so you can use it as a template to create your own repo. Click 'Use this template' button to create repo for your own project.
The environment setup is the same as other python projects. You can use create conda environment by running `conda env create -f environment.yml`.

## Usage

### Design your own experiment
Create your own experiment by inheriting `Experiment` class in `experiment/Experiment.py`. 

### Running Experiments
Run experiments by running `python run_experiments.py`. The results will be saved in `results` folder and `mongodb` backend database.

### Experiment Configuration
Place configuration files in `experiment_configs` folder. The configuration files are in json format. 
The configuration files are used to specify the experiment parameters.

### Management and UI

Direct to ui folder and run `npm install` to install dependencies. Then run `npm start` to start the ui server. You will know see all your running experiments with results in the ui.

### Modules
Modules contain built-in implementations of some commonly used functionalities. You can use them in your own experiments.
The current modules include:
- Data Loading: Load data from file.
- Data Preprocessing: Preprocess data.
- Prediction Model: Train and evaluate prediction models.
- Missing Data Imputation: Impute missing data.
- Plotting: Visualize data and results
- Utils: Common utility functions
  - Reproducibility: Set random seed for reproducibility
  - Stats: Common statistical functions and distributions