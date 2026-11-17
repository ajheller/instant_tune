# instant_tune

Predict antenna matching from measured Z-match tuner networks using scikit-rf.

## Setup

From the repository directory:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

With the environment activated:

```sh
python silent_tuning.py
# Or open the notebooks:
python -m jupyterlab
```

In an editor, select `.venv/bin/python` as the notebook kernel/interpreter.
Launch Jupyter from the repository root so relative data paths resolve correctly.
The scripts require local Touchstone measurements under `data/`, which are
currently not tracked in Git. The NanoVNA experiment notebooks also require
connected hardware and the correct serial device path.

Leave the environment with `deactivate`.
