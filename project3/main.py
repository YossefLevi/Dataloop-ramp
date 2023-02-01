# This is a sample Python script.

import dtlpy as dl

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#import hashlib

def multiHashFunc():
    import hashlib
    for i in range(100000):
        s = "<iteration" + str(i) + ">"
        hashedString = hashlib.sha256(s.encode())
        print(hashedString)


project = dl.projects.get(project_name='project3')

# Service might exist from previous run of this script.
# we will delete it and deploy it again to ensure we have the latest function
try:
    project.services.delete(service_name='hashit')
except:
    print ("no service with the name hashit")
    service = project.services.deploy(func=multiHashFunc,
                                  service_name='hashit')

execution = service.execute(project_id=project.id,
                            item_id=0,
                            function_name='multiHashFunc')
execution.logs(follow=True)
execution = execution.wait()
print(execution.latest_status)
