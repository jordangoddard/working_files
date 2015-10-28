import bpy

# Rename default pitchipoy controls to tangent animation control nameing convension

# Center Controls
bpy.context.object.data.bones["root"].name = "ctl.god.C"
bpy.context.object.data.bones["tweak_spine.001"].name = "ctl.twk_spine_02.C"
bpy.context.object.data.bones["tweak_spine.002"].name = "ctl.twk_spine_03.C"
bpy.context.object.data.bones["tweak_spine.003"].name = "ctl.twk_spine_04.C"
bpy.context.object.data.bones["tweak_spine.004"].name = "ctl.twk_neck_01.C"
bpy.context.object.data.bones["tweak_spine.005"].name = "ctl.twk_neck_02.C"
bpy.context.object.data.bones["tweak_spine"].name = "ctl.twk_spine_01.C"

bpy.context.object.data.bones["torso"].name = "ctl.root.C"
bpy.context.object.data.bones["hips"].name = "ctl.hips.C"
bpy.context.object.data.bones["chest"].name = "ctl.chest.C"
bpy.context.object.data.bones["neck"].name = "ctl.neck.C"
bpy.context.object.data.bones["head"].name = "ctl.head.C"

bpy.context.object.data.bones["shoulder.L"].name = "ctl.clavicle.L"
bpy.context.object.data.bones["shoulder.R"].name = "ctl.clavicle.R"
bpy.context.object.data.bones["breast.L"].name = "ctl.breast.L"
bpy.context.object.data.bones["breast.R"].name = "ctl.breast.R"

# Leg Controls
bpy.context.object.data.bones["foot_tweak.L"].name = "ctl.twk_foot.L"
bpy.context.object.data.bones["shin_tweak.L.001"].name = "ctl.twk_shin_01.L"
bpy.context.object.data.bones["shin_tweak.L"].name = "ctl.twk_shin_02.L"
bpy.context.object.data.bones["thigh_tweak.L.001"].name = "ctl.twk_thigh_01.L"
bpy.context.object.data.bones["thigh_tweak.L"].name = "ctl.twk_thigh_02.L"

bpy.context.object.data.bones["foot_tweak.R"].name = "ctl.twk_foot.R"
bpy.context.object.data.bones["shin_tweak.R.001"].name = "ctl.twk_shin_01.R"
bpy.context.object.data.bones["shin_tweak.R"].name = "ctl.twk_shin_02.R"
bpy.context.object.data.bones["thigh_tweak.R.001"].name = "ctl.twk_thigh_01.R"
bpy.context.object.data.bones["thigh_tweak.R"].name = "ctl.twk_thigh_02.R"

bpy.context.object.data.bones["foot_fk.L"].name = "ctl.fk_foot.L"
bpy.context.object.data.bones["shin_fk.L"].name = "ctl.fk_shin.L"
bpy.context.object.data.bones["thigh_fk.L"].name = "ctl.fk_thigh.L"

bpy.context.object.data.bones["foot_fk.R"].name = "ctl.fk_foot.R"
bpy.context.object.data.bones["shin_fk.R"].name = "ctl.fk_shin.R"
bpy.context.object.data.bones["thigh_fk.R"].name = "ctl.fk_thigh.R"

bpy.context.object.data.bones["foot_ik.L"].name = "ctl.ik_foot.L"
bpy.context.object.data.bones["foot_heel_ik.L"].name = "ctl.ik_heel.L"
bpy.context.object.data.bones["thigh_ik.L"].name = "ctl.ik_thigh.L"
bpy.context.object.data.bones["toe.L"].name = "ctl.toe.L"

bpy.context.object.data.bones["foot_ik.R"].name = "ctl.ik_foot.R"
bpy.context.object.data.bones["foot_heel_ik.R"].name = "ctl.ik_heel.R"
bpy.context.object.data.bones["thigh_ik.R"].name = "ctl.ik_thigh.R"
bpy.context.object.data.bones["toe.R"].name = "ctl.toe.R"

# Arm Controls
bpy.context.object.data.bones["upper_arm_tweak.L.001"].name = "ctl.twk_arm_upper_02.L"
bpy.context.object.data.bones["upper_arm_tweak.L"].name = "ctl.twk_arm_upper_01.L"
bpy.context.object.data.bones["forearm_tweak.L"].name = "ctl.twk_forarm_02.L"
bpy.context.object.data.bones["forearm_tweak.L.001"].name = "ctl.twk_forarm_01.L"
bpy.context.object.data.bones["hand_tweak.L"].name = "ctl.twk_hand.L"

