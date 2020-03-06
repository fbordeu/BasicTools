# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#
from sympy import Symbol,Function,trace
from sympy.matrices import Matrix

testcharacter = "'"
space = Matrix([Symbol('x'),Symbol('y'), Symbol("z")])



def GetNormal(size):
    return GetField("Normal",size)

def GetConstant(name,size=1):
    if size == 1:
      return Symbol(name)
    else:
        res = []
        for i in range(size):
            res.append(Symbol(name+"_"+str(i)))
        return (Matrix([res])).T

def GetTestField(name,size,sdim=3,extraCoordinates=[]):
    return GetField(name,size,star=True,sdim=sdim,extraCoordinates=extraCoordinates)

def GetField(name,size,star=False,sdim=3,extraCoordinates=[]):
    res = []
    suffix = ""
    if star:
        suffix = testcharacter
    s = space[0:sdim]
    s.extend(extraCoordinates)

    if size == 1:
        if len(s) == 0:
            res.append(Function(name+suffix))
        else:
            res.append(Function(name+suffix)(*s))
    else:
        for i in range(size):
            res.append(Function(name+"_"+str(i)+suffix)(*s))
    return (Matrix([res])).T

def Inner(a,b):
    return a.T*b


def Trace(arg):
    return Matrix([trace(arg)])

def Divergence(arg,sdim=3):
    return Trace(Gradient(arg,sdim=sdim) )

def Gradient(arg,sdim=3):
    shape = arg.shape[0]
    res = [[0]*shape for i in range(sdim)]
    for s in range(shape):
        for d in range(sdim):
            res[d][s] = arg[s].diff(space[d])
    return Matrix(res)

def Strain(arg ,sdim=3):
    G = Gradient(arg,sdim)
    return (G+G.T)/2

def ToVoigtEpsilon(arg):
    """ we use yamma for shear

    """
    if arg.shape[0] ==3:
        return Matrix([arg[0,0],arg[1,1],arg[2,2],2*arg[1,2],2*arg[0,2],2*arg[0,1], ])
    if arg.shape[0] ==2:
        return Matrix([arg[0,0],arg[1,1],2*arg[0,1]])
    if arg.shape[0] ==1:
        return Matrix([arg[0,0]])
    raise()

def ToVoigtSigma(arg):
    if arg.shape[0] ==3:
        return Matrix([arg[0,0],arg[1,1],arg[2,2],arg[1,2],arg[0,2],arg[0,1], ])
    if arg.shape[0] ==2:
        return Matrix([arg[0,0],arg[1,1],arg[0,1]])
    if arg.shape[0] ==1:
        return Matrix([arg[0,0]])
    raise()

def GetMassWeakForm(name="u",dim=3):
    u = GetField(name,dim)
    ut = GetTestField(name,dim)
    ener = u.T*ut
    return ener

def GetMecaElasticProblem(name="u",dim=3,K=None,planeStress=True):
    u = GetField("u",dim)
    ut = GetTestField("u",dim)
    if K is None:
        from BasicTools.FE.MaterialHelp import HookeIso
        K = HookeIso(1,0.3,dim, planeStress)
    ener = ToVoigtEpsilon(Strain(u,dim)).T*K*ToVoigtEpsilon(Strain(ut,dim))
    return ener

def GetMecaNormalPressure(flux="p",name="u", dim=3):
    ut = GetTestField(name,dim)
    if isinstance(flux,str):
        p = GetConstant(flux)
    else:
        p = float(flux)

    from BasicTools.FE.SymWeakForm import GetNormal
    Normal = GetNormal(dim)

    wflux = p*Normal.T*ut
    return wflux

def CheckIntegrity(GUI=False):
    from sympy import pprint
    #init_session()

    print(space)

    u = GetField("u",3)
    u0 = GetField("u0",3)

    ut = GetTestField("u",3)
    f = GetField("f",3)
    alpha = Symbol("alpha")

    globalconstant = GetField("g",1,sdim=0)
    print(globalconstant )


    print(u)
    print(u.shape)
    print(u.diff(Symbol("x")))
    print(ut.diff(Symbol("x")))
    print("-----------------")
    pprint(u,use_unicode=GUI)
    pprint(Gradient(u),use_unicode=GUI)

    pprint(Strain(u),use_unicode=GUI)
    pprint(u[0].diff(space[1]),use_unicode=GUI)


    from BasicTools.FE.MaterialHelp import HookeIso
    K = HookeIso(1,0.3)
    pprint(K,use_unicode=GUI)

    ener = ToVoigtEpsilon(Strain(u+u0)).T*K*ToVoigtEpsilon(Strain(ut))+ f.T*ut*alpha
    pprint(ener,use_unicode=GUI)

    return "OK"

if __name__ == '__main__':
    print(CheckIntegrity(GUI=True))# pragma: no cover