# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

import numpy as np

import BasicTools.Containers.ElementNames as EN
from BasicTools.IO.ReaderBase import ReaderBase
from BasicTools.NumpyDefs import PBasicIndexType

def ReadStl(fileName=None,string=None):
    obj = StlReader()
    obj.SetFileName(fileName)
    obj.SetStringToRead(string)
    res = obj.Read()
    return res

def LoadSTLWithVTK(filenameSTL):
    from vtkmodules.vtkIOGeometry import vtkSTLReader
    readerSTL = vtkSTLReader()
    readerSTL.SetFileName(filenameSTL)
    # 'update' the reader i.e. read the .stl file
    readerSTL.Update()

    polydata = readerSTL.GetOutput()

    # If there are no points in 'vtkPolyData' something went wrong
    if polydata.GetNumberOfPoints() == 0:
        raise ValueError("No point data could be loaded from '" + filenameSTL)# pragma: no cover

    return polydata

class StlReader(ReaderBase):
    def __init__(self,fileName = None):
        super(StlReader,self).__init__()

    def Read(self, fileName=None,string=None,out=None):

      if fileName is not None:
          self.SetFileName(fileName)

      if string is not None:
          self.SetStringToRead(string)


      # check if binary
      self.readFormat = "rb"
      self.StartReading()

      header = ""
      #read the first non space caracters to detect if binary or not
      while len(header) < 5:
          data = self.filePointer.read(1)
          if data[0] < 128:
            if chr(data[0]) == " ":
              continue
            header += chr(data[0])

      if header == "solid":
          self.PrintVerbose("Ascii File")
          return self.ReadStlAscii()
      else:
          self.PrintVerbose("Binary File")
          return self.ReadStlBinary()


    def ReadStlBinary(self):
        # from https://en.wikipedia.org/wiki/STL_(file_format)#Binary_STL

        self.readFormat = "rb"
        self.StartReading()

        import BasicTools.Containers.UnstructuredMesh as UM

        header = self.readData(80,np.int8)
        try:
           header = ''.join([(chr(item) if item < 128 else " ")  for item in header])
           print("HEADER : '" + header + "'")
        except:
           pass
        nbTriangles = self.readInt32()
        print("reading  : " + str(nbTriangles) + " triangles")

        resUM = UM.UnstructuredMesh()

        #resUM.nodes = np.empty((nbTriangles*3,3), dtype=float)

        dt = np.dtype([('normal', (np.float32,3)),
                       ('points', (np.float32,9)),
                       ('att', (np.int16)),
                       ])

        data = self.readData(nbTriangles,dt)
        normals = np.array(data["normal"])
        resUM.nodes = np.array(data["points"])
        resUM.nodes.shape = (nbTriangles*3,3)

        elements = resUM.GetElementsOfType(EN.Triangle_3)
        elements.connectivity = np.array(range(resUM.GetNumberOfNodes()),dtype=PBasicIndexType)
        elements.connectivity.shape = (nbTriangles,3)
        elements.originalIds = np.arange(nbTriangles,dtype=PBasicIndexType)
        elements.cpt = nbTriangles
        resUM.elemFields["normals"] = normals
        self.EndReading()
        resUM.GenerateManufacturedOriginalIDs()
        resUM.PrepareForOutput()

        return resUM

    def ReadStlAscii(self):

        self.readFormat = "r"
        self.StartReading()


        import BasicTools.Containers.UnstructuredMesh as UM

        resUM = UM.UnstructuredMesh()

        name = self.ReadCleanLine().split()[1];

        p = []
        normals = np.empty((0,3), dtype=float)
        nodesbuffer = []
        while True:
            line = self.ReadCleanLine()
            if not line:
                break

            l = line.strip('\n').lstrip().rstrip()
            if l.find("facet")>-1 :
                if l.find("normal")>-1 :
                 normals = np.concatenate((normals, np.fromstring(l.split("normal")[1],sep=" ")[np.newaxis]),axis=0)
                 continue
            if l.find("outer loop")>-1 :
              for i in range(3):
                line = self.ReadCleanLine()
                l = line.strip('\n').lstrip().rstrip()
                if l.find("vertex")>-1 :
                  p.append(np.fromstring(l.split("vertex")[1],sep=" ") )
              if len(p) == 3:
                nodesbuffer.extend(p)
                #resUM.nodes = np.vstack((resUM.nodes,p[0][np.newaxis,:],p[1][np.newaxis,:],p[2][np.newaxis,:]))
                p = []
              else:# pragma: no cover
                print("error: outer loop with less than 3 vertex")
                raise

        self.EndReading()


        resUM.nodes = np.array(nodesbuffer)
        del nodesbuffer
        elements = resUM.GetElementsOfType(EN.Triangle_3)
        elements.connectivity = np.array(range(resUM.GetNumberOfNodes()),dtype=PBasicIndexType)
        elements.connectivity.shape = (resUM.GetNumberOfNodes()//3,3)
        elements.originalIds = np.arange(resUM.GetNumberOfNodes()/3,dtype=PBasicIndexType)
        elements.cpt = elements.connectivity.shape[0]
        resUM.elemFields["normals"] = normals
        resUM.GenerateManufacturedOriginalIDs()
        resUM.PrepareForOutput()

        return resUM


from BasicTools.IO.IOFactory import RegisterReaderClass
RegisterReaderClass(".stl",StlReader)



def CheckIntegrity():
    data = """   solid cube_corner
          facet normal 0.0 -1.0 0.0
            outer loop
              vertex 0.0 0.0 0.0
              vertex 1.0 0.0 0.0
              vertex 0.0 0.0 1.0
            endloop
          endfacet
          facet normal 0.0 0.0 -1.0
            outer loop
              vertex 0.0 0.0 0.0
              vertex 0.0 1.0 0.0
              vertex 1.0 0.0 0.0
            endloop
          endfacet
          facet normal -1.0 0.0 0.0
            outer loop
              vertex 0.0 0.0 0.0
              vertex 0.0 0.0 1.0
              vertex 0.0 1.0 0.0
            endloop
          endfacet
          facet normal 0.577 0.577 0.577
            outer loop
              vertex 1.0 0.0 0.0
              vertex 0.0 1.0 0.0
              vertex 0.0 0.0 1.0
            endloop
          endfacet
        endsolid
"""


    res = ReadStl(string=data)
    print(res)
    if res.GetNumberOfNodes() != 12: raise Exception()
    if res.GetNumberOfElements() != 4: raise Exception()

    from BasicTools.Helpers.Tests import TestTempDir
    tempdir = TestTempDir.GetTempPath()
    f =open(tempdir+"test_input_stl_data.stl","w")
    f.write(data)
    f.close()
    res = ReadStl(fileName=tempdir+"test_input_stl_data.stl")

    try:
        import vtk
        print('reading mesh using vtk')
        mesh = LoadSTLWithVTK(tempdir+"test_input_stl_data.stl")
        print(mesh)
    except:# pragma: no cover
        print("warning : error importing vtk, disabling some tests ")
        pass
    from BasicTools.TestData import GetTestDataPath


    print("Binary reading")
    res1 = ReadStl(fileName=GetTestDataPath()+"coneBinary.stl")
    print (res1)

    print("Ascii reading")
    res2 = ReadStl(fileName=GetTestDataPath()+"coneAscii.stl")
    print (res2)

    if res1.GetNumberOfNodes() != res2.GetNumberOfNodes(): raise Exception()

    # 1e-6 because the ascii file has only 6 decimals
    if np.max(abs(res1.nodes -  res2.nodes)) > 1e-6 : raise Exception()

    if res1.GetNumberOfElements() !=res2.GetNumberOfElements(): raise Exception()

    conn1 = res1.GetElementsOfType(EN.Triangle_3).connectivity
    conn2 = res2.GetElementsOfType(EN.Triangle_3).connectivity

    if not np.all(np.equal(conn1,conn2)) : raise Exception()

    return 'ok'

if __name__ == '__main__':
    print(CheckIntegrity())# pragma: no cover






