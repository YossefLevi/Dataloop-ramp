import dtlpy as dl

class SamplingService(dl.BaseServiceRunner):
    """
    Plugin runner class
    """
    sampleCount = 5

    def videoSamples (self, item: dl.Item):
        # could have used dl.utilities.Videos.video_snapshots_generator(item=item, frame_interval=sampleCount)
        import cv2, numpy as np
        import os

        # get sample required from annotation
        sampleRequired = int(item.metadata['user']['samples'])

        # get the first frame of the video to use as background for collecting user input
        print('Download the video ' + item.stream)
        workdir = item.name + '_samples'
        os.makedirs(workdir, exist_ok=True)
        videoPath = os.path.join(workdir, item.name)
        videoPath = item.download(local_path=videoPath)

        # videoPath = '{}?jwt={}'.format(item.stream, dl.token())
        video = cv2.VideoCapture(videoPath)
        if not video.isOpened():
            print('failed opening video url')
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        print('Capturing ' + str(sampleRequired) + ' out of ' + str(frames) + ' frames from ' + videoPath)

        firstFrame = int((frames/sampleRequired)/2)
        interval = int (frames/sampleRequired)
        for i in range(sampleRequired):
            frameIndex = firstFrame + i*interval
            print('sampling frame ' + str(frameIndex))
            video.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
            ret, videoImage = video.read()
            if not ret:
                print('fail to capture frame')
            else:
                cv2.imwrite(videoPath + '_frame_' + str(frameIndex) + '.jpg', videoImage)

        #remove the duplicated local video copy
        os.remove(path=videoPath)
        #upload all frame captured
        item.dataset.items.upload(local_path=workdir)


    def getSampleRequired(self, item: dl.Item):
        import cv2, numpy as np
        import os

        # get the first frame of the video to use as background for collecting user input
        print('1: download the video '+item.stream)
        workdir = item.id
        os.makedirs(workdir, exist_ok=True)
        videoPath = os.path.join(workdir, item.name)
        videoPath = item.download(local_path=videoPath)

        #videoPath = '{}?jwt={}'.format(item.stream, dl.token())
        print('2: capturing first frame from ' + videoPath)
        video = cv2.VideoCapture(videoPath)
        if not video.isOpened():
            print('failed opening video url')
        video.set(cv2.CAP_PROP_POS_FRAMES, 1)
        ret, videoImage = video.read()
        if ret:
            print('first frame captured successfully')
        else:
            print('failed to extract frame')
            videoImage = np.zeros((1080,1920,3), np.uint8)

        w, h = videoImage.shape[1], videoImage.shape[0]

        # show the question on the middle of the image height and left third width
        dialogPoint = (int(w / 3), int(h / 2))
        rectangleStartPoint = (int(w / 3 - 50), int(h / 2 - 50))
        rectangleEndPoint = (int(2.5 * w / 3), int(h / 2 + 50))
        cv2.putText(videoImage, 'How many samples you wish to create?',
                    dialogPoint, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
        key = cv2.waitKey(0)

        inputText = ''
        finish = False
        while not finish:
            image_to_show = np.copy(videoImage)
            cv2.rectangle(image_to_show, rectangleStartPoint, rectangleEndPoint, (0, 0, 255), -1)
            cv2.putText(image_to_show, 'How many samples you wish to create? ' + inputText,
                        dialogPoint, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            cv2.imshow("Video to sample", image_to_show)
            key = cv2.waitKey(0)
            if key == 13:
                # user pressed ENTER
                self.sampleCount = int(inputText)
                finish = True
                cv2.destroyAllWindows()
            elif (key >= 48 and key <= 57):
                inputText += str(key - 48)
            elif (key >= 96 and key <= 105):
                inputText += str(key - 96)

