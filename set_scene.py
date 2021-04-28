import bpy
import csv
from mathutils import Euler
from collections import defaultdict


root_path = 'YOUR_ROOT_PATH'
video_name = '2019-12-10-15-17-50'


translation = "{}/csvs/{}/vicon_hat_3_hat_3_translation.csv".format(root_path, video_name)
orientation = "{}/csvs/{}/vicon_hat_3_hat_3_orientation.csv".format(root_path, video_name)
timestamps = "{}/csvs/{}/img_raw_03.csv".format(root_path, video_name)

collection = bpy.data.collections['Collection']

def round_to(x, a=0.333):
    return round(round(x/a)*a, 1)

# Seperate the timestamps into frame numbers 
def get_timestamps():
    time_to_frame = defaultdict(int)
    with open(timestamps) as f:
        for i, line in enumerate(f):
            _, time = line.split(",")
            time = round_to(float(time))
            time_to_frame[time] = i + 1
    return time_to_frame
  
# Get the position and orientation for each frame
def get_position(people, times):
    frame_to_data = defaultdict(list)
    with open(translation) as t:
        with open(orientation) as o:
            for trans_line, o_line in zip(t, o):
                time, x, y, z = [float(x) for x in trans_line.split(",")]
                time_o, roll, pitch, yaw = [float(x) for x in o_line.split(",")]
                
                time = round_to(float(time))
                if time in times:
                    frame = times[time]
                    if frame in people:
                        obj = people[frame][0]
                            
                        location = (-x, -y, 0)
                            
                        rotation_euler =  Euler((1.75814, 0, yaw), 'XYZ')
                        frame_to_data[frame] = [location, rotation_euler]
                        
                        
    return frame_to_data
                
# Set the proper location for each mesh
def set_position(frame_to_data, people):
    prev_obj = None
    end = max(frame_to_data.keys())
    
    # Initialize all meshes to hidden
    for frame, obj_lst in people.items():
        obj = obj_lst[0]
        obj.hide_viewport = True
        obj.keyframe_insert(data_path="hide_viewport", frame=1)
    
    for frame in range(end):
        # Set the last obj 
        if prev_obj:
            last_frame = int(prev_obj.name.split("o_")[-1])
            prev_obj.hide_viewport = True
            prev_obj.keyframe_insert(data_path="hide_viewport", frame=last_frame+1)
            bpy.context.scene.frame_set(last_frame+1)
        
        if frame not in people:
            continue
        
        obj = people[frame][0]
        
        # If we have data for this mesh, place it
        if frame in frame_to_data:
            data = frame_to_data[frame]
            obj.location = data[0]
            obj.rotation_euler =  data[-1]
        
        # If missing data, set the same as the last obj's location
        else:
            if prev_obj:
                obj.location = prev_obj.location
                obj.rotation_euler = prev_obj.rotation_euler

        # Set frame location and visibility
        obj.hide_viewport = False
        obj.keyframe_insert(data_path="hide_viewport", frame=frame)
        obj.keyframe_insert(data_path="location", frame=frame)
    
        prev_obj = obj

        # Set the scene
        bpy.context.scene.frame_set(frame)
        
        
    obj = people[end][0]
    obj.hide_viewport = True
    bpy.context.scene.frame_set(end)
       


# Get all the people meshes and assign them to a frame
def get_meshes():
    people = defaultdict(list)
    for obj in collection.all_objects:
        name = obj.name
        
        if name[0] == "o" and "empty" not in name: 
            name = name.split("o_")
            frame = name[-1]
            if frame.isdigit():
                frame = int(frame)
                people[frame] = [obj]
        
    return people

        
def main():
    # Clear all actions
    for a in bpy.data.actions:
        bpy.data.actions.remove(a)

    # Get and set the positions of the meshes
    times = get_timestamps()  
    people = get_meshes()
    positions = get_position(people, times)
    set_position(positions, people)

main()
