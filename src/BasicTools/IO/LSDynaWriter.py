# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

import numpy as np

from BasicTools.IO.WriterBase import WriterBase as WriterBase
import BasicTools.Containers.ElementNames as EN
from BasicTools.NumpyDefs import PBasicIndexType
from BasicTools.NumpyDefs import PBasicFloatType
import os

def WriteMeshToK(filename,mesh, normals= None):
    OW = KWriter()
    OW.Open(filename)
    OW.Write(mesh, normals=normals)
    OW.Close()

BasicToolToLSDyna = dict()
BasicToolToLSDyna[EN.Tetrahedron_4] = [0,1,2,3,3,3,3,3]

class KWriter(WriterBase):
    def __init__(self):
        super(KWriter,self).__init__()
    def __str__(self):
        res  = 'KWriter : \n'
        res += '   FileName : '+str(self.fileName)+'\n'
        return res

    def Write(self,meshObject,PointFieldsNames=None,PointFields=None,CellFieldsNames=None,CellFields=None,GridFieldsNames=None,GridFields=None):

        #Header
        self.writeText("$# LS-DYNA Keyword file\n*KEYWORD\n*TITLE\n"+str(os.path.basename(self.fileName))+"\n")

        #Node tags
        for i, tag in enumerate(meshObject.nodesTags):
            self.writeText("*SET_NODE_LIST\n")
            self.writeText("$#     sid\n")
            self.writeText(str(i+1).rjust(10)+"\n")
            self.writeText("$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8\n")
            listOfIds = [tag.GetIds()[j:j+8] for j in range(0, len(tag.GetIds()), 8)]
            for line in listOfIds:
                node_line = ""
                for ind in line:
                    node_line += str(ind+1).rjust(10)
                self.writeText(node_line + "\n")

        #Elements
        for name, data in meshObject.elements.items():
            self.writeText("*ELEMENT_SOLID\n")
            elementHeader = "$#   eid     pid"
            try:
                BTtoDynaConv = BasicToolToLSDyna[name]
            except KeyError:
                raise("Element "+name+" not compatible with writer")
            for i in range(len(BTtoDynaConv)):
                elementHeader += "      n"+str(i+1)
            self.writeText(elementHeader + "\n")
            for i, conn in enumerate(data.connectivity):
                elem_line = str(i+1).rjust(8)
                elem_line += str(1).rjust(8)
                for ind in BTtoDynaConv:
                    elem_line += str(conn[ind]+1).rjust(8)
                self.writeText(elem_line+"\n")

        #Nodes
        numberofpoints = meshObject.GetNumberOfNodes()
        posn = meshObject.GetPosOfNodes()
        self.writeText("*NODE\n")
        self.writeText("$#   nid               x               y               z      tc      rc\n")
        for n in range(numberofpoints):
            node_line = str(n+1).rjust(8)
            for pos in posn[n]:
                node_line += str(pos).rjust(16)
            # rc tc always 0
            node_line += str(0).rjust(8) + str(0).rjust(8) + "\n"
            self.writeText(node_line)

        self.writeText("*END")

from BasicTools.IO.IOFactory import RegisterWriterClass
RegisterWriterClass(".k",KWriter)

def CheckIntegrity():
    import BasicTools.Containers.UnstructuredMesh as UM

    from BasicTools.Helpers.Tests import TestTempDir

    tempdir = TestTempDir.GetTempPath()

    mymesh = UM.UnstructuredMesh()
    mymesh.nodes = np.array([[0.1,0,0],
                             [1,0,0],
                             [0,1,0],
                             [1,1,0],
                             [0.5,0,0.1],
                             [0,0.5,0.1],
                             [0.5,0.5,0.1],
    ],dtype=PBasicFloatType)
    mymesh.originalIDNodes = np.array([1, 3, 4, 5, 6, 7, 8],dtype=PBasicIndexType)

    tet = mymesh.GetElementsOfType(EN.Tetrahedron_4)
    tet.AddNewElement([0,1,2,3],0)
    tet.AddNewElement([1,2,3,4],1)
    tet.AddNewElement([2,3,4,5],2)

    mymesh.AddNodeToTagUsingOriginalId(1,"NodeTest")
    mymesh.AddNodeToTagUsingOriginalId(3,"NodeTest")
    mymesh.AddNodeToTagUsingOriginalId(8,"NodeTest")

    OW = KWriter()
    OW.Open(tempdir+"Test_LSDynaWriter.k")
    OW.Write(mymesh)
    OW.Close()

    res = open(tempdir+"Test_LSDynaWriter.k").read()

    ref = """$# LS-DYNA Keyword file
*KEYWORD
*TITLE
Test_LSDynaWriter.k
*SET_NODE_LIST
$#     sid
         1
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         1         2         7
*ELEMENT_SOLID
$#   eid     pid      n1      n2      n3      n4      n5      n6      n7      n8
       1       1       1       2       3       4       4       4       4       4
       2       1       2       3       4       5       5       5       5       5
       3       1       3       4       5       6       6       6       6       6
*NODE
$#   nid               x               y               z      tc      rc
       1             0.1             0.0             0.0       0       0
       2             1.0             0.0             0.0       0       0
       3             0.0             1.0             0.0       0       0
       4             1.0             1.0             0.0       0       0
       5             0.5             0.0             0.1       0       0
       6             0.0             0.5             0.1       0       0
       7             0.5             0.5             0.1       0       0
*END"""

    assert(res == ref)

    return "ok"

if __name__ == '__main__':
    print(CheckIntegrity())# pragma: no cover
