import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.animation as animation
import math
import utm
import time

# Read GPS_data from csv file
gps_data = pd.read_csv("GPS_data/gpsPlus_20230612164330.csv")
# Read LIDAR_data from csv file
lidar_data = pd.read_csv("LIDAR_data/ydlidar_20230612164330.csv")
## Show dataframe of gps and lidar
# print("gps_data= ",gps_data)
# print("\n")
# print(lidar_data.head())


# Setup for GPlidar3 function
# status of animation process (play/pause)
status = True
# Get the number of rows from lidar_data
n = lidar_data.shape[0]
# offset heading angle of polar plot
offset = np.pi/2
# Get array of range of lidar_data
r = lidar_data['lidar_range_meter']
# Get array of angle of lidar
theta = lidar_data['lidar_angle_degree']

# Get Lat Long value from gps_data
Lat = gps_data['gps_recentLatitudeN'].to_numpy()
# print(Lat)
Long = gps_data['gps_recentLongitudeE'].to_numpy()
# Get heading angle from gps_data
theta_offset = gps_data['compass_heading_degs'].to_numpy()
# Convert Lat Long to UTM (X,Y) 
# u[0] is East, X) and u[1] is North, Y
u = utm.from_latlon(Lat, Long)

# Polar Plot lidar_data
# Polar Plot Setting
fig = plt.figure(figsize=(11, 6))
# define axises for Polar Plot
ax1 = plt.subplot(1,2,1, projection='polar')
# define axises for position plot
ax2 = plt.subplot(1,2,2)
# tuple variable for update plot with animation function
line1, = ax1.plot([], [], 'ro', markersize=2)

# variables for update value each frame
xpos, ypos = [], [] # ax2
polar_theta, polar_r   = [], [] # ax1


def Polar_ax_offset(degree_offset): # this function for offset angle in Polar plot
    return (90-degree_offset)*np.pi/180

def GPlidar_plot3(gps_data, lidar_data): # Run animation plot function
    # Setup Button
    axes = plt.axes([0.4, 0.0001, 0.1, 0.075]) # button position
    bpause = Button(axes, 'Play/Pause', color="yellow") # create button
    
    def init():
        # additional setup plot
        ax1.set_title("Radius of obstacles from lidar and \n and robot heading Orientation respect to North", fontsize = 8)
        
        ax2.set_title("Position of robot from GPS")
        ax2.set_xlabel('Position X (m.)')
        ax2.set_ylabel('Position Y (m.)')

    def update(frame): # input is index i of frames in FuncAnimation (This function will be run many times by FuncAnimation)
        # call global variables
        global r, theta, n
        # ax1
        # Convert string to list then Convert to float32 numpy array
        irow_r = np.array(r[frame].strip('][').split(', '), dtype=np.float64)
        # print(irow_r)
        # determine max radius of polar plot for each timestep
        maxr = int(np.max(irow_r))+1
        # set radius limit of polar plot
        ax1.set_rmax(maxr)
        # Convert string to list and Convert float32 numpy array
        irow_theta = np.array(theta[frame].strip('][').split(', '), dtype=np.float64)
        irow_rad = irow_theta*np.pi/180.0
        # additional Polar Plot Setting 
        # set theta_offset with respect to gps_data
        ax1.set_theta_offset(Polar_ax_offset(theta_offset[frame]))
        
        # update variable
        # ax1
        polar_theta = irow_rad
        polar_r = irow_r
        # ax2   
        xpos.append(u[0][frame])
        ypos.append(u[1][frame])
        
        # update line2D
        line1.set_data(polar_theta, polar_r)
        # Position plot
        if frame == 0: # plot ax2 in update function because This axis can't update scale when new data come.
            ax2.plot(xpos, ypos, 'ro', markersize= 9)   # plot initial data as red mark
            
        elif frame == n-1:
            ax2.plot(xpos[frame], ypos[frame], 'ro', markersize= 9) # plot the lastest data as redmark
            
        else:
            ax2.plot(xpos, ypos, 'o',color='green', markersize= 4) # plot data with green mark

        # return value for ax1 plot(polar plot)
        return line1 #
        
    # initial additionadl plot setup
    init()

    # input of update is Line2D or List of Line2D
    # Blitting changes the content of the axes, not the decorators so set it to False
    # print('n = ',n)
    ani = animation.FuncAnimation(fig, update, frames=np.arange(0, n, 1),interval=1000,
                              repeat= False, blit=False) # interval unit is milliseconds, blit is False so the setup of axises can be updated
    
    def pause_ani(event): # fuction which use with pause button
        global status
        if status :
            print('True = ',status)
            ani.pause()
        else:
            ani.resume()
        status = not status # change value of the status variable
        print('out', status)

    # run callback funtion when button is onclick
    bpause.on_clicked(pause_ani)
    # show the plot
    plt.show()
    

# run animation plot function
GPlidar_plot3(gps_data, lidar_data)


