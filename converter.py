import os
import cv2
import numpy as np
from nptdms import TdmsFile
import time

def get_video_metadata(videotdms, metadatatdms):
    """
    Gets metadata about the video to be converted. These include fps, width and height of 
    frame and total number of frames in video.

    :param videotdms: path to video .tdms
    :param metadatdms: path to metadata .tdms
    :returns: a dictionary with the metadata and an integer with number of frames to convert
    :raises ValueError: if there's a mismatch between expected and reported number of frames
    """
    print(" extracting metadata from: ", metadatatdms)

    # Load metadata
    metadata = TdmsFile(metadata_file)

    # Get values to return
    metadata_object = metadata.object()
    props = {n:v for n,v in metadata_object.properties.items()} # fps, width, ...  

    # Check how many frames are in the video given frame size and # bites in video file
    if props['width'] > 0:
        # Get size of video to be converted 
        videosize = os.path.getsize(videotdms)
        tot = np.int(round(video_size/(props['width']*props['height'])))  # tot number of frames 
        if tot != props['last']:
            raise ValueError('Calculated number of frames doesnt match what is stored in the metadata: {} vs {}'.format(tot, props['last']))
    else:
        tot = 0

    return props, tot


def write_clip(data, savename, tot_frames, w, h, framerate, iscolor=False):
    """ Create a .cv2 videowriter to write the video to file 
    
        :param data: data loaded from video .tdms
        :param savename: string with path so save the video at
        :param tot_frames: number of frames in video
        :param w: width of frame in pixels
        :param h: height of frame in pixels
        :param framerate: fps of video
        :param iscolor: set as True if want to save the video as color data
    """

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videowriter = cv2.VideoWriter(savename, fourcc, framerate, (w, h), iscolor)

    for framen in tqdm(range(tot_frames+1)):
        videowriter.write(data[framen])
    videowriter.release()



def main(videotdms, metadatatdms, use_local_fld=False):
    start = time.time()
    print("Ready to convert: ", videotdms)

    # Get metadata
    props, tot_frames = self.extract_framesize_from_metadata(self.filep)

    # Get temp directory to store memmapped data
    if use_local_fld:
        # Copy the video to be converted to a local directory
        if not os.path.isdir(use_local_fld):
            raise ValueError("Passed 'use_local_fld' argument but it's not a valid directory': ", use_local_fld)
        tempdir = use_local_fld
    else:
        tempdir = os.path.split(videotdms)[0]

    # Open tdms as binary
    print("     opening as binary")
    bfile = open(videotmds, 'rb')

    # Open memmapped
    print('         ...binary opened, opening mmemmapped')
    openstart = time.time()
    tdms = TdmsFile(bfile, memmap_dir=tempdir)  # open tdms binary file as a memmapped object
    openingend = time.time()

    print('         ... memmap opening took: ', np.round(openingend-openstart, 2))
    print('     Extracting data')
    tdms = tdms.__dict__['objects']["/'cam0'/'data'"].data.reshape((tot_frames, props['height'], props['width']), order='C')
    tdms = tdms[:, :, :(props['width']+props['padding'])]  # reshape

    # Write to Video
    savepath = videotdms.split(".")[0]+".mp4"
    print('     Writing video at: ' savepath)
    write_clip(tdms, savepath, params, tot_frames, props['width'], props['height'], props['fps'])
    print('     Finished writing video in {}s.'.format(round(time.time()-openingend, 2)))

    # Check if all the frames have been converted
    cap = cv2.VideoCapture(savepath)
    nframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('     Converted video has {} frames, original video had: {}'.format(nframes, tot_frames))
    if not tot_frames == frames_counter:
        raise ValueError('Number of frames in converted clip doesnt match that of original clip')

    # fin
    end = time.time()
    print('     Converted {} frames in {}s\n\n'.format(tot_frames, round(end-start)))