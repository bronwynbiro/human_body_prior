
# Pose Forecasting in the SFU-Store-Nav 3D Virtual Human Platform

This repo contains code to create 3D simulations for the SFU-Store-Nav dataset. The retail scene was re-created in Blender, and the 3D body shape and pose estimations were combined with motion capture data to have virtual humans interact with the scene as in the original experiment.  We also propose an LSTM Variational Autoencoder that learns a latent representation of human pose and regularizes the distribution of the latent code to be a normal distribution. We can then predict future poses given an input sequence. 

This code is built upon [VPoser](https://github.com/nghorbani/human_body_prior), and we use their methods to visualize the SMPL body. 

If you only want to run the pose forecasting, you can skip to that section. Otherwise, the first few steps explain how to gather the data and visualize it in Blender. 

## Gathering the data
Get the original SFU-Store-Nav dataset from [here](https://www.rosielab.ca/datasets/sfu-store-nav). 

## Get SMPL meshes
We use [VIBE](https://github.com/mkocabas/VIBE) to get the SMPL body parameters and meshes. You will need to download the SMPL body from [here](https://smpl.is.tue.mpg.de/). You can use the Colab demo [here](https://colab.research.google.com/drive/1dFfwxZ52MN86FA6uFNypMEdFShd2euQA), but modify it to add the `--save_obj` flag: 

     !python demo.py --vid_file VID_NAME.avi --output_folder OUTPUT_NAME --save_obj

After running, save the corresponding .obj files and the .pkl file.

## Run Blender script
### Importing body meshes to Blender
We use the [Stop Motion Obj](https://github.com/neverhood311/Stop-motion-OBJ) plugin in Blender to import the body meshes. Follow the instructions, then in Blender:
1.  Click File > Import > Mesh Sequence
2.  Navigate to the folder where your mesh sequence is stored
3.  In the File Name box, provide 0
4.  Leave the Cache Mode set to Cached
5.  Click Select Folder and wait while your sequence is loaded
6.  Click the sequence in "Scene Collection"  
7.  Click Context > Object
8.  Click Mesh Sequence > Advanced > Bake sequence

If there were multiple body IDs returned, you will need to repeat for each different ID folder. 

### Set the positions

You will need to put the corresponding .csv files into a folder of the form `YOUR ROOT DIR/csvs/VIDEO_NAME`. Then, set the `root_path` and `video_name`  variables in `set_scene.py` and run it. 

## Pose forecasting

1. Download the SMPL body from [here](https://smpl.is.tue.mpg.de/) and save it under `human_body_prior/smpl/models/neutral.pkl`.  
2. Follow the instructions [here](https://github.com/vchoutas/smplx/blob/f4206853a4746139f61bdcf58571f2cea0cbebad/tools/README.md) to make the pkl file compatible with Python 3. 
3. Download a trained VPoser from the [SMPL-X project website](https://smpl-x.is.tue.mpg.de/). 
4. Change the `torchgometry/core/conversions.py: L302:304` to:
```
mask_c1 = mask_d2 * ~mask_d0_d1
mask_c2 = ~mask_d2 * mask_d0_nd1
mask_c3 = ~mask_d2) * ~mask_d0_nd1
```
5. Run the [pose forecasting notebook](https://github.com/bronwynbiro/human_body_prior/blob/master/Pose_forecasting.ipynb). It is compatible with Colab, but the visualizations require GPU.
