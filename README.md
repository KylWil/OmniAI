# OmniAI

## Description

OmniAI is a training environment for the game DareFightingICE. It offers a Proximal Policy Optimization (PPO) reinforcement learning (RL) training algorithm, state data CSV exporting, and training data tracking and analysis.

## Getting Started

### External Dependencies

* [DareFightingICE v7.1](https://github.com/TeamFightingICE/FightingICE/releases/tag/v7.1)
* [JDK 21](https://www.oracle.com/java/technologies/downloads/#java21)
* [Python v3.12.13](https://www.python.org/downloads/release/python-31213/)

### Python Packages

* numpy v2.5.4
* pandas v3.1.0
* pyftg v2.3
* tensorboard v2.20.0
* torch (requires specific installation based on hardware)
* typer v0.27.3

### Installing

1. Install JDK 21 (Required to run DareFightingICE)
2. Clone the project repo or download it from [GitHub](https://github.com/KylWil/OmniAI/archive/refs/heads/main.zip)
3. Navigate to the project folder and run the setup script associated with your operating system (setup-windows.bat or setup-linux.sh)

## Executing program

### Training an agent

1. Open a terminal and navigate to the OmniAI project folder
2. Launch the game client located at ~/OmniAI/FightingICE7.1/run-YOUROS-headless(.bat for windows, .sh for linux)
3. Open a terminal and navigate to the OmniAI project folder
4. Ensure the virtual environment is activated. (./.venv/Scripts/activate.ps1 for windows // source .venv/bin/activate for linux)
5. Run the command: python main.py --learn --games x (where x is the desired amount of games to train for)

### Playing an agent

1. Open a terminal and navigate to the OmniAI project folder
2. Launch the game client located at ~/OmniAI/FightingICE7.1/run-YOUROS(.bat for windows, .sh for linux)
3. Open a terminal and navigate to the OmniAI project folder
4. Ensure the virtual environment is activated. (./.venv/Scripts/activate.ps1 for windows // source .venv/bin/activate for linux)
5. Run the command: python main.py --games x (where x is the desired amount of games to play)

\*\*Optional tags include:
* --savedata: Saves a csv of frame-by-frame character data to /OmniAI/reports/ each round
* --deterministic: Tells agent to use strictly best move instead of sampling (EXCLUSIVE WITH --learn)
* --nocuda: Disables GPU utilization

## Help

If the setup scripts fail, you can manually install the following requirements to install the program.

* Install JDK 21
* Setup a Python 3.12 virtual environment in the project folder
* Download DareFightingICE v7.1 and resource v7.1 found in External Dependencies
* Extract DareFightingICE into the project folder
* Extract resource into the DareFightingICE folder
* Modify the launch script in the DareFightingICE folder to include --headless-mode and --input-sync for training
* Install the packages found in the requirements.txt file found in the repo to your virtual environment

Contact me [@KylWil](https://github.com/KylWil) if you have any further questions.

## Authors

[@KylWil](https://github.com/KylWil)

## License

This project is open source and covered under the MIT open-source license. See LICENSE for more details.

## Acknowledgments

Inspiration, code snippets, etc.
* [FightingICE team from Ritsumeikan University](https://www.ice.ci.ritsumei.ac.jp/~ftgaic/)
* [README-Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
