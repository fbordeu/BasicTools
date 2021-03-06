# distutils: language = c++
#cython: language_level=3
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#

import cython
import numpy as np
cimport numpy as np
from cython.operator cimport dereference as deref

testcharacter = "'"

cimport BasicTools.FE.WeakForms.NativeNumericalWeakForm as NNWF
from BasicTools.CythonDefs cimport CBasicIndexType

cdef class PyWeakTerm:
    #cdef NNWF.WeakTerm* _c_WeakTerm

    def __cinit__(self):
       self._c_WeakTerm = new NNWF.WeakTerm()
       self.pointerOwner = True
       if self._c_WeakTerm is NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self._c_WeakTerm is not NULL and self.pointerOwner == True:
            del self._c_WeakTerm

    cdef NNWF.WeakTerm* GetCppPointer(self):
        return self._c_WeakTerm

    cdef PyWeakTerm copy(self):
        res = PyWeakTerm()
        res.fieldName = self.fieldName
        res.derCoordName = self.derCoordName
        res.derDegree = self.derDegree
        res.constant = self.constant
        res.normal = self.normal
        res.spaceIndex_ = self.spaceIndex_
        res.derCoordIndex_ = self.derCoordIndex_
        res.numberingIndex_ = self.numberingIndex_
        res.valuesIndex_ = self.valuesIndex_
        res.internalType = self.internalType
        res.spaceIndex_ = self.spaceIndex_
        return res

    @staticmethod
    cdef PyWeakTerm create(NNWF.WeakTerm* ptr):
        obj = <PyWeakTerm>PyWeakTerm.__new__(PyWeakTerm) # create instance without calling __init__
        obj._c_WeakTerm = ptr
        obj.pointerOwner = False
        return obj

    @property
    def derDegree(self):
        return self._c_WeakTerm.derDegree

    @derDegree.setter
    def derDegree(self, value):
        self._c_WeakTerm.derDegree = value

    @property
    def fieldName(self):
        return self._c_WeakTerm.fieldName.decode()

    @fieldName.setter
    def fieldName(self, value):
        self._c_WeakTerm.fieldName = value.encode()

    @property
    def derCoordName(self):
        return self._c_WeakTerm.derCoordName.decode()

    @derCoordName.setter
    def derCoordName(self, value):
        self._c_WeakTerm.derCoordName = value.encode()

    @property
    def derCoordIndex_(self):
        return self._c_WeakTerm.derCoordIndex_

    @derCoordIndex_.setter
    def derCoordIndex_(self, value):
        self._c_WeakTerm.derCoordIndex_ = value

    @property
    def constant(self):
        return self._c_WeakTerm.constant

    @constant.setter
    def constant(self, value):
        self._c_WeakTerm.constant = value

    @property
    def spaceIndex_(self):
        return self._c_WeakTerm.spaceIndex_

    @spaceIndex_.setter
    def spaceIndex_(self, value):
        self._c_WeakTerm.spaceIndex_ = value

    @property
    def numberingIndex_(self):
        return self._c_WeakTerm.numberingIndex_

    @numberingIndex_.setter
    def numberingIndex_(self, value):
        self._c_WeakTerm.numberingIndex_ = value

    @property
    def normal(self):
        return self._c_WeakTerm.normal

    @normal.setter
    def normal(self, value):
        self._c_WeakTerm.normal = value

    @property
    def valuesIndex_(self):
        return self._c_WeakTerm.valuesIndex_

    @valuesIndex_.setter
    def valuesIndex_(self, value):
        self._c_WeakTerm.valuesIndex_ = value

    @property
    def modeIndex_(self):
        return self._c_WeakTerm.modeIndex_

    @modeIndex_.setter
    def modeIndex_(self, value):
        self._c_WeakTerm.modeIndex_ = value

    @property
    def numberingIndex_(self):
        return self._c_WeakTerm.numberingIndex_

    @numberingIndex_.setter
    def numberingIndex_(self, value):
        self._c_WeakTerm.numberingIndex_ = value

    @property
    def internalType(self):
        return self._c_WeakTerm.internalType

    @internalType.setter
    def internalType(self, value):
        self._c_WeakTerm.internalType = value

    def __str__(self):
        res = ""
        if self.derDegree > 0 and self.normal == 0 :
#            #res += "d" + self.fieldName + "/"  + "d"  + str(self.derCoordName)
            res += "Derivative("+str(self.fieldName)+", "+str(self.derCoordName)+")"
        else:
            res += self.fieldName
        return res

    @property
    def EnumError(self):
        return -1

    @property
    def EnumNormal(self):
        return 0

    @property
    def EnumConstant(self):
        return 1

    @property
    def EnumUnknownField(self):
        return 2

    @property
    def EnumTestField(self):
        return 3

    @property
    def EnumExtraField(self):
        return 4

    @property
    def EnumExtraIPField(self):
        return 5



