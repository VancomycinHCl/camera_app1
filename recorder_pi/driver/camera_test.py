import os
import sys
import configparser
import time
from datetime import datetime
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

class CommandInstance():
    def __init__(self,type,payload,config):
        self.type = type
        self.payload = payload
        self.config = config
    def __str__(self):
        print(self,self.type)

def readConfig(file):
    read_ini = configparser.ConfigParser()
    read_ini.read(file)
    cam_value = read_ini.items('Camera')
    path_value = read_ini.items('Path')
    other_value = read_ini.items('Other')
    camera_config = {}
    path_config = {}
    other_config = {}
    for i in cam_value:
        camera_config[i[0]] = i[1]
    for i in path_value:
        path_config[i[0]] = i[1]
    for i in other_value:
        other_config[i[0]] = i[1]
    #print(camera_config,other_config,path_config)
    return (camera_config,path_config,other_config)

def generateCommand_str(config_dict):
    cmd_list = ["libcamera-vid","--save-pts timestamps.txt"]
    camera_config,path_config,other_config = config_dict
    cmd_list.append("--height")
    cmd_list.append(camera_config["height"])
    cmd_list.append("--width")
    cmd_list.append(camera_config["width"])
    cmd_list.append("--framerate")
    cmd_list.append(camera_config["framerate"])
    cmd_list.append("-t")
    cmd_list.append(camera_config["duration"])
    if (camera_config["focus"] == "continue"):
        pass
        #cmd_list.append("--continue-autofocus")
    if (other_config["preview"]=="qt-preview"):
        cmd_list.append("--qt-preview")
    root_path_str = path_config["root_path"]
    video_path_str = path_config["raw_path"]
    filename_str = datetime.now().strftime("%H_%M_%S")
    cmd_list.append("-o")
    cmd_list.append(root_path_str+"/"+video_path_str+"/"+filename_str+".h264")
    #cmd_list.append(filename_str + ".h264")
    cmd_str = " ".join(cmd_list)
    print(cmd_str)
    return CommandInstance(payload=cmd_str, type="bash_cmd", config=config_dict)

def generateCommand_api():
    
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)

    encoder = H264Encoder(10000000)

    picam2.start_recording(encoder, '/home/pi/camera_app/output/raw_video/test.h264')
    time.sleep(60)
    picam2.stop_recording()
    

def generateCommand_str_classInline(config_dict):
    cmd_list = ["libcamera-vid","--save-pts timestamps.txt"]
    #camera_config,path_config,other_config = config_dict
    cmd_list.append("--height")
    cmd_list.append(config_dict["height"])
    cmd_list.append("--width")
    cmd_list.append(config_dict["width"])
    cmd_list.append("--framerate")
    cmd_list.append(config_dict["framerate"])
    cmd_list.append("-t")
    cmd_list.append(config_dict["duration"])
    if (config_dict["focus"] == "continue"):
        pass
        #cmd_list.append("--continue-autofocus")
    if (config_dict["preview"]=="qt-preview"):
        cmd_list.append("--qt-preview")
    root_path_str = config_dict["root_path"]
    video_path_str = config_dict["raw_path"]
    filename_str = datetime.now().strftime("%H_%M_%S")
    cmd_list.append("-o")
    cmd_list.append(root_path_str+"/"+video_path_str+"/"+filename_str+".h264")
    #cmd_list.append(filename_str + ".h264")
    cmd_str = " ".join(cmd_list)
    print(cmd_str)
    return CommandInstance(payload=cmd_str,type="bash_cmd",config=config_dict)


def CaptureVideo_0(commandInstance):
    if commandInstance.type == "bash_cmd":
        #try:
            #root_path_str = commandInstance.config[1]["root_path"]
            #video_path_str = commandInstance.config[1]["raw_path"]
        #except:
            #root_path_str = commandInstance.config["root_path"]
            #video_path_str = commandInstance.config["raw_path"]
        #dest_path_list = [root_path_str,"/",video_path_str]
        #dest_path = "".join(dest_path_list)
        #src_path = "*.h264"
        os.system(commandInstance.payload)
        #print("mv "+src_path+" "+dest_path)
        #os.system("mv "+src_path+" "+dest_path)
    return

def CaptureVideo(commandInstance) -> (str,str) or None:
    """
    Introduction: Capture the video by executing bash command and return the file path.

    :param commandInstance: Class commandinstance
    :return: string tuple, first is the current filename and the second is the path
    """


    if commandInstance.type == "bash_cmd":
        root_path_str = commandInstance.config["root_path"]
        video_path_str = commandInstance.config["raw_path"]
        filename_str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        dest_path = "".join(root_path_str+"/"+video_path_str+"/"+filename_str+".h264")
        src_path = "*.h264"
        os.system(commandInstance.payload)
        #os.system("mv "+dest_path+" "+src_path)
        return (filename_str,dest_path)
    return


if __name__ == "__main__":
    a = readConfig("/home/pi/camera_app/config.ini")
    a1 = generateCommand_str(a)
    CaptureVideo(a1)
    #generateCommand_api()
