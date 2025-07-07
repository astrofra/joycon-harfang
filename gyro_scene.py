from math import pi

def clamp(x, a, b):
	x = max(x, a)
	x = min(x, b)
	return x

import harfang as hg
from pyjoycon import GyroTrackingJoyCon, get_L_id, get_R_id

joycon_id = get_L_id()
joycon = GyroTrackingJoyCon(*joycon_id)

hg.InputInit()
hg.WindowSystemInit()

res_x, res_y = 1280, 720
win = hg.RenderInit('Harfang - Draw Models no Pipeline', res_x, res_y, hg.RF_VSync | hg.RF_MSAA4X)

pipeline = hg.CreateForwardPipeline()
res = hg.PipelineResources()

hg.AddAssetsFolder("assets_compiled")

scene = hg.Scene()
hg.LoadSceneFromAssets("main.scn", scene, res, hg.GetForwardPipelineInfo())

# main loop
lamp = scene.GetNode("lamp")

while not hg.ReadKeyboard().Key(hg.K_Escape) and hg.IsWindowOpen(win):
	dt = hg.TickClock()

	# cube_rot = hg.Vec3(joycon.direction.x, joycon.direction.y, joycon.direction.z)
	# cube_rot = hg.Vec3(joycon.rotation.y, joycon.rotation.z, joycon.rotation.x)
	# cube_rot = hg.Vec3(joycon.pointer.x, joycon.pointer.y, 0.0)
	if joycon.pointer is not None:
		x = joycon.pointer.y
	else:
		x = prev_x

	if joycon.pointer is not None:
		y = joycon.pointer.x
	else:
		y = prev_y

	x = clamp(x, -pi/2, pi/2)
	y = clamp(y, -pi/2, pi/2)

	prev_x = x
	prev_y = y

	cube_rot = hg.Vec3(x, y, 0)

	lamp.GetTransform().SetRot(cube_rot)

	scene.Update(dt)
	hg.SubmitSceneToPipeline(0, scene, hg.IntRect(0, 0, res_x, res_y), True, pipeline, res)

	hg.Frame()
	hg.UpdateWindow(win)

hg.RenderShutdown()
