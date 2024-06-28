# Dynamic Obstacles

This package creates and adds dynamic obstacles into the Gazebo simulation environment for autonomous navigation and mapping.

## Installation

### Step 1: Clone the Package

Clone the package into the `src` directory of your Catkin workspace:

```bash
cd ~/catkin_ws/src
git clone https://github.com/epsilonone/Autonomous-Navigation-and-Mapping.git
```

### Step 2: Rebuild workspace

Rebuild your Catkin workspace or specifically rebuild the dynamic package:

```bash
cd ~/catkin_ws
catkin build
```
Or rebuild specific package

```bash
catkin build dynamic
```
## Usage

### Step 3: Launch Gazebo World

Launch the Gazebo world with ocean waves:

```bash
roslaunch uuv_gazebo_worlds ocean_waves.launch
```

### Step 4: Launch dynamic obstacles

Launch the dynamic obstacles:

```bash
roslaunch dynamic obstacles.launch
```









