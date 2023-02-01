# This is a sample Python script.
import json


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/.

import dtlpy as dl

project = dl.projects.get(project_name='project2')
if project is None :
    project = dl.projects.create(project_name='project2')
    dl.projects.checkout(project_name='project2')

dataset = project.datasets.get(dataset_name='dataset2')
if dataset is None :
    dataset = dl.datasets.create(dataset_name='dataset2')

filters = dl.Filters()
filters.add(field='name', values='cat.jpg')
list = dataset.items.list(filters=filters)
# Count the items
imageCount = list.items_count
print('Number of items in dataset: {}'.format(imageCount))

if imageCount == 0 :
    dataset.items.upload(local_path="C:/Users/forro/Downloads/cat.jpg")

catItem = list[0][0]

catItem.metadata['user'] = dict()
catItem.metadata['user']['foo'] = 'bar'
catItem.update()


catLabel = dataset.add_label(label_name='cat', color=(34, 6, 231))

builder = catItem.annotations.builder()
builder.add(annotation_definition=dl.Classification(label='cat'))
catItem.annotations.upload(builder)

if imageCount == 1 :
    dataset.items.upload(local_path="C:/Users/forro/Downloads/cat2.jpg")

filters = dl.Filters()
filters.add(field='name', values='cat2.jpg')
list = dataset.items.list(filters=filters)
imageCount = list.items_count
print('Number of items in dataset: {}'.format(imageCount))

if imageCount == 1 :
    #get second image of the first page
    catItem2 = list[0][0]
    catItem2.metadata['user'] = {}
    catItem2.metadata['user']['foo'] = 'bar2'
    catItem2.update()

with open("filter.json","r") as f:
    x = json.load(f)
    filters = dl.Filters(custom_filter=x)
    #filters = dl.Filters(custom_filter={"$and":[{"hidden":False},
    #            {"type":"file"}]},)
    list = dataset.items.list(filters=filters)
    # Count the items
    imageCount = list.items_count
    print('Number of filtered items in dataset: {}'.format(imageCount))