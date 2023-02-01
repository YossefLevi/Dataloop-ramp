# This is a sample Python script.
import dtlpy as dl

# below code was taken from https://dataloop.ai/docs/faas-tutorial
def rgb2gray(item: dl.Item):
    import cv2
    import numpy as np
    buffer = item.download(save_locally=False)
    bgr = cv2.imdecode(np.frombuffer(buffer.read(), np.uint8), -1)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    gray_item = item.dataset.items.upload(local_path=gray,
                                         remote_path='/gray' + item.dir,
                                         remote_name=item.filename)
    # add modality
    item.modalities.create(name='gray',
                          ref=gray_item.id)
    item.update(system_metadata=True)


try:
    project = dl.projects.get(project_name='project3')
except:
    project = dl.projects.create(project_name='project3')

dl.projects.checkout(project_name='project3')

try :
    dataset = project.datasets.get(dataset_name='task2_dataset1')
    print('found task2_dataset1')
except:
    dataset = dl.datasets.create(dataset_name='task2_dataset1')
    print('created task2_dataset1')


try:
    project.services.delete(service_name='grayit')
except:
    print ("no service with the name grayit")

service = project.services.deploy(func=rgb2gray,
                                  service_name='grayit')

service.triggers.create(name='graynewitem',
                      execution_mode=dl.TriggerExecutionMode.ONCE,
                      resource='Item',
                      actions='Created',
                      function_name='rgb2gray',
                      filters={'$and': [{'hidden': False},
                                        {"datasetId": dataset.id},
                                        {'type': 'file'}]}
                      )

dataset.items.upload(local_path="C:/Users/forro/Downloads/cat2.jpg")