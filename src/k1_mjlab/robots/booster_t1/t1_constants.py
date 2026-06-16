"""Booster T1 constants."""

from pathlib import Path

import mujoco
from mjlab.actuator import BuiltinPositionActuatorCfg
from mjlab.entity import EntityArticulationInfoCfg, EntityCfg
from mjlab.utils.os import update_assets
from mjlab.utils.spec_config import CollisionCfg

##
# MJCF and assets.
##

T1_XML: Path = Path(__file__).parent / "xmls" / "t1.xml"

assert T1_XML.exists(), f"T1 robot XML not found at {T1_XML}"


def get_assets(meshdir: str) -> dict[str, bytes]:
    assets: dict[str, bytes] = {}
    update_assets(assets, T1_XML.parent / "assets", meshdir)
    return assets


def get_spec() -> mujoco.MjSpec:
    spec = mujoco.MjSpec.from_file(str(T1_XML))
    spec.assets = get_assets(spec.meshdir)
    return spec


##
# Keyframe config.
##

INIT_STATE = EntityCfg.InitialStateCfg(
    pos=(0, 0, 0.72),
    joint_pos={
        "Left_Shoulder_Roll": -1.4,
        "Left_Elbow_Yaw": -0.4,
        "Right_Shoulder_Roll": 1.4,
        "Right_Elbow_Yaw": 0.4,
        "Left_Hip_Pitch": -0.2,
        "Left_Knee_Pitch": 0.4,
        "Left_Ankle_Pitch": -0.2,
        "Right_Hip_Pitch": -0.2,
        "Right_Knee_Pitch": 0.4,
        "Right_Ankle_Pitch": -0.2,
    },
    joint_vel={".*": 0.0},
)

##
# Collision config.
##

_foot_regex = r"^(left|right)_foot_collision$"


# This enables all collisions, including self collisions.
# Self-collisions are given condim=1 while foot collisions are given condim=3.
FULL_COLLISION = CollisionCfg(
    geom_names_expr=[".*_collision"],
    condim={_foot_regex: 3, ".*_collision": 1},
    priority={_foot_regex: 1},
    friction={_foot_regex: (0.6,)},
)

FULL_COLLISION_WITHOUT_SELF = CollisionCfg(
    geom_names_expr=[".*_collision"],
    contype=0,
    conaffinity=0,
    condim={_foot_regex: 3, ".*_collision": 1},
    priority={_foot_regex: 1},
    friction={_foot_regex: (0.6,)},
)

# This disables all collisions except the feet.
# Feet get condim=3, all other geoms are disabled.
FEET_ONLY_COLLISION = CollisionCfg(
    geom_names_expr=[_foot_regex],
    contype=0,
    conaffinity=0,
    condim=3,
    priority=1,
    friction=(0.6,),
)

##
# Actuator config.
##

# kp/kv are uniform across all T1 joints; effort limits and armatures vary
# by motor tier (matches forcerange and per-joint armature in T1_23dof.xml).
_T1_KP = 75.0
_T1_KV = 5.0
_T1_FRICTIONLOSS = 0.1

T1_ACTUATOR_HEAD = BuiltinPositionActuatorCfg(
    target_names_expr=(r"Head_(Yaw|Pitch)",),
    stiffness=_T1_KP,
    damping=_T1_KV,
    effort_limit=7.0,
    armature=0.0,
    frictionloss=_T1_FRICTIONLOSS,
)
T1_ACTUATOR_ARM_PITCH = BuiltinPositionActuatorCfg(
    target_names_expr=(r"(Left|Right)_(Shoulder|Elbow)_Pitch",),
    stiffness=_T1_KP,
    damping=_T1_KV,
    effort_limit=18.0,
    armature=0.05,
    frictionloss=_T1_FRICTIONLOSS,
)
T1_ACTUATOR_ARM_OTHER = BuiltinPositionActuatorCfg(
    target_names_expr=(
        r"(Left|Right)_Shoulder_Roll",
        r"(Left|Right)_Elbow_Yaw",
    ),
    stiffness=_T1_KP,
    damping=_T1_KV,
    effort_limit=18.0,
    armature=0.0,
    frictionloss=_T1_FRICTIONLOSS,
)
T1_ACTUATOR_WAIST_HIP_ROLL_YAW = BuiltinPositionActuatorCfg(
    target_names_expr=(
        r"Waist",
        r"(Left|Right)_Hip_(Roll|Yaw)",
    ),
    stiffness=_T1_KP,
    damping=_T1_KV,
    effort_limit=25.0,
    armature=0.0,
    frictionloss=_T1_FRICTIONLOSS,
)
T1_ACTUATOR_HIP_PITCH = BuiltinPositionActuatorCfg(
    target_names_expr=(r"(Left|Right)_Hip_Pitch",),
    stiffness=_T1_KP,
    damping=_T1_KV,
    effort_limit=45.0,
    armature=0.0,
    frictionloss=_T1_FRICTIONLOSS,
)
T1_ACTUATOR_KNEE = BuiltinPositionActuatorCfg(
    target_names_expr=(r"(Left|Right)_Knee_Pitch",),
    stiffness=_T1_KP,
    damping=_T1_KV,
    effort_limit=60.0,
    armature=0.0,
    frictionloss=_T1_FRICTIONLOSS,
)
T1_ACTUATOR_ANKLE_PITCH = BuiltinPositionActuatorCfg(
    target_names_expr=(r"(Left|Right)_Ankle_Pitch",),
    stiffness=_T1_KP,
    damping=_T1_KV,
    effort_limit=24.0,
    armature=0.05,
    frictionloss=_T1_FRICTIONLOSS,
)
T1_ACTUATOR_ANKLE_ROLL = BuiltinPositionActuatorCfg(
    target_names_expr=(r"(Left|Right)_Ankle_Roll",),
    stiffness=_T1_KP,
    damping=_T1_KV,
    effort_limit=15.0,
    armature=0.05,
    frictionloss=_T1_FRICTIONLOSS,
)

##
# Articulation config.
##

T1_ARTICULATION = EntityArticulationInfoCfg(
    actuators=(
        T1_ACTUATOR_HEAD,
        T1_ACTUATOR_ARM_PITCH,
        T1_ACTUATOR_ARM_OTHER,
        T1_ACTUATOR_WAIST_HIP_ROLL_YAW,
        T1_ACTUATOR_HIP_PITCH,
        T1_ACTUATOR_KNEE,
        T1_ACTUATOR_ANKLE_PITCH,
        T1_ACTUATOR_ANKLE_ROLL,
    ),
    soft_joint_pos_limit_factor=0.9,
)

##
# Final config.
##


def get_t1_robot_cfg() -> EntityCfg:
    """Get a fresh T1 robot configuration instance.

    Returns a new EntityCfg instance each time to avoid mutation issues when
    the config is shared across multiple places.
    """
    return EntityCfg(
        init_state=INIT_STATE,
        collisions=(FULL_COLLISION,),
        spec_fn=get_spec,
        articulation=T1_ARTICULATION,
    )


T1_ACTION_SCALE: dict[str, float] = {}
for a in T1_ARTICULATION.actuators:
    assert isinstance(a, BuiltinPositionActuatorCfg)
    e = a.effort_limit
    s = a.stiffness
    assert e is not None
    for n in a.target_names_expr:
        T1_ACTION_SCALE[n] = 0.25 * e / s


if __name__ == "__main__":
    import mujoco.viewer as viewer
    from mjlab.entity.entity import Entity

    robot = Entity(get_t1_robot_cfg())

    viewer.launch(robot.spec.compile())
