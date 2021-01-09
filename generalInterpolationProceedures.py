import os
import shutil
from runAndPrintOutput import runAndPrintOutput

FFMPEG4 = 'ffmpeg'


def extractFrames(inputFile, projectFolder, mode, mpdecimateSensitivity="64*12,64*8,0.33"):
    '''
    Equivalent to DAINAPP Step 1
    '''
    os.chdir(projectFolder)
    if os.path.exists("original_frames"):
        shutil.rmtree("original_frames")
    if not os.path.exists("original_frames"):
        os.mkdir("original_frames")

    if mode == 1:
        runAndPrintOutput([FFMPEG4,'-i',inputFile,'-map_metadata','-1','-pix_fmt','rgb24','original_frames/%15d.png'])
    elif mode == 3 or mode == 4:
        hi, lo, frac = mpdecimateSensitivity.split(",")
        mpdecimate = "mpdecimate=hi={}:lo={}:frac={}".format(hi, lo, frac)
        runAndPrintOutput([FFMPEG4,'-i',inputFile,'-map_metadata','-1','-pix_fmt','rgb24','-copyts','-r','1000','-vsync','0','-frame_pts','true','-vf', mpdecimate,'-qscale:v','1','original_frames/%15d.png'])

def generateLoopContinuityFrame(framesFolder):
    files = os.listdir(framesFolder)
    files.sort()

    # Find the distance between the first two and last two frames
    # Use this distance to calculate position for the loop continuity frame
    beginFirst = int(files[0][:-4])
    endFirst = int(files[1][:-4])

    beginLast = int(files[-2][:-4])
    endLast = int(files[-1][:-4])

    averageDistance = int(((endFirst-beginFirst) + (endLast-beginLast)) / 2)

    # Create frame
    shutil.copy(framesFolder + '/' + files[0], framesFolder + '/' + '{:015d}.png'.format(endLast + averageDistance))
    print("Made loop continuity frame:",framesFolder + '/' + '{:015d}.png'.format(endLast + averageDistance))

def removeLoopContinuityFrame(framesFolder):
    files = os.listdir(framesFolder)
    files.sort()
    os.remove(framesFolder + '/' + files[-1])

