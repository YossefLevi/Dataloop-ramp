# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import torch
import dtlpy as dl
import os

if dl.token_expired():
    dl.login()

# Download YOLOv5 from PyTorch Hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# cat is class number 15 and dog is class number 16 in YOLO model
print('using YOLO to detect ' + model.names[15] +' and '+ model.names[16])


project = dl.projects.get(project_name='project5')
dataset = project.datasets.get(dataset_name='task3_dataset2')
filters = dl.Filters()
filters.add(field='type', values='file')
pages = dataset.items.list(filters=filters)
# Count the items
imageCount = pages.items_count
print('Number of items in dataset: {}'.format(imageCount))

workdir = 'downloads'
os.makedirs(workdir, exist_ok=True)

for page in pages:
    for item in page:
        imagePath = os.path.join(workdir, item.name)
        imagePath = item.download(local_path=imagePath)
        print(item.name)

        results = model([imagePath])
        for boxDetected in results.xyxy[0]:
            # each element is of 6 numbers corner1(x,y), Corner2(x,y), Confidence score, Class
            #print(boxDetected)
            classification = int(boxDetected[5])
            if ((classification == 15) or (classification == 16)):
                #use SDK to draw the box over the item
                if (classification == 15) :
                    label = 'Cat'
                else:
                    label = 'Dog'
                print('found ' + label)
                builder = item.annotations.builder()
                builder.add(
                    annotation_definition=dl.Box(left=int(boxDetected[0]),
                                                 top=int(boxDetected[1]),
                                                 right=int(boxDetected[2]),
                                                 bottom=int(boxDetected[3]),
                                                 label=label))
                # upload annotations to item
                builder.upload()