cdef class PyWeakMonom:
    #cdef NNWF.WeakMonom* _c_WeakMonom

    def __cinit__(self):
        self.pointerOwner = True
        self._c_WeakMonom = new NNWF.WeakMonom()
        if self._c_WeakMonom is NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self._c_WeakMonom is not NULL and self.pointerOwner == True:
            del self._c_WeakMonom

    def copy(self):
        res = PyWeakMonom()
        res._c_WeakMonom.prefactor = self._c_WeakMonom.prefactor
        for i in range(self.GetNumberOfProds()):
            res._c_WeakMonom.prod.push_back(deref(self.GetProd(i).copy().GetCppPointer() ))
        return res

    cpdef  hasVariable(self,str var):
        for m in self :
            if m.fieldName == str(var):
                return True
        return False

    cpdef AddProd(self,PyWeakTerm term):
        term.pointerOwner = False
        self._c_WeakMonom.prod.push_back(deref(term.GetCppPointer()))

    cpdef CBasicIndexType GetNumberOfProds(self):
        return self._c_WeakMonom.prod.size()

    cdef PyWeakTerm GetProd(self, CBasicIndexType n):
        cdef NNWF.WeakTerm* res = &self._c_WeakMonom.prod[n]
        return PyWeakTerm.create(res)

    cdef NNWF.WeakMonom* GetCppPointer(self):
        return self._c_WeakMonom

    @staticmethod
    cdef PyWeakMonom create(NNWF.WeakMonom* ptr):
        obj = <PyWeakMonom>PyWeakMonom.__new__(PyWeakMonom) # create instance without calling __init__
        obj._c_WeakMonom = ptr
        obj.pointerOwner = False
        return obj

    @property
    def prefactor(self):
        return self._c_WeakMonom.prefactor

    @prefactor.setter
    def prefactor(self, value):
        self._c_WeakMonom.prefactor = value


    def __str__(self):
        res = str(self._c_WeakMonom.prefactor)
        for i in range(self.GetNumberOfProds()):
            res += "*"
            res += str(self.GetProd(i))
        return res

    def __iter__(self):
        return PyWeakMonomIter(self)

cdef class PyWeakForm:
    #cdef NNWF.WeakForm* _c_WeakForm

    def __cinit__(self):
        self.pointerOwner = False
        self._c_WeakForm = new NNWF.WeakForm()
        if self._c_WeakForm is NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self._c_WeakForm is not NULL and self.pointerOwner == True:
            del self._c_WeakForm

    cdef NNWF.WeakForm* GetCppPointer(self):
        return self._c_WeakForm

    cpdef AddTerm(self,PyWeakMonom monom):
        monom.pointerOwner = False
        self._c_WeakForm.form.push_back(deref(monom.GetCppPointer()))

    cpdef CBasicIndexType GetNumberOfTerms(self):
        return self._c_WeakForm.GetNumberOfTerms()

    cpdef PyWeakMonom GetMonom(self, int n):
        cdef NNWF.WeakMonom* res = &self._c_WeakForm.form[n]
        return PyWeakMonom.create(res)

    def GetRightPart(self,list unknownvars):
        res = PyWeakForm()
        for p in self:
            for uv in unknownvars:
                if p.hasVariable(uv):
                    break
            else:
                res.AddTerm(p)
        return res

    def  GetLeftPart(self,list unknownvars):
        res = PyWeakForm()
        for p in self:
            tocopy = False
            for uv in unknownvars:
               if p.hasVariable(uv):
                    tocopy =True
                    break
            if tocopy:
                res.AddTerm(p)
        return res

    def __str__(self):
        res = ""
        for i in range(self.GetNumberOfTerms()):
            res +=str(self.GetMonom(i))   + "\n"
        return res


    @staticmethod
    cdef PyWeakForm create(NNWF.WeakForm* ptr):
        obj = <PyWeakForm>PyWeakForm.__new__(PyWeakForm) # create instance without calling __init__
        obj._c_WeakForm = ptr
        return obj

    def __iter__(self):
        return PyWeakFormIter(self)

cdef class PyWeakFormIter():
    def __init__(self,PyWeakForm father):
        self.index = father.GetNumberOfTerms()
        self.father = father

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.father.GetMonom(self.index)

    def next(self):
        return self.__next__()


cdef class PyWeakMonomIter():
    def __init__(self,PyWeakMonom father):
        self.index = father.GetNumberOfProds()
        self.father = father

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.father.GetProd(self.index)

    def next(self):
        return self.__next__()

def CheckIntegrity(GUI=False):
    F = PyWeakForm()
    M = PyWeakMonom()
    T = PyWeakTerm()
    T.fieldName = "u"
    M.AddProd(T)
    F.AddTerm(M)

    for term in F:
        print(term)

    return 'OK'

