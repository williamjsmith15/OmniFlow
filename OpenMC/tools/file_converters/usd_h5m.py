from typing import Iterable
from pxr import Usd
from vertices_to_h5m import vertices_to_h5m
import numpy as np
import os

# Name of file changeable for ease of testing... default should be 'dagmc.usd'
# fname_root = 'dagmc' # Default
# fname_root = 'Test_1_Bucket' # TESTING
# fname_root = 'Test_2_MilkJug' # TESTING
# fname_root = 'Test_3_RubixCube' # TESTING
fname_root = 'Test_4_DonutOnCube' # TESTING

# Grab the filepath of the usd file
def find_files(filename): # TODO: find a better way to search for this rather than search from root (lazy implementation)
    search_path = os.path.abspath("/")
    result = []

    # Walking top-down from the root
    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result

# USD Helper Functions
def getValidProperty (primative, parameterName):
    # Get param
    prop = primative.GetProperty(parameterName)
    
    # Test validity
    if ( type(prop) == type(Usd.Attribute())): # is valid
        return prop.Get()
    else: # is not
        print("Requested parameter is not valid!")
        return None
        #raise Exception("Requested parameter is not valid!")

def getProperty (primative, parameterName): # Unsafe 
    # Get param
    prop = primative.GetProperty(parameterName).Get()

    return prop

def propertyIsValid (primative, parameterName):
    # Get param
    prop = primative.GetProperty(parameterName)
    
    # Test validity
    if ( type(prop) == type(Usd.Attribute())): # is valid
        return True
    else:
        return False




