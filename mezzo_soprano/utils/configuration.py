from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from omegaconf import OmegaConf
from omegaconf.dictconfig import DictConfig
from rich.tree import Tree

# Path to configuration

_config_path = Path("~/.config/mezzo_soprano/").expanduser()

_config_name = Path("mezzo_soprano_config.yml")

_config_file = _config_path / _config_name

# Define structure of configuration with dataclasses


@dataclass
class Logging:

    on: bool = True
    level: str = "WARNING"


@dataclass
class Model:

    leptonic_model: str = "lepto_ml_fuck"
    hadronic_model: str = "hadronic_ml_fuck"
    neutrino_model: str = "hadronic_nu_ml_fuck"


@dataclass
class mezzo_sopranoConfig:

    logging: Logging = Logging()
    model: Model = Model()


# Read the default config
mezzo_soprano_config: mezzo_sopranoConfig = OmegaConf.structured(
    mezzo_sopranoConfig
)

# Merge with local config if it exists
if _config_file.is_file():

    _local_config = OmegaConf.load(_config_file)

    mezzo_soprano_config: mezzo_sopranoConfig = OmegaConf.merge(
        mezzo_soprano_config, _local_config
    )

# Write defaults if not
else:

    # Make directory if needed
    _config_path.mkdir(parents=True, exist_ok=True)

    with _config_file.open("w") as f:

        OmegaConf.save(config=mezzo_soprano_config, f=f.name)


def recurse_dict(d, tree) -> None:

    for k, v in d.items():

        if (type(v) == dict) or isinstance(v, DictConfig):

            branch = tree.add(
                k, guide_style="bold medium_orchid", style="bold medium_orchid"
            )

            recurse_dict(v, branch)

        else:

            tree.add(
                f"{k}: [blink cornflower_blue]{v}",
                guide_style="medium_spring_green",
                style="medium_spring_green",
            )

    return


def show_configuration() -> None:

    tree = Tree(
        "config", guide_style="bold medium_orchid", style="bold medium_orchid"
    )

    recurse_dict(mezzo_soprano_config, tree)

    return tree
