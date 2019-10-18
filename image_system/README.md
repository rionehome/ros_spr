# Install
in your root,
```
colcon build --package-select image_system
source install/local_setup.bash
```
then,
```
cd ~/your/workspace/image_system
mkdir model
bash get_npz.bash
```
# Usage
ros2 run image_system image_system

it is success example in execution.
```
[INFO] [DetectHuman]: LOADING POSE MODEL
[INFO] [DetectHuman]: LOADING MODEL
[INFO] [DetectHuman]: DONE

```

# Data flow
![image_system](https://github.com/rionehome/image_system/blob/images/SequenceDiagram.png "image_system")
