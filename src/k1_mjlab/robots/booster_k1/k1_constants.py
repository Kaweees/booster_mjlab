"""Booster K1 constants."""

from pathlib import Path

import mujoco
from mjlab.actuator import BuiltinPositionActuatorCfg
from mjlab.entity import EntityArticulationInfoCfg, EntityCfg
from mjlab.utils.spec_config import CollisionCfg

##
# MJCF and assets.
##

K1_XML: Path = Path(__file__).parent / "xmls" / "k1.xml"

assert K1_XML.exists(), f"K1 robot XML not found at {K1_XML}"


def get_spec() -> mujoco.MjSpec:
    return mujoco.MjSpec.from_file(str(K1_XML))


##
# Keyframe config.
##

INIT_STATE = EntityCfg.InitialStateCfg(
    pos=(0, 0, 0.513),
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

# kp/kv are uniform across all K1 joints; effort limits and armatures vary by motor tier.
_K1_KP = 75.0
_K1_KV = 5.0
_K1_FRICTIONLOSS = 0.1

K1_ACTUATOR_HEAD = BuiltinPositionActuatorCfg(
    target_names_expr=(r"Head_(Yaw|Pitch)",),
    stiffness=_K1_KP,
    damping=_K1_KV,
    effort_limit=6.0,
    armature=0.002,
    frictionloss=_K1_FRICTIONLOSS,
)
K1_ACTUATOR_ARM = BuiltinPositionActuatorCfg(
    target_names_expr=(
        r"(Left|Right)_Shoulder_(Pitch|Roll)",
        r"(Left|Right)_Elbow_(Pitch|Yaw)",
    ),
    stiffness=_K1_KP,
    damping=_K1_KV,
    effort_limit=14.0,
    armature=0.001,
    frictionloss=_K1_FRICTIONLOSS,
)
K1_ACTUATOR_ANKLE = BuiltinPositionActuatorCfg(
    target_names_expr=(r"(Left|Right)_Ankle_(Pitch|Roll)",),
    stiffness=_K1_KP,
    damping=_K1_KV,
    effort_limit=20.0,
    armature=0.0565,
    frictionloss=_K1_FRICTIONLOSS,
)
K1_ACTUATOR_HIP_PITCH = BuiltinPositionActuatorCfg(
    target_names_expr=(r"(Left|Right)_Hip_Pitch",),
    stiffness=_K1_KP,
    damping=_K1_KV,
    effort_limit=30.0,
    armature=0.0478125,
    frictionloss=_K1_FRICTIONLOSS,
)
K1_ACTUATOR_HIP_ROLL = BuiltinPositionActuatorCfg(
    target_names_expr=(r"(Left|Right)_Hip_Roll",),
    stiffness=_K1_KP,
    damping=_K1_KV,
    effort_limit=35.0,
    armature=0.0339552,
    frictionloss=_K1_FRICTIONLOSS,
)
K1_ACTUATOR_HIP_YAW = BuiltinPositionActuatorCfg(
    target_names_expr=(r"(Left|Right)_Hip_Yaw",),
    stiffness=_K1_KP,
    damping=_K1_KV,
    effort_limit=20.0,
    armature=0.0282528,
    frictionloss=_K1_FRICTIONLOSS,
)
K1_ACTUATOR_KNEE = BuiltinPositionActuatorCfg(
    target_names_expr=(r"(Left|Right)_Knee_Pitch",),
    stiffness=_K1_KP,
    damping=_K1_KV,
    effort_limit=40.0,
    armature=0.095625,
    frictionloss=_K1_FRICTIONLOSS,
)

##
# Articulation config.
##

K1_ARTICULATION = EntityArticulationInfoCfg(
    actuators=(
        K1_ACTUATOR_HEAD,
        K1_ACTUATOR_ARM,
        K1_ACTUATOR_ANKLE,
        K1_ACTUATOR_HIP_PITCH,
        K1_ACTUATOR_HIP_ROLL,
        K1_ACTUATOR_HIP_YAW,
        K1_ACTUATOR_KNEE,
    ),
    soft_joint_pos_limit_factor=0.9,
)

##
# Final config.
##


def get_k1_robot_cfg() -> EntityCfg:
    """Get a fresh K1 robot configuration instance.

    Returns a new EntityCfg instance each time to avoid mutation issues when
    the config is shared across multiple places.
    """
    return EntityCfg(
        init_state=INIT_STATE,
        collisions=(FULL_COLLISION,),
        spec_fn=get_spec,
        articulation=K1_ARTICULATION,
    )


K1_ACTION_SCALE: dict[str, float] = {}
for a in K1_ARTICULATION.actuators:
    assert isinstance(a, BuiltinPositionActuatorCfg)
    e = a.effort_limit
    s = a.stiffness
    assert e is not None
    for n in a.target_names_expr:
        K1_ACTION_SCALE[n] = 0.25 * e / s


if __name__ == "__main__":
    import mujoco.viewer as viewer
    from mjlab.entity.entity import Entity

    robot = Entity(get_k1_robot_cfg())

    viewer.launch(robot.spec.compile())