bpy.context.object.data.bones["upper_arm_tweak.R.001"].name = "ctl.twk_arm_upper_02.R"
bpy.context.object.data.bones["upper_arm_tweak.R"].name = "ctl.twk_arm_upper_01.R"
bpy.context.object.data.bones["forearm_tweak.R"].name = "ctl.twk_forarm_02.R"
bpy.context.object.data.bones["forearm_tweak.R.001"].name = "ctl.twk_forarm_01.R"
bpy.context.object.data.bones["hand_tweak.R"].name = "ctl.twk_hand.R"

bpy.context.object.data.bones["upper_arm_fk.L"].name = "ctl.fk_arm_upper.L"
bpy.context.object.data.bones["forearm_fk.L"].name = "ctl.fk_forarm.L"
bpy.context.object.data.bones["hand_fk.L"].name = "ctl.fk_hand.L"

bpy.context.object.data.bones["upper_arm_fk.R"].name = "ctl.fk_arm_upper.R"
bpy.context.object.data.bones["forearm_fk.R"].name = "ctl.fk_forarm.R"
bpy.context.object.data.bones["hand_fk.R"].name = "ctl.fk_hand.R"

bpy.context.object.data.bones["upper_arm_ik.L"].name = "ctl.ik_arm_upper.L"
bpy.context.object.data.bones["hand_ik.L"].name = "ctl.ik_hand.L"

bpy.context.object.data.bones["upper_arm_ik.R"].name = "ctl.ik_arm_upper.R"
bpy.context.object.data.bones["hand_ik.R"].name = "ctl.ik_hand.R"

# Hand Controls
bpy.context.object.data.bones["tweak_thumb.01.L"].name = "ctl.twk_thumb_01.L"
bpy.context.object.data.bones["tweak_thumb.02.L"].name = "ctl.twk_thumb_02.L"
bpy.context.object.data.bones["tweak_thumb.03.L.001"].name = "ctl.twk_thumb_04.L"
bpy.context.object.data.bones["tweak_thumb.03.L"].name = "ctl.twk_thumb_03.L"
bpy.context.object.data.bones["thumb.01.L"].name = "ctl.thumb_01.L"
bpy.context.object.data.bones["thumb.02.L"].name = "ctl.thumb_02.L"
bpy.context.object.data.bones["thumb.03.L"].name = "ctl.thumb_03.L"

bpy.context.object.data.bones["tweak_thumb.01.R"].name = "ctl.twk_thumb_01.R"
bpy.context.object.data.bones["tweak_thumb.02.R"].name = "ctl.twk_thumb_02.R"
bpy.context.object.data.bones["tweak_thumb.03.R.001"].name = "ctl.twk_thumb_04.R"
bpy.context.object.data.bones["tweak_thumb.03.R"].name = "ctl.twk_thumb_03.R"
bpy.context.object.data.bones["thumb.01.R"].name = "ctl.thumb_01.R"
bpy.context.object.data.bones["thumb.02.R"].name = "ctl.thumb_02.R"
bpy.context.object.data.bones["thumb.03.R"].name = "ctl.thumb_03.R"

bpy.context.object.data.bones["tweak_f_index.01.L"].name = "ctl.twk_index_01.L"
bpy.context.object.data.bones["tweak_f_index.02.L"].name = "ctl.twk_index_02.L"
bpy.context.object.data.bones["tweak_f_index.03.L.001"].name = "ctl.twk_index_04.L"
bpy.context.object.data.bones["tweak_f_index.03.L"].name = "ctl.twk_index_03.L"
bpy.context.object.data.bones["f_index.01.L"].name = "ctl.index_01.L"
bpy.context.object.data.bones["f_index.02.L"].name = "ctl.index_02.L"
bpy.context.object.data.bones["f_index.03.L"].name = "ctl.index_03.L"

bpy.context.object.data.bones["tweak_f_index.01.R"].name = "ctl.twk_index_01.R"
bpy.context.object.data.bones["tweak_f_index.02.R"].name = "ctl.twk_index_02.R"
bpy.context.object.data.bones["tweak_f_index.03.R.001"].name = "ctl.twk_index_04.R"
bpy.context.object.data.bones["tweak_f_index.03.R"].name = "ctl.twk_index_03.R"
bpy.context.object.data.bones["f_index.01.R"].name = "ctl.index_01.R"
bpy.context.object.data.bones["f_index.02.R"].name = "ctl.index_02.R"
bpy.context.object.data.bones["f_index.03.R"].name = "ctl.index_03.R"

