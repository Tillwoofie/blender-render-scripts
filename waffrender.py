import argparse
import bpy
import sys


def set_comp_device(device_type):
    waffcycles = bpy.context.preferences.addons['cycles']
    waffcycles.preferences.get_devices()
    try:
        waffcycles.preferences.compute_device_type = device_type
    except (TypeError):
        return False
    return True

def list_devices():
    waffcycles = bpy.context.preferences.addons['cycles']
    waffcycles.preferences.get_devices()
    return waffcycles.preferences.devices

def enable_device(device):
    waffcycles = bpy.context.preferences.addons['cycles']
    waffcycles.preferences.get_devices()
    print(device['name'])
    device['use'] = 1
    print(' - Enabled!')

def enable_devices(try_nvidia):
    waffcycles = bpy.context.preferences.addons['cycles']
    waffcycles.preferences.get_devices()
    # find and maybe filter devices for optix/cuda
    nvidia_dev_found = False

    if try_nvidia:
        for device in waffcycles.preferences.devices:
            if 'NVIDIA' in device['name']:
                enable_device(device)
                nvidia_dev_found = True
            elif 'Tesla' in device['name']:
                enable_device(device)
                nvidia_dev_found = True
    
    # no nvidia devices found
    if not try_nvidia or not nvidia_dev_found:
        print("")
        print("No nvidia devices found or requested, enable everything else.")
        for device in waffcycles.preferences.devices:
            device['use'] = 1
            print(device['name'], " - Enabled!" if device['use'] else " - Disabled!" )


def list_cameras():
    return [cam for cam in bpy.data.objects if cam.type == 'CAMERA']


def set_cam(new_camera):
    bpy.context.scene.camera = bpy.data.objects[new_camera]


def main():
    #do things
    noargs = False
    
    argv = sys.argv
    try:
        argv = argv[argv.index('--') + 1:]
    except (ValueError):
        noargs = True

    parser = argparse.ArgumentParser(description="Set options on waffrender")

    parser.add_argument('-c', '--cam', action="store", type=str, default="", dest='cam_new_name')
    parser.add_argument('-n', '--no-accel', action='store_true', default=False, dest='no_accel')
    parser.add_argument('-l', '--list', action='store_true', default=False, dest='list_accel')

    args = parser.parse_args(argv)

    if args.list_accel:
        for dev in list_devices():
            print( dev['name'] )
    
    #if we want accel:
    if not args.no_accel:
       optix_on = set_comp_device('OPTIX')
       if not optix_on:
           cuda_on = set_comp_device('CUDA')
       # if neither, we got no special devices.
       if optix_on or cuda_on:
           enable_devices(True)
       else:
           enable_devices(False)
    else:
        print("No acceleration requested, using default devices")

    # if set camera

    cam_name=args.cam_new_name
    if cam_name != "":
        blend_cams = list_cameras()
        if cam_name in [cam.name for cam in blend_cams]:
            print("New camera %s found and set!" % cam_name)
            set_cam(cam_name)
        else:
            print("Camera %s not found, using default cam from file" % cam_name)

if __name__ == '__main__':
    main()
