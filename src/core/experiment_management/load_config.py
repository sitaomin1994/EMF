from config import ROOT_DIR, settings
import os
import json
from datetime import datetime
import itertools
from dataclasses import dataclass, field, asdict
from .config_manager.config_manage import (
	get_exp_file_name, get_exp_config, ExperimentConfig,
	load_config_fields_from_dicts,
)
from hashlib import md5


def load_configs_raw(config_file: str):

	config_dir = os.path.join(ROOT_DIR, settings['experiment_config_dir'])
	with open(os.path.join(config_dir + "\{}".format(config_file))) as f:
		config = json.load(f)

	experiment_name = config['experiment_name']
	config_tmpl = config['config_tmpl']
	vars_config = config['vars_config']
	experiment_vars = load_config_fields_from_dicts(vars_config)

	# Experiment ID
	# --------------------------------------------------------------------------------------------
	exp_id = md5("{}{}".format(experiment_name, str(datetime.now().strftime("%m%d%H"))).encode()).hexdigest()

	# Experiment Configs
	# --------------------------------------------------------------------------------------------
	# generate all combinations
	vars_values = [item.value for item in experiment_vars]
	combinations = list(
		itertools.product(*vars_values)
	)

	# generate configs and corresponding file names
	exp_configs = []
	for combination in combinations:
		# copy config
		config = get_exp_config(config_tmpl, combination, experiment_vars)

		# generate file and dir names
		dir_name, file_name = get_exp_file_name(combination, experiment_vars)
		dir_name = "{}/{}".format(experiment_name, datetime.now().strftime("%m%d")) + "/" + dir_name

		# append to exp_configs
		exp_config = ExperimentConfig(
			config=config, experiment_type=experiment_name, dir_name=dir_name,
			file_name=file_name, values=combination, keys=[item.abbr_name for item in experiment_vars]
		)
		exp_configs.append(exp_config)

	# Experiment Meta
	# --------------------------------------------------------------------------------------------
	exp_meta = {
		"exp_id": exp_id,
		"exp_name": experiment_name,
		"dir_name": "{}/{}".format(experiment_name, datetime.now().strftime("%m%d")),
		"filename": "experiment_meta@{}.json".format(datetime.now().strftime("%m%d%H%M")),
		"type": "meta",
		"date": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
		"variations": [asdict(item) for item in experiment_vars],
		"config_tmpl": config_tmpl
	}

	return exp_configs, exp_meta
