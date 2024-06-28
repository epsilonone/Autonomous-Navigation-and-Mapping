#!/usr/bin/env python3
import rospy
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
import time

def move_cubes():
    rospy.init_node('move_cubes', anonymous=True)
    rospy.wait_for_service('/gazebo/set_model_state')
    set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
    
    rate = rospy.Rate(50)  # 50 Hz
    
    # Define model names and initial positions
    model_names = ['box1', 'box2', 'box3', 'box4', 'box5',
                   'box6', 'box7', 'box8', 'box9', 'box10']
    
    initial_positions_x = [0.019344984088539116, 6.468471475318647, 12.616070551621, 18.17468731275332, 22.88440701692387,
                           26.525008405243137, 28.926261003031104, 29.975884907615814, 29.624800871792065, 27.889425194873088]
    initial_positions_y = [0.00018805105307251324, 0.701449216353101, 2.77268684610263, 6.1170521707498615, 10.578166384709377,
                           15.94743274550876, 21.973790325627995, 28.37545334243607, 34.85308714820447, 41.10380478554836]
    
    model_states = []
    for i in range(10):
        model_state = ModelState()
        model_state.model_name = model_names[i]
        model_state.reference_frame = 'world'
        model_state.pose.position.x = initial_positions_x[i]
        model_state.pose.position.y = initial_positions_y[i]
        model_state.pose.position.z = -19  # Initial z position
        model_states.append(model_state)
    
    # Set initial velocities and directions
    velocities = [-2.0] * 10  # 1 m/s downwards for all models
    directions = [1] * 10  # All start by moving downwards
    
    start_time = time.time()
    thresh = 2 # control x-threshold

    while not rospy.is_shutdown():
        current_time = time.time()
        elapsed_time = current_time - start_time
        start_time = current_time

        for i in range(10):
            # Update z position for each model
            model_states[i].pose.position.z += velocities[i] * elapsed_time * directions[i]
            model_states[i].pose.position.x += velocities[i] * elapsed_time * directions[i]

            # Check boundaries and reverse direction if needed
            if model_states[i].pose.position.z <= -24:
                model_states[i].pose.position.z = -24
                directions[i] = -1  # start moving downwards
            elif model_states[i].pose.position.z >= -14:
                model_states[i].pose.position.z = -14
                directions[i] = 1  # start moving upwards

            # Check boundaries and reverse direction if needed for x
            if model_states[i].pose.position.x <= initial_positions_x[i] - thresh:
                model_states[i].pose.position.x = initial_positions_x[i] - thresh
                # directions[i] = -1  # start moving downwards
            elif model_states[i].pose.position.x >= initial_positions_x[i] + thresh:
                model_states[i].pose.position.x = initial_positions_x[i] +thresh
                # directions[i] = 1  # start moving upwards
        
        # Call service to update all models' states
        try:
            for i in range(10):
                set_model_state(model_states[i])
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed: {e}")
        
        start_time = current_time
        rate.sleep()

if __name__ == '__main__':
    try:
        move_cubes()
    except rospy.ROSInterruptException:
        pass

