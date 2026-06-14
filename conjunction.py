#Initializing orekit    
import orekit
vm = orekit.initVM()

from orekit.pyhelpers import setup_orekit_curdir 
setup_orekit_curdir()

from org.orekit.time import TimeScalesFactory , AbsoluteDate
from org.orekit.propagation.analytical.tle import TLE, TLEPropagator
import matplotlib.pyplot as plt
import numpy as np

#International space station
ISS_tle_1 = "1 25544U 98067A   26149.48556289  .00013329  00000+0  24549-3 0  9993"             
ISS_tle_2 = "2 25544  51.6334  32.6833 0007323 111.1510 249.0262 15.49469300568852"
ISStle = TLE(ISS_tle_1, ISS_tle_2)

#Hubble space telescope 
hub_tle_1 = "1 20580U 90037B   26149.49594231  .00007031  00000+0  22368-3 0  9997"
hub_tle_2 = "2 20580  28.4725 208.3008 0001387 305.7435  54.3032 15.30537421785707"
hubtle = TLE(hub_tle_1,hub_tle_2)

#Propagate both ISS and HUBBLE
ISS_propagator = TLEPropagator.selectExtrapolator(ISStle)
hub_propagator = TLEPropagator.selectExtrapolator(hubtle)

#Getting Time
utc = TimeScalesFactory.getUTC()
start_time = AbsoluteDate(2026, 5, 29, 6, 59, 59.0, utc)
start_date = start_time
end_time = start_time.shiftedBy(48.0 * 60.0 * 60.0)

#3D Positions
iss_positions = []
hub_positions = []

#Storing Dist. and Time
dist = []
time = []

while (start_time.compareTo(end_time) <= 0.0):

    iss_state = ISS_propagator.propagate(start_time)
    hub_state = hub_propagator.propagate(start_time)

    iss_pos = iss_state.getPVCoordinates().getPosition()
    hub_pos = hub_state.getPVCoordinates().getPosition()

    iss_positions.append([iss_pos.getX(), iss_pos.getY(), iss_pos.getZ()])
    hub_positions.append([hub_pos.getX(), hub_pos.getY(), hub_pos.getZ()])

    #distance = iss_pos.distance(hub_pos)
    distance = np.sqrt(((iss_pos.getX() - hub_pos.getX()) ** 2) + 
                       ((iss_pos.getY() - hub_pos.getY()) ** 2) +
                       ((iss_pos.getZ() - hub_pos.getZ()) ** 2))
    dist.append(distance)

    elapsed_time = start_time.durationFrom(start_date) / 3600 
    time.append(elapsed_time)    
    
    start_time = start_time.shiftedBy(60.0)

#getting the closest approach point
min_dist = min(dist)
min_index = dist.index(min_dist)
closest_time = time[min_index]

coarse_seconds = min_index * 60.0
coarse_date = start_date.shiftedBy(coarse_seconds)

print(f"Closest Approach: {min_dist/1000 : .2f} km at hour {closest_time : .2f}"
      "\n" f"On {coarse_date}")

# Fine search

fine_search = 10 * 60.0 
fine_start = coarse_date.shiftedBy(-fine_search)
fine_end = coarse_date.shiftedBy(fine_search)

print(f"\nFine search window: {fine_start} to {fine_end}")

fine_dist = []
fine_time = []
finesearchtime = fine_start

while finesearchtime.compareTo(fine_end)<= 0.0:
    iss_state = ISS_propagator.propagate(finesearchtime)
    hub_state = hub_propagator.propagate(finesearchtime)

    iss_pos = iss_state.getPVCoordinates().getPosition()
    hub_pos = hub_state.getPVCoordinates().getPosition()

    fine_distance = iss_pos.distance(hub_pos)
    fine_dist.append(fine_distance)
    fine_time.append(finesearchtime.durationFrom(start_date) / 3600.0 )

    finesearchtime = finesearchtime.shiftedBy(0.1)

#finding refined minimum
refined_min_dist = min(fine_dist)
refined_min_index = fine_dist.index(refined_min_dist) 
refined_coarse_date = fine_start.shiftedBy(refined_min_index * 0.1)

print(f"\nRefined TCA: {refined_coarse_date}")
print(f"Refined minimum distance: {refined_min_dist/1000:.3f} km")
print(f"Improvement: {(min_dist - refined_min_dist)/1000:.3f} km more accurate")


# Convert lists to numpy arrays for easier slicing andd plotting
iss_pos_array = np.array(iss_positions) / 1000.0
hub_pos_array = np.array(hub_positions) / 1000.0
dist_km = [d / 1000 for d in dist]

# Single figure with side-by-side 2D and 3D subplots
fig = plt.figure(figsize=(15, 6))

# Left Plot: 2D Distance over Time
plot1 = fig.add_subplot(1, 2, 1)
plot1.plot(time, dist_km, linewidth=2, color='blue')
plot1.set_xlabel('Time (Hrs)')
plot1.set_ylabel("Distance (km)")
plot1.set_title("ISS - Hubble Conjunction Analysis")
plot1.axvline(closest_time, color='red', linestyle='--', label=f'Closest: {min_dist/1000:.2f} km')
plot1.grid(True)
plot1.legend()

# Plot Earth as a sphere
plot2 = fig.add_subplot(1, 2, 2, projection='3d')
plot2.scatter([0], [0], [0], s=1000, c='blue', label='Earth')

# Plot orbits
plot2.plot(iss_pos_array[:, 0], iss_pos_array[:, 1], iss_pos_array[:, 2], 'b-', linewidth=0.3, label='ISS Orbit')
plot2.plot(hub_pos_array[:, 0], hub_pos_array[:, 1], hub_pos_array[:, 2], 'r-', linewidth=0.3, label='Hubble Orbit')

# Plot closest approach point
closest_iss = iss_pos_array[min_index]
plot2.scatter(*closest_iss, s=300, c='green', marker='*', label='Closest Approach')

#labelling the plot
plot2.set_xlabel('X (km)')
plot2.set_ylabel('Y (km)')
plot2.set_zlabel('Z (km)')
plot2.set_title('3D Conjunction Visualization: ISS vs Hubble')
plot2.legend(loc = 'upper left', fontsize=8, markerscale = 0.3)

# Set equal aspect ratio for 3D plot to avoid distortion
max_range = np.array([iss_pos_array[:, 0].max()-iss_pos_array[:, 0].min(), 
                      iss_pos_array[:, 1].max()-iss_pos_array[:, 1].min(), 
                      iss_pos_array[:, 2].max()-iss_pos_array[:, 2].min()]).max() / 2.0

mid_x = (iss_pos_array[:, 0].max()+iss_pos_array[:, 0].min()) * 0.5
mid_y = (iss_pos_array[:, 1].max()+iss_pos_array[:, 1].min()) * 0.5
mid_z = (iss_pos_array[:, 2].max()+iss_pos_array[:, 2].min()) * 0.5

plot2.set_xlim(mid_x - max_range, mid_x + max_range)
plot2.set_ylim(mid_y - max_range, mid_y + max_range)
plot2.set_zlim(mid_z - max_range, mid_z + max_range)


plt.tight_layout()
plt.show()