bpy.context.object.data.bones["tweak_f_middle.01.L"].name = "ctl.twk_mid_01.L"
bpy.context.object.data.bones["tweak_f_middle.02.L"].name = "ctl.twk_mid_02.L"
bpy.context.object.data.bones["tweak_f_middle.03.L.001"].name = "ctl.twk_mid_04.L"
bpy.context.object.data.bones["tweak_f_middle.03.L"].name = "ctl.twk_mid_03.L"
bpy.context.object.data.bones["f_middle.01.L"].name = "ctl.mid_01.L"
bpy.context.object.data.bones["f_middle.02.L"].name = "ctl.mid_02.L"
bpy.context.object.data.bones["f_middle.03.L"].name = "ctl.mid_03.L"

bpy.context.object.data.bones["tweak_f_middle.01.R"].name = "ctl.twk_mid_01.R"
bpy.context.object.data.bones["tweak_f_middle.02.R"].name = "ctl.twk_mid_02.R"
bpy.context.object.data.bones["tweak_f_middle.03.R.001"].name = "ctl.twk_mid_04.R"
bpy.context.object.data.bones["tweak_f_middle.03.R"].name = "ctl.twk_mid_03.R"
bpy.context.object.data.bones["f_middle.01.R"].name = "ctl.mid_01.R"
bpy.context.object.data.bones["f_middle.02.R"].name = "ctl.mid_02.R"
bpy.context.object.data.bones["f_middle.03.R"].name = "ctl.mid_03.R"

bpy.context.object.data.bones["tweak_f_ring.01.L"].name = "ctl.twk_ring_01.L"
bpy.context.object.data.bones["tweak_f_ring.02.L"].name = "ctl.twk_ring_02.L"
bpy.context.object.data.bones["tweak_f_ring.03.L.001"].name = "ctl.twk_ring_04.L"
bpy.context.object.data.bones["tweak_f_ring.03.L"].name = "ctl.twk_ring_03.L"
bpy.context.object.data.bones["f_ring.01.L"].name = "ctl.ring_01.L"
bpy.context.object.data.bones["f_ring.02.L"].name = "ctl.ring_02.L"
bpy.context.object.data.bones["f_ring.03.L"].name = "ctl.ring_03.L"

bpy.context.object.data.bones["tweak_f_ring.01.R"].name = "ctl.twk_ring_01.R"
bpy.context.object.data.bones["tweak_f_ring.02.R"].name = "ctl.twk_ring_02.R"
bpy.context.object.data.bones["tweak_f_ring.03.R.001"].name = "ctl.twk_ring_04.R"
bpy.context.object.data.bones["tweak_f_ring.03.R"].name = "ctl.twk_ring_03.R"
bpy.context.object.data.bones["f_ring.01.R"].name = "ctl.ring_01.R"
bpy.context.object.data.bones["f_ring.02.R"].name = "ctl.ring_02.R"
bpy.context.object.data.bones["f_ring.03.R"].name = "ctl.ring_03.R"

bpy.context.object.data.bones["tweak_f_pinky.01.L"].name = "ctl.twk_pinky_01.L"
bpy.context.object.data.bones["tweak_f_pinky.02.L"].name = "ctl.twk_pinky_02.L"
bpy.context.object.data.bones["tweak_f_pinky.03.L.001"].name = "ctl.twk_pinky_04.L"
bpy.context.object.data.bones["tweak_f_pinky.03.L"].name = "ctl.twk_pinky_03.L"
bpy.context.object.data.bones["f_pinky.01.L"].name = "ctl.pinky_01.L"
bpy.context.object.data.bones["f_pinky.02.L"].name = "ctl.pinky_02.L"
bpy.context.object.data.bones["f_pinky.03.L"].name = "ctl.pinky_03.L"

bpy.context.object.data.bones["tweak_f_pinky.01.R"].name = "ctl.twk_pinky_01.R"
bpy.context.object.data.bones["tweak_f_pinky.02.R"].name = "ctl.twk_pinky_02.R"
bpy.context.object.data.bones["tweak_f_pinky.03.R.001"].name = "ctl.twk_pinky_04.R"
bpy.context.object.data.bones["tweak_f_pinky.03.R"].name = "ctl.twk_pinky_003.R"
bpy.context.object.data.bones["f_pinky.01.R"].name = "ctl.pinky_01.R"
bpy.context.object.data.bones["f_pinky.02.R"].name = "ctl.pinky_02.R"
bpy.context.object.data.bones["f_pinky.03.R"].name = "ctl.pinky_03.R"

