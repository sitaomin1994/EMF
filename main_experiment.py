import hydra
from omegaconf import DictConfig, OmegaConf


@hydra.main(version_base=None, config_path="conf/experiment1/", config_name="conf.yaml")
def main(cfg: DictConfig) -> None:
	print(OmegaConf.to_yaml(cfg))


if __name__ == '__main__':
	main()
