# distutils: language = c++
#cython: language_level=3

from libcpp.vector cimport vector

cimport numpy as np


cimport BasicTools.FE.WeakForms.NativeNumericalWeakForm as NNWF

cdef extern from "src_cpp/NativeIntegration.cpp":
    pass

# Decalre the class with cdef

cdef extern from "src_cpp/NativeIntegration.h" :
    cdef cppclass MonoElementsIntegralCpp:
        MonoElementsIntegralCpp() except +
        void SetNumberOfUnkownFields(int)
        void SetUnkownOffset(int,int)
        void SetTotalUnkownDofs(int)

        void SetNumberOfTestFields(int)
        void SetTestOffset(int,int)
        void SetTotalTestDofs(int)

        void SetNumberOfConstants(int)
        void SetConstants(int,double)

        void AllocateWorkingElementVIJ(int size)

        void SetNumberOfIntegrationPoints(int)
        void SetIntegrationPointI(int, double,double,double,double)
        int totalUnkownDofs,totalTestDofs

        void SetComputeNormal(int)
        void SetDomainToTreat()
        void SetPoints(double*, int, int)
        void SetConnectivity(np.int_t*, int, int)

        void SetNumberOfSpaces(int)
        void InitSpaceS(const int& s,
                 const int& dim ,
                 const int& NumberOfShapeFunctions,
                 const int& numberOfIntegrationPoints )
        void SetSpaceSvalNI(const int& spaceNumber,
                      const int& integrationPoint,
                      double* pd)
        void SetSpaceSvaldphidxiI(const int& spaceNumber,
                      const int& integrationPoint,
                      double* pd)


        void SetNumberOfNumberings(int i)
        void SetNumberingI(int i, int n, int m,np.int_t* ip)
        void SetNumberOfValues(int i)
        void SetValueI(int i, int n, int m, double* dp)

        void SetNumberOfIPValues(int i)
        void SetIPValueI(int i, int n, int m, double* dp)

        void SetLocalOffsets(int, vector[double]&,vector[int]&,int, vector[double]&,vector[int]&)
        void Integrate(NNWF.WeakForm*, vector[int])
        double* vK
        np.int_t* iK
        np.int_t* jK
        double* F
        int totalvijcpt
        bint onlyEvaluation
        int  geoSpaceNumber
