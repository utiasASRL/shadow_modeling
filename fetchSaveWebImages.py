#!/usr/bin/env python

# coding: utf-8


# to access the OS disk
import os
import sys

# deal with URL images
import urllib

# for data structure
import pandas as pd

# image processing
from PIL import Image

# time management
import datetime
import time



cam_names = {'Cuyamaca_Peak',
              'California_School',
              'Tenerife_Observatory',
              'Kelowna_Airport',
              'Phoenix_Arizona'
             }

metadata = pd.DataFrame(index=cam_names, columns=('lat', 'long', 'utc_offset', 'webcam_url', 'crop_left', 'crop_top', 'crop_right', 'crop_bottom'))

metadata.loc['Cuyamaca_Peak'] = (32.916783, -116.631822, -8,'http://www.creekbed.org/cuyacam_000.jpg', 0, 0, 1280, 610)
metadata.loc['California_School'] = (32.668000, -116.295743, -8, 'http://wwc.instacam.com/instacamimg/BLVRD/BLVRD_l.jpg', 50, 0, 1280, 720)
metadata.loc['Tenerife_Observatory'] = (28.302559, -16.510025, 0, 'http://www.telescope.org/v4webcams-i.php?cam=teide', 0, 0, 640, 460)
metadata.loc['Kelowna_Airport'] = (49.957878, -119.378719, -8, 'http://www.metcam.navcanada.ca/dawc_images/wxcam/CYLW/CYLW_N-full-e.jpeg', 15, 53, 769, 600)
metadata.loc['Phoenix_Arizona'] = (33.583734, -112.072115, -7, 'http://www.phoenixvis.net/CreateMain.aspx?t=main&p=/images/photos-main/SOMT1.jpg', 0, 0, 800, 458)

metadata.to_csv('./metadata.csv')



sleep_time = 10 # in minutes

counter = 0

while(True):
    for name in metadata.index:
        path = './' + name

        # check if folders exist
        if not os.path.exists(path):
            os.makedirs(path)

        try:
            # save images
            image_name = str(counter) + ".jpg"
            image_path = path + '/' + image_name
            urllib.urlretrieve(metadata.loc[name].webcam_url, image_path)

            # Dealing with time zones
            utc_now = datetime.datetime.utcnow()

            # crop image to remove artifacts caused by texts
            time.sleep(1)
        
            original = Image.open(image_path)
            crop_measur = metadata.loc[name, ['crop_left', 'crop_top', 'crop_right', 'crop_bottom'] ].values
            original = original.crop(crop_measur)
            original.save(image_path)

            # write the information
            time_file_path = path + '/' + name + '_time.csv'
            if not os.path.exists(time_file_path):
                with open(time_file_path, 'a') as f:
                    f.write('file_name, utc_time \n')


            with open(time_file_path, 'a') as f:
                f.write(image_name + ', ' + str(utc_now) + '\n')
        except:
            error_file_path = time_file_path = path + '/error_log.txt'
            e = sys.exc_info()[0]
            
            with open(error_file_path, 'a') as f:
                f.write(image_name + ': ' + str(e) + ' \n')            

    

    
    rec_duration = datetime.timedelta(minutes = counter*sleep_time)
    counter += 1
    
    # print information console
    os.system('clear')
    print('Number of images recorded: ' + str(counter) + ' total time: ' + str(rec_duration))

    time.sleep(sleep_time*60) # in seconds

