import sys

# pat = '{}'.format(__file__.replace("hooks", ""))
# print pat
# sys.path.append(pat)  # make it possible to type lib infront of modules inported from the lis

from codeskResource.create_shared_project_parameter import SharedParameters
from UI.xamlFiles.SetProjectInfo import SetProjectInfo

SharedParameters()

SetProjectInfo("SetProjectInfo.xaml")
