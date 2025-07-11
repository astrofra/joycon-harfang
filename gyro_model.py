# Draw models without a pipeline

import harfang as hg
from pyjoycon import GyroTrackingJoyCon, get_L_id, get_R_id

joycon_id = get_L_id()
joycon = GyroTrackingJoyCon(*joycon_id)

hg.InputInit()
hg.WindowSystemInit()

res_x, res_y = 1280, 720
win = hg.RenderInit('Harfang - Draw Models no Pipeline', res_x, res_y, hg.RF_VSync | hg.RF_MSAA4X)

# vertex layout and models
vtx_layout = hg.VertexLayoutPosFloatNormUInt8()

cube_mdl = hg.CreateCubeModel(vtx_layout, 1, 1, 1)
ground_mdl = hg.CreatePlaneModel(vtx_layout, 5, 5, 1, 1)

shader = hg.LoadProgramFromFile('assets_compiled/shaders/mdl')

# main loop
angle = 0

while not hg.ReadKeyboard().Key(hg.K_Escape) and hg.IsWindowOpen(win):
	dt = hg.TickClock()
	angle = angle + hg.time_to_sec_f(dt)

	viewpoint = hg.TranslationMat4(hg.Vec3(0, 1, -3))
	hg.SetViewPerspective(0, 0, 0, res_x, res_y, viewpoint)

	# cube_rot = hg.Vec3(joycon.direction.x, joycon.direction.y, joycon.direction.z)
	cube_rot = hg.Vec3(-joycon.rotation.y, joycon.rotation.z, -joycon.rotation.x)
	# cube_rot = hg.Vec3(joycon.pointer.x, joycon.pointer.y, 0.0)
	hg.DrawModel(0, cube_mdl, shader, [], [], hg.TransformationMat4(hg.Vec3(0, 1, 0), cube_rot))
	hg.DrawModel(0, ground_mdl, shader, [], [], hg.TranslationMat4(hg.Vec3(0, 0, 0)))

	hg.Frame()
	hg.UpdateWindow(win)

hg.RenderShutdown()
