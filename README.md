## How to Run Labs 3 & 4

> Previous lab [Lab 2](https://www.google.com/search?q=https://github.com/Oleksandr-Na-no/Robotics_Lab_2/blob/main/README.md)

### 1\. Prepare the Environment & Update Docker

Open the Docker container from the **[robotics\_lpnu](https://github.com/RybOlya/robotics_lpnu/tree/master)** repository.

> **Note:** Navigate to the `robotics_lpnu/` folder (`cd robotics_lpnu/`) and run:
>
> ```bash
> ./scripts/cmd run
> ```

Since Labs 3 and 4 use TurtleBot3, you need to install its packages inside the container (if not already built into your Docker image):

```bash
sudo apt update && sudo apt install -y ros-jazzy-turtlebot3 ros-jazzy-turtlebot3-simulations
```

-----

### 2\. Setup Files and Build the Workspace

**Important:** Before launching, make sure to copy your `robot.sdf` from previous labs to the `worlds` folder.

Inside the container, build the packages for both labs:

```bash
source /opt/ros/jazzy/setup.bash
cd /opt/ws
colcon build --packages-select lab3 lab4
source install/setup.bash
```

> ⚠️ Rebuild every time you change `package.xml`, `setup.py`, launch files, or add/edit python scripts (like `figure_8_path.py` or `dead_reckoning.py`).

-----

### 3\. Running Lab 3: Moving Mobile Robots

You will test path nodes on either the Custom 4-wheel robot or TurtleBot3.

**Terminal 1 (Launch Simulation & RViz2):**
Choose ONE of the following to launch:

```bash
# Option A: Custom 4-wheel robot
cd /opt/ws
source install/setup.bash
ros2 launch lab3 bringup.launch.py

# Option B: TurtleBot3 in 8x8m room
cd /opt/ws
source install/setup.bash
ros2 launch lab3 turtlebot3_room_bringup.launch.py
```

**Terminal 2 (Run Robot Controller):**
Run the desired path script. (Make sure you have implemented `figure_8_path.py` as per the task).

```bash
cd /opt/ws
source install/setup.bash

# Run Square (default or with parameters):
ros2 run lab3 square_path
ros2 run lab3 square_path --ros-args -p side_length:=2.5 -p odom_topic:=/odom

# OR Run Circle:
ros2 run lab3 circle_path

# OR Run Figure-8 (Student Task):
ros2 run lab3 figure_8_path
```

✅ The robot should start moving, and RViz2 will show the trajectory on `/path` (Ensure Fixed Frame is set to `odom`).

-----

### 4\. Running Lab 4: Dead Reckoning

Ensure you have implemented the missing logic in `lab4/dead_reckoning.py` before running.

**Terminal 1 (Launch Dead Reckoning & TurtleBot3):**

```bash
cd /opt/ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch lab4 dead_reckoning_bringup.launch.py
```

**Terminal 2 (Run Trajectory):**

```bash
cd /opt/ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run lab3 circle_path
```

✅ **You should see:** RViz displaying two paths—the odom (ground truth) and your calculated dead reckoning path. The terminal will log the error/drift.