class USDtoDAGMC:
    '''
    Class to convert USD to h5m file format usable for DAGMC, for use with OpenMC
    '''
    def __init__(self):
        # Initialise with blank numpy arrays
        self.vertices       = np.array([])
        self.triangles      = []
        self.material_tags  = []

    def add_USD_file(self, filename: str = fname_root + '.usd'):
        '''
        Load parts form USD into class with their associated material tags and then converts to triangles for use 
        in the conversion script

        Args:
            filename: filename used to import the USD file with
        '''

        #TODO: Add in material tags handling - just sorting out the acutal geometry at the moment

        stage_file = filename
        stage = Usd.Stage.Open(stage_file)
        volumeOffset = 0 # Required as all vertices have to be in a global 1D array (all volumes) => this offsets the indexing
                         # for each individual volume as all vertices for new volumes are added into the same array as previous
                         # volumes (vertices is 1D, triangles is 2D with 2nd dimension have the number of volumes in)
        matCount = 1 #TEMP MAT FIX

        for primID, x in enumerate(stage.Traverse()):
            primType = x.GetTypeName()
            print(f"PRIM: {str(primType)}")
            print(f'PrimID is {primID}')

            if str(primType) == 'Mesh':
                # GET MATERIAL NAME HERE - NEEDED FOR MATERIALS STUFF LATER - IMPLEMENTED ONLY WITH DUMMY MAT NAMES SO FAR

                # Get num of vertecies in elements
                allVertexCounts  = np.array(getValidProperty(x,"faceVertexCounts"))
                allVertexIndices = np.array(getValidProperty(x,"faceVertexIndices"))

                # Get if there is rotation or translation of the meshes
                rotation = [0,0,0] if not propertyIsValid(x,"xformOp:rotateXYZ") else list(getProperty(x,"xformOp:rotateXYZ"))
                translation = np.array([0,0,0]) if not propertyIsValid(x,"xformOp:translate") else np.array(list(getProperty(x,"xformOp:translate")))
                print(f'Rotation is {rotation}')    # Not currently doing anything with rotation - will keep an eye and see if its an issue
                print(f'Translation is {translation}')
                
                newVertices = np.array(getValidProperty(x,"points"), dtype='float64') + translation # Assign vertices here and add translation to the vertexes - fixes meshes at the origin issue 
                if self.vertices.size == 0: # For first run though just set vertices to newVertices array
                    self.vertices = newVertices
                else:
                    self.vertices = np.append(self.vertices, newVertices, axis=0)

                globalCount = 0
                extraPointCount = 0
                endOfVolumeIdx = np.size(self.vertices,0)
                trianglesForVolume = np.array([], dtype="int")

                for Count in allVertexCounts:
                    if Count == 3:      # Triangle
                        a, b, c = globalCount, globalCount+1, globalCount+2
                        # For explanation of +volumeOffset see initialisation of volumeOffset variable
                        if trianglesForVolume.size == 0: # This whole shenanegans is because i dont know how to use numpy arrays properly.... LEARN
                            trianglesForVolume = np.array([[allVertexIndices[a]+volumeOffset, allVertexIndices[b]+volumeOffset, allVertexIndices[c]+volumeOffset]])
                        else:
                            trianglesForVolume = np.append(trianglesForVolume, np.array([[allVertexIndices[a]+volumeOffset, allVertexIndices[b]+volumeOffset, allVertexIndices[c]+volumeOffset]]), axis=0)
                    elif Count == 4:    # Quadrilateral => Split into 2 triangles
                        a, b, c, d = globalCount, globalCount+1, globalCount+2, globalCount+3
                        if trianglesForVolume.size == 0:
                            trianglesForVolume = np.array([[allVertexIndices[a]+volumeOffset, allVertexIndices[b]+volumeOffset, allVertexIndices[c]+volumeOffset]])
                        else:
                            trianglesForVolume = np.append(trianglesForVolume, np.array([[allVertexIndices[a]+volumeOffset, allVertexIndices[b]+volumeOffset, allVertexIndices[c]+volumeOffset]]), axis=0)
                        #Think this may cause issues with some quadrilaterials being split into 2 triangles that overlap and leave a gap - see latex doc
                        trianglesForVolume = np.append(trianglesForVolume, np.array([[allVertexIndices[a]+volumeOffset, allVertexIndices[c]+volumeOffset, allVertexIndices[d]+volumeOffset]]), axis=0) 
                    elif Count > 4:     # n points to triangles
                        indices = np.array([allVertexIndices[globalCount+i]+volumeOffset for i in range(Count)]) # Get array of indices of points 
                        points = np.array([self.vertices[idx] for idx in indices]) # Get points that match those indices
                        # Find mifddle of n-sided polygon => can make triangles from every edge to centre point and add to end of vertices matrix
                        self.vertices = np.append(self.vertices, np.array([[np.average(points[:,dir]) for dir in range(3)]]), axis=0) 
                        
                        centrePointIdx = endOfVolumeIdx + extraPointCount
                        extraPointCount += 1 # Just added an extra point into the vertices array

                        for triangleNum in range(Count):
                            if triangleNum == Count - 1: # Last triangle
                                trianglesForVolume = np.append(trianglesForVolume, np.array([[indices[0], indices[triangleNum], centrePointIdx]]), axis=0)
                            else:
                                if trianglesForVolume.size == 0:
                                    trianglesForVolume = np.array([[indices[triangleNum], indices[triangleNum+1], centrePointIdx]])
                                else:
                                    trianglesForVolume = np.append(trianglesForVolume, np.array([[indices[triangleNum], indices[triangleNum+1], centrePointIdx]]), axis=0)
                    else:
                        print(f"I don't know what to do with a {Count} count yet...")
                    
                    globalCount += Count

                
                self.triangles.append(trianglesForVolume)
                self.material_tags.append(f"mat{matCount}") #TEMP MAT FIX
                matCount += 1 #TEMP MAT FIX
                shapeVertices = np.shape(newVertices)
                volumeOffset += shapeVertices[0] + extraPointCount # Account for all points plus any extras added in from Counts>4

            else:
                print(f"I don't know what to do with a {str(primType)} yet...")
            
            print("\n\n")

    def save_to_h5m(self, filename: str = fname_root + '.h5m'):
        '''
        Use the verticies saved in the class to convert to h5m using the vertices_to_h5m mini package
        https://github.com/fusion-energy/vertices_to_h5m

        Args:
            filename: Filename to save the h5m file, default will be dagmc.h5m (as this is the format required by DAGMC)
        '''

        vertices_to_h5m(
            vertices=self.vertices,
            triangles=self.triangles,
            material_tags=self.material_tags,
            h5m_filename=filename,
        )

filepath = find_files(fname_root + '.usd')
convert = USDtoDAGMC()
convert.add_USD_file(filename = filepath[0])
convert.save_to_h5m()