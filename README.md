* Getting started (UI) 
Login to platform, create a dataset, upload an image containing cat, add label containing cat and then: Classify the entire image as cat Clone the image and use bounding box to classify the cat Clone the image and use polygon to segment the cat SDK Install our python sdk login using the cli create script that: create project and dataset (dataset2) upload the cat image to the dataset (image1) add metadata field called "foo" with the value "bar" classify the image with adding annotation of cat
upload second cat image (image2) to the dataset with metadata field called "foo" with the value "bar2" Search (UI) using the UI search for all items with metadata key foo == bar2 make sure you see only one image (image2)

* SDK search (UI and SDK) 
Take the DQL filter of the previous step from UI Using the filter json query the dataset and make sure a single image is returned (image2) . add classification of cat to this image search all images containing labels of cat, you should see two now

* Clone (UI) 
Clone image1 without annotations but with metadata into new dataset (dataset3) clone image 2 with annotations bt without metadata into the same dataset (dataset3) using the SDK search on dataset3 items with label cat or metadata key foo=bar, raise python exception is count is not 2

* Hello function 
Code a simple function calculating sha256 100K times of the string "", where X is the index of the current iteration number. run it make sure the CPU is busy. Upload this function into dataloop platform create an execution of the function (i.e. run it remotely) print to console progress watch CPU & RAM in UI remove the function from the system

* Trigger & Modality 
Using opencv, write a function that converts color image to grayscale image create dataset, dataset1 Upload the function to platform and set up a trigger that for every image uploaded to dataset another image is created as grey scale. make the grey scale image as modality image of the original image open the original image in UI, see switch to modality using the UI button remove the function

* Toolbar, and configuration 
Using opencv, write a function that is sampling frames from video. Users provide as input the amount of expected frames when running. function samples in unified rate to prove the needed amount. create dataset, dataset2 Upload the function to the platform and add a button to activate it on the dataset browser. samples are saved in the original folder of the image with the name <video_file_name>_smaples as subfolder run the function, make sure samples are generated remove the function

* Concurrency(Threads on the same machine) 
Run the hello function in step 1 for 1M iterations, use higher concurrency and instance type to cut the execution time by 25%.

* Concurrency(Different machines) 
Run the hello function in step 1 for 10M iterations, in parallel batches of 100K, allow 4 machines.