bpy.context.object.data.bones["palm.L"].name = "ctl.palm.L"
bpy.context.object.data.bones["palm.R"].name = "ctl.palm.R"

# Face Controls
bpy.context.object.data.bones["eyes"].name = "ctl.eyes.C"
bpy.context.object.data.bones["eye.L"].name = "ctl.eye.L"
bpy.context.object.data.bones["eye.R"].name = "ctl.eye.R"

bpy.context.object.data.bones["jaw_master"].name = "ctl.jaw_master.C"
bpy.context.object.data.bones["jaw.L.001"].name = "ctl.jaw_02.L"
bpy.context.object.data.bones["jaw.R.001"].name = "ctl.jaw_02.R"
bpy.context.object.data.bones["jaw.L"].name = "ctl.jaw_01.L"
bpy.context.object.data.bones["jaw.R"].name = "ctl.jaw_01.R"
bpy.context.object.data.bones["jaw"].name = "ctl.jaw_01.C"

bpy.context.object.data.bones["teeth.B"].name = "ctl.teeth_bot.C"
bpy.context.object.data.bones["teeth.T"].name = "ctl.teeth_top.C"

bpy.context.object.data.bones["tongue_master"].name = "ctl.tongue_master.C"
bpy.context.object.data.bones["tongue"].name = "ctl.tongue_01.C"
bpy.context.object.data.bones["tongue.001"].name = "ctl.tongue_02.C"
bpy.context.object.data.bones["tongue.002"].name = "ctl.tongue_03.C"
bpy.context.object.data.bones["tongue.003"].name = "ctl.tongue_04.C"

bpy.context.object.data.bones["nose_master"].name = "ctl.nose_01.C"
bpy.context.object.data.bones["nose.R.001"].name = "ctl.nose.R"
bpy.context.object.data.bones["nose.L.001"].name = "ctl.nose.L"
bpy.context.object.data.bones["nose.002"].name = "ctl.nose_02.C"

bpy.context.object.data.bones["master_eye.L"].name = "ctl.eye_master.L"
bpy.context.object.data.bones["master_eye.R"].name = "ctl.eye_master.R"

bpy.context.object.data.bones["ear.L"].name = "ctl.ear.L"
bpy.context.object.data.bones["ear.R"].name = "ctl.ear.R"

bpy.context.object.data.bones["chin"].name = "ctl.chin_01.C"
bpy.context.object.data.bones["chin.001"].name = "ctl.chin_02.C"
bpy.context.object.data.bones["chin.002"].name = "ctl.chin_03.C"
bpy.context.object.data.bones["chin.R"].name = "ctl.chin_01.R"
bpy.context.object.data.bones["chin.L"].name = "ctl.chin_01.L"

bpy.context.object.data.bones["cheek.B.R.001"].name = "ctl.cheek.R"
bpy.context.object.data.bones["cheek.B.L.001"].name = "ctl.cheek.L"

bpy.context.object.data.bones["lips.R"].name = "ctl.lips.R"
bpy.context.object.data.bones["lips.L"].name = "ctl.lips.L"
bpy.context.object.data.bones["lip.B.R.001"].name = "ctl.lips_bot.R"
bpy.context.object.data.bones["lip.B.L.001"].name = "ctl.lips_bot.L"
bpy.context.object.data.bones["lip.B"].name = "ctl.lips_bot.C"
bpy.context.object.data.bones["lip.T.R.001"].name = "ctl.lips_top.R"
bpy.context.object.data.bones["lip.T.L.001"].name = "ctl.lips_top.L"
bpy.context.object.data.bones["lip.T"].name = "ctl.lips_top.C"

bpy.context.object.data.bones["lid.B.R.002"].name = "ctl.eyelid_bot.R"
bpy.context.object.data.bones["lid.T.R.002"].name = "ctl.eyelid_top.R"
bpy.context.object.data.bones["brow.T.R.001"].name = "ctl.brow_01.R"
bpy.context.object.data.bones["brow.T.R.002"].name = "ctl.brow_02.R"
bpy.context.object.data.bones["brow.T.R.003"].name = "ctl.brow_03.R"

