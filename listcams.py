import bpy

print()
print()
print("Listing camera information:")
print()

cam_ob = bpy.context.scene.camera

if cam_ob is None:
    print("No scene cam detected")
elif cam_ob.type == 'CAMERA':
    print("Regular scene cam: %s" % cam_ob.name)
else:
    print("%s object as camera: %s" % (cam_ob.type, cam_ob.name))

cameras_obj = [cam for cam in bpy.data.objects if cam.type == 'CAMERA']
print("Cameras found: %i" % (len(cameras_obj), ))
print()
print("Scene cameras:")
for cam in cameras_obj:
    print("  - %s" % cam.name)
