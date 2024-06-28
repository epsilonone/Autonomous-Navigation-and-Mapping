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
    
    model_state1 = ModelState()
    model_state1.model_name = 'box1'  # name of the first box model
    model_state1.reference_frame = 'world'
    model_state1.pose.position.x = 0.019344984088539116
    model_state1.pose.position.y = 0.00018805105307251324

    model_state2 = ModelState()
    model_state2.model_name = 'box2'  # name of the second box model
    model_state2.reference_frame = 'world'
    model_state2.pose.position.x = 6.468471475318647
    model_state2.pose.position.y = 0.701449216353101

    # print(model_state1)
    # print(model_state2)

    z_position1 = -14
    velocity1 = -2.0  # 1 m/s downwards
    direction1 = 1
    
    # z_position2 = 5.0
    # velocity2 = -1.0  # 1 m/s downwards
    # direction2 = -1
    
    start_time = time.time()

    while not rospy.is_shutdown():
        current_time = time.time()
        elapsed_time = current_time - start_time
        start_time = current_time

        # Update position for box1
        z_position1 += velocity1 * elapsed_time * direction1
        if z_position1 <= -24:
            z_position1 = -24
            direction1 = -1  # start moving upwards
        elif z_position1 >= -14:
            z_position1 = -14
            direction1 = 1  # start moving downwards
        model_state1.pose.position.z = z_position1
        model_state2.pose.position.z = z_position1
        
        # Update position for box2
        # z_position2 += velocity2 * elapsed_time * direction2
        # if z_position2 <= 0:
        #     z_position2 = 0
        #     direction2 = 1  # start moving upwards
        # elif z_position2 >= 5:
        #     z_position2 = 5
        #     direction2 = -1  # start moving downwards
        # model_state2.pose.position.z = z_position2
        
        # Call service to update both models' states
        try:
            set_model_state(model_state1)
            set_model_state(model_state2)
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed: {e}")
        
        start_time = current_time
        rate.sleep()

if __name__ == '__main__':
    try:
        move_cubes()
    except rospy.ROSInterruptException:
        pass

