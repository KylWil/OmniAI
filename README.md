# OmniAI

## Description

OmniAI is a training environment for the game DareFightingICE. It offers a Proximal Policy Optimization (PPO) training algorithm, state data CSV exporting, and training data tracking and analysis.

## Getting Started

### External Dependencies

* [DareFightingICE v7.1](https://github.com/TeamFightingICE/FightingICE/releases/tag/v7.1)
* [JDK 21](https://www.oracle.com/java/technologies/downloads/#java21)
* [Python v3.12.13](https://www.python.org/downloads/release/python-31213/)
* [Ubuntu Linux](https://ubuntu.com/download) (This program was written on Ubuntu Linux, it is unknown whether or not it will run on any other Linux distributions or operating systems)

### Python Packages

* numpy v2.5.1
* pandas v3.0.5
* pyftg v2.3
* tensorboard v2.21.0
* torch v2.13.0+rocm7.2 (AMD GPU)
* torchaudio v2.11.0+rocm7.2 (AMD GPU)
* torchvision v0.28.0+rocm7.2 (AMD GPU)
* typer v0.26.8

### Installing

1. Install JDK 21 (Required to run DareFightingICE)
2. Create a virtual environment for Python v3.12.13
3. Install the above Python packages to the virtual environment
4. Download and extract DareFightingICE-7.1.zip
5. Download resource-7.1.zip and move the data folder into ~/DareFightingICE-7.1./FightingICE7.1. The moved data folder should be in the same folder as run-linux-amd64.sh
6. Download OmniAI
7. Move linux-play.sh from the OmniAI repository into the same folder as run-linux-amd64.sh

## Executing program

### Playing the trained AI

1. Open a terminal and navigate to your DareFightingICE folder
2. Run linux-play.sh
3. Open a terminal and navigate to your OmniAI folder
4. Activate your Python v3.12.13 virtual environment
5*. Run "python3 main.py play --randomaction" without the quotes

*Optional tags include:
* --randomaction: Chooses a random action every frame. AI will repeatedly kick otherwise.
* --savedata: Saves a csv of frame-by-frame character data to /OmniAI/reports/ each round.
## Help

## Authors

[@KylWil](https://github.com/KylWil)

## Version History

## License

This project is open source and covered under the MIT open-source license. See LICENSE for more details.

## Acknowledgments

Inspiration, code snippets, etc.
* [FightingICE team from Ritsumeikan University](https://www.ice.ci.ritsumei.ac.jp/~ftgaic/)
* [README-Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
