# ISS-Hubble Conjunction Analysis

## What This Does
Tracks two satellites (ISS and Hubble) and finds when they get closest to each other.

## How It Works
1. **Loads TLE data** — current orbital information for both satellites
2. **Propagates orbits** — calculates positions every 60 seconds for 48 hours using SGP4 math
3. **Calculates distance** — measures how far apart the satellites are at each moment
4. **Finds closest approach** — identifies the time and distance of closest encounter
5. **Visualizes results** — shows distance over time (2D) and orbits in 3D space

## Requirements
- Python 3.10
- Orekit (orbital mechanics library)
- NumPy, Matplotlib
- orekit-data.zip (reference data file)

## Installation
```bash
conda create -n orekit-env python=3.10
conda activate orekit-env
conda install -c conda-forge orekit numpy matplotlib
```

## Running
```bash
python conjunction.py
```

## Output
- **Console:** Closest approach distance and time
- **2D Plot:** Distance between satellites over 48 hours
- **3D Plot:** Both orbits around Earth, showing closest approach point
  <img width="1500" height="600" alt="Conjunction_analysis" src="https://github.com/user-attachments/assets/46dcb995-0274-4426-8aec-48321402c2e0" />


## Important Notes
- Uses SGP4 propagation (standard for TLE-based analysis)
- Step size: 60 seconds
- Accuracy: ±1-2 km (typical for TLE data)
- For higher precision, numerical propagation with force models would be needed

## Author
Akash K
