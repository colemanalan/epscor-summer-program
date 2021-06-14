#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import numpy as np
import pickle as pkl
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# -- initialize timer
t00 = time.time()

# -- set the file names
hename = "../data/MonteCarlo_Proton.obj"
dename = "../data/DetectorLocations.obj"

# -- read in the data
print("loading event and detector data for {0}...".format(hename))
hedat = pkl.load(open(hename, "rb"))
dedat = pkl.load(open(dename, "rb"))

# -- initialize events array
print("creating event arrays...")
nevent = len(hedat)
ntank = 2 * len(dedat.positions)
evSarr = np.zeros((nevent, ntank), dtype=float)
evTarr = np.zeros((nevent, ntank), dtype=float)
evParr = np.zeros(nevent, dtype=float)

# -- loop through events
for ii in range(nevent):

    if (ii % 100) == 0:
        print("\r  working on event {0} of {1}".format(ii + 1, nevent), end="")

    # -- get tank hits
    tevent = hedat[ii]
    tanks = tevent.keys()

    # -- fill events array
    for tank in tanks:
        col = tank[0] * 2 + tank[1]

        if np.isnan(tevent.tankHits[tank]).any():
            continue

        evSarr[ii, col] = tevent.tankHits[tank][0]
        evTarr[ii, col] = tevent.tankHits[tank][1]

    evParr[ii] = tevent.GetPrimary().energy
print("")

# -- convert to log10 of signal and primary energy
evSarr[evSarr > 0] = np.log10(evSarr[evSarr > 0])
evParr = np.log10(evParr)

# -- alert user
print("  finished in {0:.3f}s".format(time.time() - t00))
print("running Random Forest Regressor model...")
t0 = time.time()

# -- create feat and targ as well as training/testing data
feat = np.hstack([evSarr, evTarr])
targ = evParr
feat_tr, feat_te, targ_tr, targ_te = \
    train_test_split(feat, targ, test_size=0.2, random_state=302)

# -- initialize random forest regressor
rfr = RandomForestRegressor(min_samples_leaf=5)

# -- fit the model
rfr.fit(feat_tr, targ_tr)

# -- get the accuracies
pred_tr = rfr.predict(feat_tr)
pred_te = rfr.predict(feat_te)
r2_tr = r2_score(targ_tr, pred_tr)
r2_te = r2_score(targ_te, pred_te)

print("  R^2 for training set : {0:.3f}".format(r2_tr))
print("  R^2 for testing set  : {0:.3f}".format(r2_te))

# -- alert user
print("  finished in {0:.3f}s".format(time.time() - t0))
