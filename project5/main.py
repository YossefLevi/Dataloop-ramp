# This is a sample Python script.

import dtlpy as dl

try:
    project = dl.projects.get(project_name='project5')
except:
    project = dl.projects.create(project_name='project5')

dl.projects.checkout(project_name='project5')

try :
    dataset = project.datasets.get(dataset_name='task2_dataset2')
    print('found task2_dataset2')
    filters = dl.Filters()
    filters.add(field='type', values='file')
    dataset.items.delete(filters=filters)
except:
    dataset = dl.datasets.create(dataset_name='task2_dataset2')
    print('created task2_dataset2')

filters = dl.Filters()
filters.add(field='name', values='NewYear.webm')
list = dataset.items.list(filters=filters)
# Count the items
imageCount = list.items_count
print('Number of items in dataset: {}'.format(imageCount))

if imageCount == 0 :
    dataset.items.upload(local_path="C:/Users/forro/Downloads/NewYear.webm")

list = dataset.items.list(filters=filters)

moduleName = 'sampler'
print('define module ' + moduleName)
module = dl.PackageModule(
    name=moduleName,
    class_name='SamplingService',
    #src_path='Source',
    entry_point='sampler.py',
    functions=[
        dl.PackageFunction(
            name='videoSamples',
            inputs=[dl.FunctionIO(type=dl.PackageInputType.ITEM, name="item")],
            #outputs=dataset_io,
            description='generate frame samples out of video item'
        ),
        dl.PackageFunction(
            name='getSampleRequired',
            inputs=[dl.FunctionIO(type=dl.PackageInputType.ITEM, name="item")],
            # outputs=dataset_io,
            description='dialog box to get sample count from the user'
        )
    ])

print('UI slot')
slots = [
    dl.PackageSlot(module_name=moduleName,
                   function_name='videoSamples',
                   display_name='Sample Video',
                   post_action=dl.SlotPostAction(type=dl.SlotPostActionType.NO_ACTION),
                   display_icon='fas fa-exchange-alt',
                   display_scopes=[
                       dl.SlotDisplayScope(
                           resource=dl.SlotDisplayScopeResource.ITEM,
                           panel=dl.UiBindingPanel.STUDIO,
                           filters={})])
]

packageName = 'video-sampler'
print('push package '+ packageName)
package = project.packages.push(
    package_name=packageName,
    modules=module,
    slots=slots
)

print('create service')
try:
    service = package.services.deploy(service_name=packageName, module_name=moduleName)
except:
    print('service already exist')
    package = package.update()
    service = package.services.get(service_name=packageName)
    project.services.update(service=service)

package.services.activate_slots(service=service,
                                project_id=project.id,
                                slots=slots)

import cv2, numpy as np
import os

item = list[0][0]
print('Download the video '+ item.stream)
workdir = '../' + item.id
os.makedirs(workdir, exist_ok=True)
videoPath = os.path.join(workdir, item.name)
videoPath = item.download(local_path=videoPath)

print('Capturing first frame from ' + videoPath)
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
        finish = True
        cv2.destroyAllWindows()
    elif (key >= 48 and key <= 57):
        inputText += str(key - 48)
    elif (key >= 96 and key <= 105):
        inputText += str(key - 96)


# add the inputText as the sample count meta data on the item
item.metadata['user'] = dict()
item.metadata['user']['samples'] = inputText
item.update()