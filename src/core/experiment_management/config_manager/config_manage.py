from dataclasses import dataclass, field, asdict
from typing import Tuple, Iterable, List
from copy import deepcopy
from datetime import datetime


@dataclass
class ConfigField:

	name: str
	abbr_name: str = field(init=False)
	value: str
	keys: List[str]
	save_mode: str = None
	custom_name: bool = False

	def __post_init__(self):
		if not self.custom_name:
			self.abbr_name = ''.join([item[0] for item in self.name.split("_")])
		else:
			self.abbr_name = self.name

	def __str__(self):
		return self.abbr_name + ":" + str(self.value)


@dataclass
class ExperimentConfig:

	config: dict
	experiment_type: str
	keys: List[str]
	values: tuple
	dir_name: str
	file_name: str


def get_exp_file_name(combination: Tuple, experiment_vars: List[ConfigField]):
	dirs, file_fields = [], []
	for idx in range(len(combination)):
		if experiment_vars[idx].save_mode and experiment_vars[idx].save_mode.startswith('dir'):
			dirs.append((combination[idx], experiment_vars[idx].save_mode))
		else:
			field_name = experiment_vars[idx].abbr_name + '_' + str(combination[idx])
			file_fields.append(field_name)
	dir_name = '/'.join([dir_item[0] for dir_item in sorted(dirs, key=lambda x: x[1])])
	file_name = '@'.join(file_fields) + ".json"

	return dir_name, file_name


def get_exp_config(config_tmpl, combination, experiment_vars: List[ConfigField]):
	# copy config
	config = deepcopy(config_tmpl)
	# update config
	for idx in range(len(combination)):
		keys = experiment_vars[idx].keys
		value = combination[idx]
		update_nested_dict(config, keys, value)

	return config


def update_nested_dict(nested_dict, keys, value):
	# Initialize variable to hold the nested dictionary
	nested = nested_dict

	# Loop through each key in the list and access the corresponding value in the dictionary
	for key in keys[:-1]:
		nested = nested.setdefault(key, {})

	# Update the value
	nested[keys[-1]] = value

	return nested_dict


def load_config_fields_from_dicts(config_dicts: List[dict]):
	config_fields = []
	for config_dict in config_dicts:
		config_field = ConfigField(**config_dict)
		config_fields.append(config_field)

	return config_fields
