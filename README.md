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

## Executing program

### Playing the trained AI

1. Navigate to your DareFightingICE folder and run the .sh file associated with your operating system, i.e. "run-linux-amd64.sh"
2. Navigate the terminal to your OmniAI folder
3. Activate your Python v3.12.13 virtual environment in a terminal
4. Run "python3 main.py play --a1 OmniAI" without the quotes
5. Return to the DareFightingICE window and navigate to "FIGHT" using the arrow keys and select it with "Z"
6. Using the arrow keys, ensure Player 1 is set to OmniAI, Player 2 is set to MctsAi23i**, and Character 1 is set to GARNET.
7. Select PLAY to begin the match.

\*\* Advanced users can select different AI by utilizing different launch parameters.

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