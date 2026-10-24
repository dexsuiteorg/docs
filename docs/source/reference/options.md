# Options

<p class="ds-lede">Every option class that <code>ds.make</code> accepts, field by field, generated from
<code>dexsuite/options/</code>. Import them from <code>dexsuite</code>.</p>

```python
import dexsuite as ds

ds.make("lift", robot=ds.RobotOptions(...), cameras=ds.CamerasOptions(...), sim=ds.SimOptions(...))
```

(simoptions)=
## SimOptions

User-configurable simulation parameters.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `control_hz` | `int` | `20` | The frequency (in Hz) at which control actions are applied. |
| `performance_mode` | `bool` | `False` | A flag to enable or disable performance-optimizing settings within the simulation. |
| `n_envs` | `int` | `1` | Number of parallel copies of the scene. |
| `physics_substeps` | `int \| None` | `None` | Override the task's integration substeps, preserving its physical timestep and the control frequency; None uses task defaults. |
| `precision` | `str` | `'32'` | Genesis floating-point precision, fixed for the process. |

(robotoptions)=
## RobotOptions

The complete robot configuration for an environment.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `type_of_robot` | `Literal['single', 'bimanual']` | `'single'` | The robot configuration type, either 'single' or 'bimanual'. |
| `single` | `ArmOptions \| None` | `None` | The configuration for a single-arm robot. |
| `left` | `ArmOptions \| None` | `None` | The configuration for the left arm of a bimanual robot. |
| `right` | `ArmOptions \| None` | `None` | The configuration for the right arm of a bimanual robot. |
| `layout` | `LayoutOptions` | `LayoutOptions()` | The placement options for the robot(s) in the world. |
| `visualize_tcp` | `bool` | `False` | If True, renders a visual marker for the Tool Center Point (TCP). |
| `visualize_aabb` | `bool` | `False` | If True, renders a visual marker for the workspace bounding box (AABB). |

(armoptions)=
## ArmOptions

Specifications for a single robotic arm, including its gripper and controllers.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `manipulator` | `str` | `"franka"` | The registered name of the manipulator model. |
| `gripper` | `str \| None` | `"robotiq"` | The registered name of the gripper model, if applicable. |
| `manipulator_controller` | `ControllerOptions` | `ControllerOptions("osc_pose")` | The controller configuration for the arm. |
| `gripper_controller` | `ControllerOptions \| None` | `ControllerOptions("joint_position")` | The controller configuration for the gripper. |
| `workspace` | `AABBOptions \| None` | `None` | An optional AABB defining the robot's operational workspace. |

(controlleroptions)=
## ControllerOptions

Specifications for a controller and its configuration.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `name` | `str` | `required` | The name of the controller, which must be registered in the controller registry. |
| `config` | `dict[str, Any]` | `dict()` | A dictionary of parameters to be passed to the controller's __init__ method during instantiation. |

(aabboptions)=
## AABBOptions

An axis-aligned bounding box (AABB) in the arm's base frame.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `min` | `Vec3` | `(0.0, 0.0, 0.0)` | The (x, y, z) coordinates of the minimum corner of the box. |
| `max` | `Vec3` | `(1.0, 1.0, 1.0)` | The (x, y, z) coordinates of the maximum corner of the box. |

(layoutoptions)=
## LayoutOptions

Define the placement of robots in the environment.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `preset` | `str \| None` | `None` | The name of a layout preset for bimanual setups, found in the configuration files. |
| `params` | `dict[str, object]` | `dict()` | A dictionary of additional parameters for the layout. |
| `single` | `PoseOptions \| None` | `None` | The explicit pose for a single-arm setup. |
| `left` | `PoseOptions \| None` | `None` | The pose for the left arm in a bimanual setup (resolved from preset). |
| `right` | `PoseOptions \| None` | `None` | The pose for the right arm in a bimanual setup (resolved from preset). |

(poseoptions)=
## PoseOptions

Represent a 6-DoF pose in the world frame.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `pos` | `Vec3` | `(0.0, 0.0, 0.0)` | The (x, y, z) position. |
| `yaw_rad` | `float` | `0.0` | The rotation around the z-axis in radians. |
| `quat` | `Quat \| None` | `None` | The (w, x, y, z) orientation as a quaternion. |

(camerasoptions)=
## CamerasOptions

Configuration for all cameras and rendering modalities in the environment.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `static` | `dict[str, StaticCamOptions \| str]` | `{'front': 'front'}()` | A dictionary mapping camera names to StaticCamOptions or preset string keys. Defaults to a single 'front' camera. |
| `dynamic` | `dict[str, DynamicCamOptions \| str]` | `{'wrist': 'wrist_cam'}()` | A dictionary mapping camera names to DynamicCamOptions or preset string keys. Defaults to a single 'wrist' camera. |
| `modalities` | `tuple[str, ...]` | `('rgb',)` | A tuple of rendering modalities (e.g., 'rgb', 'depth') to generate for all cameras. 'rgb' is required. |

(staticcamoptions)=
## StaticCamOptions

Define a fixed camera in world coordinates.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `pos` | `Vec3` | `required` | The (x, y, z) position of the camera in the world frame. |
| `lookat` | `Vec3` | `required` | The (x, y, z) point in the world frame the camera looks at. |
| `fov` | `float` | `55.0` | The vertical field of view in degrees. Must be between 0 and 180. |
| `res` | `ResHW` | `(224, 224)` | The (width, height) resolution of the camera image in pixels. |
| `gui` | `bool` | `False` | Whether Genesis should create a GUI visualization for this camera. |
| `near` | `float` | `0.1` | Rendering near clipping distance in metres (not sensor minimum range). |
| `far` | `float` | `20.0` | Rendering far clipping distance in metres. |

(dynamiccamoptions)=
## DynamicCamOptions

Define a camera that is attached to a robot link.

| Field | Type | Default | Meaning |
|---|---|---|---|
| `link` | `str \| None` | `None` | The name of the robot link to attach the camera to. |
| `pos_offset` | `Vec3` | `(0.0, 0.0, 0.0)` | The (x, y, z) position offset relative to the link's frame. |
| `quat_offset` | `Quat` | `(1.0, 0.0, 0.0, 0.0)` | The (w, x, y, z) orientation offset (quaternion) relative to the link's frame. |
| `fov` | `float` | `60.0` | The vertical field of view in degrees. Must be between 0 and 180. |
| `res` | `ResHW` | `(224, 224)` | The (width, height) resolution of the camera image in pixels. |
| `gui` | `bool` | `False` | Whether Genesis should create a GUI visualization for this camera. |
| `near` | `float` | `0.1` | Rendering near clipping distance in metres (not sensor minimum range). |
| `far` | `float` | `20.0` | Rendering far clipping distance in metres. |
