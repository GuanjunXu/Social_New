#!/usr/bin/python
# coding:utf-8

from devicewrapper.android import device as d
import unittest
import commands
import re
import subprocess
import os
import string
import time
import sys
import util 
import string

AD = util.Adb()
TB = util.TouchButton()
SM = util.SetMode() 

#Written by XuGuanjun

PACKAGE_NAME  = 'com.intel.camera22'
ACTIVITY_NAME = PACKAGE_NAME + '/.Camera'

#All setting info of camera could be cat in the folder
PATH_PREF_XML  = '/data/data/com.intel.camera22/shared_prefs/'

#FDFR / GEO / BACK&FROUNT xml file in com.intelcamera22_preferences_0.xml
PATH_0XML      = PATH_PREF_XML + 'com.intel.camera22_preferences_0.xml'

#PICSIZE / EXPROSURE / TIMER / WHITEBALANCE / ISO / HITS / VIDEOSIZE in com.intel.camera22_preferences_0_0.xml
PATH_0_0XML    = PATH_PREF_XML + 'com.intel.camera22_preferences_0_0.xml'

#####                                    #####
#### Below is the specific settings' info ####
###                                        ###
##                                          ##
#                                            #

#FD/FR states check point
FDFR_STATE      = PATH_0XML   + ' | grep pref_fdfr_key'

#Geo state check point
GEO_STATE       = PATH_0XML   + ' | grep pref_camera_geo_location_key'

#Pic size state check point
PICSIZE_STATE   = PATH_0_0XML + ' | grep pref_camera_picture_size_key'

#Exposure state check point 
EXPOSURE_STATE  = PATH_0_0XML + ' | grep pref_camera_exposure_key'

#Timer state check point
TIMER_STATE     = PATH_0_0XML + ' | grep pref_camera_delay_shooting_key'

#Video Size state check point
VIDEOSIZE_STATE = PATH_0_0XML + ' | grep pref_video_quality_key'

#White balance state check point
WBALANCE_STATE  = PATH_0_0XML + ' | grep pref_camera_whitebalance_key'

#Flash state check point
FLASH_STATE     = PATH_0_0XML + ' | grep pref_camera_video_flashmode_key'

