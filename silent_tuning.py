#
# Silent Tuning in Python/scikit-rf
#  Aaron Heller <ajheller@gmail.com>
#  17-Jan-2025
#


# %%
from pathlib import Path

import numpy as np
import skrf as rf
from matplotlib import pyplot as plt

# %%
_here = Path(__file__).resolve().parent
data_files = _here / "data"

# project_files = Path("/Users/heller/dev/instant_tune/")
tuner_files = data_files / "tuners" / "zmatch"
antenna_files = data_files / "antennas"
calib_files = data_files / "vna_calibration"

# %%
# load the antenna
ant = rf.Network(antenna_files / "Mosley-TA-33-W6SRI.s1p")

# plot the return loss of the antenna
fig, ax = plt.subplots(1, 1, figsize=(6, 6))
ant.plot_s_db(ax=ax)
ax.grid(True)
ax.set_title("Return loss TA-33 antenna vs. Frequency")


# %%
# Z-match settings used for calibration
Ls = (1, 3, 5, 7, 9)
Ts = (1, 3, 5, 7, 9)

# set up big plot
fig, axes = plt.subplots(len(Ls), len(Ts), figsize=(30, 30))

# iterate over settings
for li, l in enumerate(Ls):
    for ti, t in enumerate(Ts):

        # load the forward and reverse s2p sweeps
        zm_f, zm_r = [
            rf.Network(tuner_files / f"zmatch-L{l}-T{t}-{dir}.s2p")
            for dir in ("F", "R")
        ]

        # merge into a single two-port network
        tuner = rf.network.four_oneports_2_twoport(
            s11=zm_f.s11, s12=zm_r.s21, s21=zm_f.s21, s22=zm_r.s11
        )

        # cascade the tuner and antenna networks
        tuner_ant = tuner**ant

        # plot return loss of the combined network
        ax = axes[li, ti]
        tuner_ant.plot_s_db(ax=ax)
        ax.set_title(f"L={l} T={t}")
        ax.grid(True)
        ax.set_ylim((-30, +5))

plt.show()


# %%
