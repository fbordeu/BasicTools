# -*- coding: utf-8 -*-
#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
#
#from BasicTools.Containers.ElementNames import ElementsInfo

def GetGeneratedFiles(prefix = "cpp_src/"):
    """Get the list of generated files for this generator"""
    return (prefix + "FE/GeneratedIntegrationsRules.cpp",)

def Generate(prefix = "cpp_src/"):
    from cpp_generators.Tools import PrintHeader, PrintToFile, PrintFillMatrix
    import BasicTools.FE.IntegrationsRules as IR

    """Run the generation of cpp file using the prefix"""
    filename = prefix +  "FE/GeneratedIntegrationsRules.cpp"

    with open(filename, 'w', encoding="utf8") as cppfile:
        PrintHeader(cppfile)
        PrintToFile(cppfile,"#include <map>")
        PrintToFile(cppfile,"#include <stdexcept>")
        PrintToFile(cppfile,"#include <cmath>")
        PrintToFile(cppfile,"#include <LinAlg/EigenTypes.h>")
        PrintToFile(cppfile,"#include <FE/Space.h>")
        PrintToFile(cppfile,"#include <FE/IntegrationRule.h>")
        PrintToFile(cppfile,"using std::pow;")
        PrintToFile(cppfile,"using namespace BasicTools;")
        PrintToFile(cppfile,"""
namespace BasicTools {

std::map<std::string,SpaceIntegrationRule>  GetPythonDefinedIntegrationRules(){
    std::map<std::string,SpaceIntegrationRule> res;
""")
        for k,v in IR.IntegrationRulesAlmanac.items():

            PrintToFile(cppfile,f"""    {{ // working on {k}
            SpaceIntegrationRule ir; """)
            for k2,v2 in v.items():
                PrintToFile(cppfile,f"""        {{ // working on {k2}
                IntegrationRule eir;""")
                PrintFillMatrix(cppfile,12*" "+"eir.p", v2[0])
                PrintFillMatrix(cppfile,12*" "+"eir.w", v2[1])
                PrintToFile(cppfile,12*" "+f"""ir.storage["{k2}"] = eir;""" )
                PrintToFile(cppfile,8*" "+"}")
            PrintToFile(cppfile,8*" "+f"""res["{k}"] = ir;""" )
            PrintToFile(cppfile,8*" "+"}")
        PrintToFile(cppfile,"""
    return res;
};

std::map<std::string,SpaceIntegrationRule> IntegrationRulesAlmanac = GetPythonDefinedIntegrationRules();
};// BasicTools namespace
""")

if __name__ == '__main__':# pragma: no cover
    Generate()
