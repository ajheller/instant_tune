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
```

To run `silent_tuning.ipynb` in VS Code, select `.venv/bin/python` as the
notebook kernel. JupyterLab is optional and is not included in `requirements.txt`.
For a browser-based notebook interface, install and launch it separately:

```sh
python -m pip install jupyterlab
python -m jupyterlab
```

Run the notebook with the repository root as its working directory so relative
data paths resolve correctly.

## Measurement data

All Touchstone measurements required by `silent_tuning.py` and
`silent_tuning.ipynb` are checked into the repository under `data/`:

- `antennas/Mosley-TA-33-W6SRI.s1p`: antenna measurement.
- `tuners/zmatch/`: 50 forward/reverse sweeps for the 25 tuner settings.
- `vna_calibrations/cal-1-30MHz-505pts.s2p`: calibration measurement loaded by
  the notebook.

These analyses use saved measurements and do not require connected hardware.
The local NanoVNA experiment notebooks are not tracked in Git; running them
requires connected hardware and the correct serial device path.

Leave the environment with `deactivate`.
