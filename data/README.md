# DATASET

The original dataset is not publicly available.

There are two input files: the first format is expected to be a .json, while the second is a .parquet.

The first file must contain data associated to 29 routes; for each route we have:
- Signal of the entire route (signal);
- Speed along the entire route (speed);
- Portion of signal relating to the curvilinear section (signalRett);
- Portion of signal relating to the straight section (signalCur);
- Speed along the curved section (speedRett);
- Speed along the straight stretch (speedCur);
- Indices delimiting the traits (idxRett, idxCur);

The second file provides the mileage of each trait.