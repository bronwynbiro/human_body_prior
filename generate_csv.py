import joblib
import glob
from collections import defaultdict
all_f = glob.glob('*.pkl')

res = []
experiment_num_to_name = {}

for i, pkl_fname in enumerate(all_f):
  output = joblib.load(pkl_fname)
  experiment_num_to_name[i] = pkl_fname
  data_per_frame = {}

  # Get the poses for each body ID
  for body in output.keys():
    frames_per_id = len(output[body]['frame_ids'])
    for frame, pose_data in enumerate(output[body]['pose']):
      # If there's multiple people at a frame, select the one in the most total frames
      if frame not in data_per_frame or frames_per_id > data_per_frame[frame][0]:
        data_per_frame[frame] = [frames_per_id, pose_data]
  
  # Add the poses per frame to dataframe
  for frame, pose_data in sorted(data_per_frame.items()):
    flat_data = [i, frame]
    # Skip the frames per id variable
    for pose in pose_data[1:]:
      flat_data.extend(pose)
      res.append(flat_data)

df = pd.DataFrame(res)

# reset column names
pose_range = [i for i in range(1, 73)]
col_names = ['experiment_num', 'frame_num']
col_names.extend(pose_range)
df.columns = col_names
df.head()

df.to_csv("pkl.csv", index=False)