class CameraTest(unittest.TestCase):
    def setUp(self):
        super(CameraTest,self).setUp()
        #Delete all image/video files captured before
        AD.cmd('rm','/sdcard/DCIM/*')
        #Refresh media after delete files
        AD.cmd('refresh','/sdcard/DCIM/*')
        #Launch social camera
        self._launchCamera()
        SM.switchcamera('video')

    def tearDown(self):
    	AD.cmd('pm','com.intel.camera22') #Force reset the camera settings to default
        super(CameraTest,self).tearDown()
        self._pressBack(4)

    def testRecordVideoWithFlashOn(self):
        '''
            Summary: Record a video in flash on mode
            Steps  : 
                1.Launch video activity
                2.Check flash state, set to ON
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video','flash','on')
        assert AD.cmd('cat',FLASH_STATE).find('on')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoWithFlashOff(self):
        '''
            Summary: Record a video in flash off mode
            Steps  : 
                1.Launch video activity
                2.Check flash state, set to Off
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video','flash','off')
        assert AD.cmd('cat',FLASH_STATE).find('off')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithBalanceAuto(self):
        '''
            Summary: Capture video with White Balance Auto
            Steps  :  
                1.Launch video activity
                2.Set White Balance Auto
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video',5,5)
        assert AD.cmd('cat',WBALANCE_STATE).find('auto')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithBalanceIncandescent(self):
        '''
            Summary: Capture video with White Balance Incandescent
            Steps  :  
                1.Launch video activity
                2.Set White Balance Incandescent
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video',5,4)
        assert AD.cmd('cat',WBALANCE_STATE).find('incandescent')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithBalanceDaylight(self):
        '''
            Summary: Capture video with White Balance Daylight
            Steps  :  
                1.Launch video activity
                2.Set White Balance Daylight
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video',5,3)
        assert AD.cmd('cat',WBALANCE_STATE).find('incandescent')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithBalanceFluorescent(self):
        '''
            Summary: Capture video with White Balance Fluorescent
            Steps  :  
                1.Launch video activity
                2.Set White Balance Fluorescent
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video',5,2)
        assert AD.cmd('cat',WBALANCE_STATE).find('fluorescent')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithBalanceCloudy(self):
        '''
            Summary: Capture video with White Balance Cloudy
            Steps  :  
                1.Launch video activity
                2.Set White Balance Cloudy
                3.Touch shutter button to capture 30s video
                4.Exit  activity
        '''
        SM.setCameraSetting('video',5,1)
        assert AD.cmd('cat',WBALANCE_STATE).find('cloudy')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithExposureAuto(self):
        '''
            Summary: Capture video with Exposure auto
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure auto
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity
        '''
        SM.setCameraSetting('video',4,3)
        assert AD.cmd('cat',EXPOSURE_STATE).find('0')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithExposure1(self):
        '''
            Summary: Capture video with Exposure 1
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure 1
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity
        '''
        SM.setCameraSetting('video',4,4)
        assert AD.cmd('cat',EXPOSURE_STATE).find('3')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithExposure2(self):
        '''
            Summary: Capture video with Exposure 2
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure 2
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity
        '''
        SM.setCameraSetting('video',4,5)
        assert AD.cmd('cat',EXPOSURE_STATE).find('6')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithExposureRed1(self):
        '''
            Summary: Capture video with Exposure -1
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure -1
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity
        '''
        SM.setCameraSetting('video',4,2)
        assert AD.cmd('cat',EXPOSURE_STATE).find('-3')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithExposureRed2(self):
        '''
            Summary: Capture video with Exposure -2
            Steps  :  
                1.Launch Video activity
                2.Touch Exposure Setting icon, set Exposure -2
                3.Touch shutter button
                4.Touch shutter button to capture picture
                5.Exit  activity
        '''
        SM.setCameraSetting('video',4,1)
        assert AD.cmd('cat',EXPOSURE_STATE).find('-6')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithHSSize(self):
        '''
            Summary: Capture video with HS size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set to HS
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''
        SM.setCameraSetting('video',3,3)
        assert AD.cmd('cat',VIDEOSIZE_STATE).find('5')
        assert AD.cmd('cat',PATH_0_0XML + ' | grep enable-hightspeed').find('true')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithHDSize(self):
        '''
            Summary: Capture video with HD size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set to HD
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''
        SM.setCameraSetting('video',3,2)
        assert AD.cmd('cat',VIDEOSIZE_STATE).find('5')
        assert AD.cmd('cat',PATH_0_0XML + ' | grep enable-hightspeed').find('false')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithSDSize(self):
        '''
            Summary: Capture video with SD size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set to SD
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''
        SM.setCameraSetting('video',3,1)
        assert AD.cmd('cat',VIDEOSIZE_STATE).find('4')
        assert AD.cmd('cat',PATH_0_0XML + ' | grep enable-hightspeed').find('false')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithFHDSize(self):
        '''
            Summary: Capture video with FHD size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set to FHD
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''
        SM.setCameraSetting('video',3,4)
        assert AD.cmd('cat',VIDEOSIZE_STATE).find('6')
        assert AD.cmd('cat',PATH_0_0XML + ' | grep enable-hightspeed').find('false')
        self._takeVideoAndCheckCount(30,2)

    def testRecordVideoCaptureVideoWithFHSSize(self):
        '''
            Summary: Capture video with FHS size
            Steps  :  
                1.Launch video activity
                2.Check video size ,set to FHS
                3.Touch shutter button to capture 30s video
                4.Exit  activity 
        '''
        SM.setCameraSetting('video',3,5)
        assert AD.cmd('cat',VIDEOSIZE_STATE).find('6')
        assert AD.cmd('cat',PATH_0_0XML + ' | grep enable-hightspeed').find('true')
        self._takeVideoAndCheckCount(30,2)
















    def _takeVideoAndCheckCount(self,recordtime,delaytime):
        beforeNo = AD.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count before capturing
        TB.takeVideo(recordtime)
        time.sleep(delaytime) #Sleep a few seconds for file saving
        afterNo = AD.cmd('ls','/sdcard/DCIM/100ANDRO') #Get count after taking picture
        if beforeNo != afterNo - 1: #If the count does not raise up after capturing, case failed
            self.fail('Taking picture failed!')

    def _launchCamera(self):
        d.start_activity(component = ACTIVITY_NAME)
        #When it is the first time to launch camera there will be a dialog to ask user 'remember location', so need to check
        try:
            assert d(text = 'OK').wait.exists(timeout = 2000)
            d(text = 'OK').click.wait()
        except:
            pass
        assert d(resourceId = 'com.intel.camera22:id/mode_button').wait.exists(timeout = 3000), 'Launch camera failed in 3s'

    def _pressBack(self,touchtimes):
        for i in range(0,touchtimes):
            d.press('back')