bpy.context.object.data.bones["lid.B.L.002"].name = "ctl.eyelid_bot.L"
bpy.context.object.data.bones["lid.T.L.002"].name = "ctl.eyelid_top.L"
bpy.context.object.data.bones["brow.T.L.001"].name = "ctl.brow_01.L"
bpy.context.object.data.bones["brow.T.L.002"].name = "ctl.brow_02.L"
bpy.context.object.data.bones["brow.T.L.003"].name = "ctl.brow_03.L"


bpy.context.object.data.bones["nose"].name = "ctl.sub_nose_00.C"
bpy.context.object.data.bones["nose.001"].name = "ctl.sub_nose_00.C"
bpy.context.object.data.bones["nose.003"].name = "ctl.sub_nose_01.C"
bpy.context.object.data.bones["nose.004"].name = "ctl.sub_nose_02.C"
bpy.context.object.data.bones["nose.005"].name = "ctl.sub_nose_03.C"
bpy.context.object.data.bones["nose.R"].name = "ctl.sub_nose_00.R"
bpy.context.object.data.bones["nose.L"].name = "ctl.sub_nose_00.L"

bpy.context.object.data.bones["cheek.T.R.001"].name = "ctl.sub_cheek.R"
bpy.context.object.data.bones["cheek.T.L.001"].name = "ctl.sub_cheek.L"

bpy.context.object.data.bones["brow.B.R.004"].name = "ctl.sub_brow_04.R"
bpy.context.object.data.bones["brow.B.R.003"].name = "ctl.sub_brow_03.R"
bpy.context.object.data.bones["brow.B.R.002"].name = "ctl.sub_brow_02.R"
bpy.context.object.data.bones["brow.B.R.001"].name = "ctl.sub_brow_01.R"
bpy.context.object.data.bones["brow.B.R"].name = "ctl.sub_brow_00.R"
bpy.context.object.data.bones["brow.T.R"].name = "ctl.sub_temple.R"

bpy.context.object.data.bones["brow.B.L.004"].name = "ctl.sub_brow_04.L"
bpy.context.object.data.bones["brow.B.L.003"].name = "ctl.sub_brow_03.L"
bpy.context.object.data.bones["brow.B.L.002"].name = "ctl.sub_brow_02.L"
bpy.context.object.data.bones["brow.B.L.001"].name = "ctl.sub_brow_01.L"
bpy.context.object.data.bones["brow.B.L"].name = "ctl.sub_brow_00.L"
bpy.context.object.data.bones["brow.T.L"].name = "ctl.sub_temple.L"

bpy.context.object.data.bones["lid.B.R"].name = "ctl.sub_eyelid_00.R"
bpy.context.object.data.bones["lid.T.R.003"].name = "ctl.sub_eyelid_01.R"
bpy.context.object.data.bones["lid.T.R.001"].name = "ctl.sub_eyelid_02.R"
bpy.context.object.data.bones["lid.T.R"].name = "ctl.sub_eyelid_03.R"
bpy.context.object.data.bones["lid.B.R.003"].name = "ctl.sub_eyelid_04.R"
bpy.context.object.data.bones["lid.B.R.001"].name = "ctl.sub_eyelid_05.R"

bpy.context.object.data.bones["lid.B.L"].name = "ctl.sub_eyelid_00.L"
bpy.context.object.data.bones["lid.T.L.003"].name = "ctl.sub_eyelid_01.L"
bpy.context.object.data.bones["lid.T.L.001"].name = "ctl.sub_eyelid_02.L"
bpy.context.object.data.bones["lid.T.L"].name = "ctl.sub_eyelid_03.L"
bpy.context.object.data.bones["lid.B.L.003"].name = "ctl.sub_eyelid_04.L"
bpy.context.object.data.bones["lid.B.L.001"].name = "ctl.sub_eyelid_05.L"

bpy.context.object.data.bones["ear.R.002"].name = "ctl.sub_ear_01.R"
bpy.context.object.data.bones["ear.R.003"].name = "ctl.sub_ear_02.R"
bpy.context.object.data.bones["ear.R.004"].name = "ctl.sub_ear_03.R"

bpy.context.object.data.bones["ear.L.002"].name = "ctl.sub_ear_01.L"
bpy.context.object.data.bones["ear.L.003"].name = "ctl.sub_ear_02.L"
bpy.context.object.data.bones["ear.L.004"].name = "ctl.sub_ear_03.L"

