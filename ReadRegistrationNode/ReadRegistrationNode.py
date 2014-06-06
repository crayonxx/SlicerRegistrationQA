import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# ReadRegistrationNode
#
#Constants that have to be the same in creating Registration Hierarchy
NAME_CT = 'CT'
NAME_WARP = 'WarpedImage'
NAME_VECTOR = 'Vector' #Vector Field from phase to reference phase
NAME_INVVECTOR = 'InvVector' #Vector from reference phase to phase
NAME_ABSDIFF = 'AbsoluteDifference'
NAME_JACOBIAN = 'Jacobian'
NAME_INVERSECONS = 'InverseConsistency'
NAME_REFPHASE = 'ReferenceHierarchyNode'

class ReadRegistrationNode:
  def __init__(self, parent):
    parent.title = "Read Registration Node" # TODO make this more human readable by adding spaces
    parent.categories = ["RegistrationQuality"]
    parent.dependencies = []
    parent.contributors = ["Kristjan Anderle (GSI)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc. and Steve Pieper, Isomics, Inc.  and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['ReadRegistrationNode'] = self.runTest

  def runTest(self):
    tester = ReadRegistrationNodeTest()
    tester.runTest()

#
# qReadRegistrationNodeWidget
#

class ReadRegistrationNodeWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    #
    # Reload and Test area
    #
    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload && Test"
    self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "ReadRegistrationNode Reload"
    reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    # reload and test button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    reloadFormLayout.addWidget(self.reloadAndTestButton)
    self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    ##
    ## input volume selector
    ##
    #self.inputSelector = slicer.qMRMLNodeComboBox()
    #self.inputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    #self.inputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    #self.inputSelector.selectNodeUponCreation = True
    #self.inputSelector.addEnabled = False
    #self.inputSelector.removeEnabled = False
    #self.inputSelector.noneEnabled = False
    #self.inputSelector.showHidden = False
    #self.inputSelector.showChildNodeTypes = False
    #self.inputSelector.setMRMLScene( slicer.mrmlScene )
    #self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    #parametersFormLayout.addRow("Input Volume: ", self.inputSelector)
    #
    # Patient Name
    #
    self.patientName = qt.QLineEdit()     
    self.patientName.setToolTip( "Input patient name" )
    self.patientName.text = 'Patient'
    parametersFormLayout.addRow("Patient Name:", self.patientName)
    #
    # Find CT
    #
    self.selectCT = qt.QPushButton("Select CT file")
    self.selectCT.toolTip = "Find CT file on disk."
    self.selectCT.enabled = True
    parametersFormLayout.addRow(self.selectCT)
    # CT Directory
    self.pathCT = qt.QLineEdit()     
    self.pathCT.setToolTip( "Input the path to CT Directory" )
    self.pathCT.text = ''
    parametersFormLayout.addRow("CT Directory path:", self.pathCT)
    
    # Warp images ctDirectory
    self.pathWarpedImages = qt.QLineEdit()     
    self.pathWarpedImages.setToolTip( "Input the path to warp images ctDirectory" )
    self.pathWarpedImages.text = ''
    parametersFormLayout.addRow("Patient Name:", self.pathWarpedImages)
    
    # Vector fields ctDirectory
    self.pathVectorFields = qt.QLineEdit()     
    self.pathVectorFields.setToolTip( "Input the path to vector fields ctDirectory" )
    self.pathVectorFields.text = ''
    parametersFormLayout.addRow("Patient Name:", self.pathVectorFields)
    
    #
    # Create subject hierarchy
    #
    self.createHierarchyButton = qt.QPushButton("Create Subject Hierarchy")
    self.createHierarchyButton.toolTip = "Create Subject Hierarchy from the CT file on disk."
    self.createHierarchyButton.enabled = True
    parametersFormLayout.addRow(self.createHierarchyButton)

    # connections
    self.selectCT.connect('clicked(bool)', self.onSelectCT)
    self.createHierarchyButton.connect('clicked(bool)', self.onCreateHierarchyButton)
    #self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelectCT(self):
    loadFileName = qt.QFileDialog()
    filePath=loadFileName.getOpenFileName()
    if not filePath == '':
      ctDirectoryName = os.path.dirname(os.path.realpath(filePath))
      self.pathCT.text = ctDirectoryName + '/'
      self.pathWarpedImages.text = ctDirectoryName + '/WarpedImages/'
      self.pathVectorFields.text = ctDirectoryName + '/VectorFields/'
      #self.ctDirectoryName = ctDirectoryName
    else:
      print "No input file"
      
  
  def onCreateHierarchyButton(self):
    logic = ReadRegistrationNodeLogic()
    logic.createHierarchy(self.pathCT.text,self.pathWarpedImages.text,self.pathVectorFields.text,self.patientName.text)

  def onReload(self,moduleName="ReadRegistrationNode"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    globals()[moduleName] = slicer.util.reloadScriptedModule(moduleName)

  def onReloadAndTest(self,moduleName="ReadRegistrationNode"):
    try:
      self.onReload()
      evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
      tester = eval(evalString)
      tester.runTest()
    except Exception, e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(),
          "Reload and Test", 'Exception!\n\n' + str(e) + "\n\nSee Python Console for Stack Trace")


#
# ReadRegistrationNodeLogic
#

class ReadRegistrationNodeLogic:
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    pass

  def createHierarchy(self,ctDirectory,warpDirectory,vectorDirectory,patientName):
    from vtkSlicerSubjectHierarchyModuleMRML import vtkMRMLSubjectHierarchyNode
    from vtkSlicerSubjectHierarchyModuleLogic import vtkSlicerSubjectHierarchyModuleLogic
    try:
      vtkMRMLSubjectHierarchyNode
      vtkSlicerSubjectHierarchyModuleLogic
    except AttributeError:
      import sys
      sys.stderr.write('Unable to create SubjectHierarchy nodes: SubjectHierarchy module not found!')
      return
    
    if not os.path.exists(ctDirectory):
      print ctDirectory + "Doesn't exist"
      return
      
    referencePhase = 0
    
    #Create Patient Node
    subjectNode = vtkMRMLSubjectHierarchyNode()
    subjectNode.SetName(patientName)
    subjectNode.SetLevel('Subject')
    subjectNode.SetAttribute('Directory',ctDirectory)
    slicer.mrmlScene.AddNode(subjectNode)
    #Create Registration node
    registrationNode = vtkMRMLSubjectHierarchyNode()
    registrationNode.SetName('Registration Node')
    registrationNode.SetLevel('Study')
    registrationNode.SetParentNodeID(subjectNode.GetID())
    #Paths to directories
    registrationNode.SetAttribute(NAME_CT+'Directory',ctDirectory)
    registrationNode.SetAttribute('ReferencePhase',str(referencePhase))
    slicer.mrmlScene.AddNode(registrationNode)
    
    
    for fileName in os.listdir(ctDirectory):
      
      
      #Looking for file names that end with 0.0% or 0%
      if not fileName.find('%') > -1:
        print "Cannot find % in file name"
        continue
      numberEnding = '0.0'
      if not fileName.find(numberEnding+'%') > -1:
        numberEnding = '0'
      index = fileName.find(numberEnding+'%')
      if not index > -1:
        print "No ending with 0 in fileName"
        continue
      
      n = 0
      #Try to find out, which phase do we have
      try:
	phase = int(fileName[index-1])
      except:
	print fileName[index-1]
	phase = 0

      #Create New phase in subject hierarchy
      phaseNode = vtkMRMLSubjectHierarchyNode()
      phaseNode.SetParentNodeID(registrationNode.GetID())
      phaseNode.SetName('Phase_'+str(phase)+'0%')
      phaseNode.SetLevel('Series')
      #phaseNode.SetAttribute('DICOMHierarchy.SeriesModality','CT')
      phaseNode.SetAttribute('Directory',ctDirectory)
      #phaseNode.SetOwnerPluginName('Volumes')
      slicer.mrmlScene.AddNode(phaseNode)
      
      #Check if reference phase and link it
      if phase == referencePhase:
        registrationNode.SetAttribute('ReferenceHierarchyNode',phaseNode.GetID())
      
      
      #Create New volume in subject hierarchy
      ctNode = vtkMRMLSubjectHierarchyNode()
      ctNode.SetParentNodeID(phaseNode.GetID())
      ctNode.SetName(NAME_CT)
      ctNode.SetLevel('Subseries')
      ctNode.SetAttribute('DICOMHierarchy.SeriesModality','CT')
      ctNode.SetAttribute('FilePath',ctDirectory+fileName)
      #ctNode.SetOwnerPluginName('Volumes')
      slicer.mrmlScene.AddNode(ctNode)
      numberEnding = '0'
      if os.path.exists(warpDirectory):
	for file in os.listdir(warpDirectory):
          if file.find(str(phase)+numberEnding) > -1:
	    warpNode = vtkMRMLSubjectHierarchyNode()
	    warpNode.SetParentNodeID(phaseNode.GetID())
	    warpNode.SetName(NAME_WARP)
	    warpNode.SetLevel('Subseries')
	    warpNode.SetAttribute('DICOMHierarchy.SeriesModality','CT')
	    warpNode.SetAttribute('FilePath',warpDirectory+file)
	   #warpNode.SetOwnerPluginName('Volumes')
	    slicer.mrmlScene.AddNode(warpNode)
      
      if os.path.exists(vectorDirectory):
	for file in os.listdir(vectorDirectory):
          if file.find(str(phase)+numberEnding) > -1:
	    vectorNode = vtkMRMLSubjectHierarchyNode()
	    vectorNode.SetParentNodeID(phaseNode.GetID())
	    vectorNode.SetName(NAME_VECTOR)
	    vectorNode.SetLevel('Subseries')
	    vectorNode.SetAttribute('FilePath',vectorDirectory+file)
	   #vectorNode.SetOwnerPluginName('Volumes')
	    slicer.mrmlScene.AddNode(vectorNode)
      
	
    #for fileName in os.listdir(fileNameGD):
    print "Subject Hierarchy Created"
    return


class ReadRegistrationNodeTest(unittest.TestCase):
  """
  This is the test case for your scripted module.
  """

  def delayDisplay(self,message,msec=1000):
    """This utility method displays a small dialog and waits.
    This does two things: 1) it lets the event loop catch up
    to the state of the test so that rendering and widget updates
    have all taken place before the test continues and 2) it
    shows the user/developer/tester the state of the test
    so that we'll know when it breaks.
    """
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_ReadRegistrationNode1()

  def test_ReadRegistrationNode1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = ReadRegistrationNodeLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
