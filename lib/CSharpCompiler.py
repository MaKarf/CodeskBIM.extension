import clr
import System
from System.CodeDom.Compiler import CompilerParameters, CompilerResults
from Microsoft.CSharp import CSharpCodeProvider


def compile_csharp_code(csharp_code, output_dll):
    code_provider = CSharpCodeProvider()
    parameters = CompilerParameters(System.Array[str](["System.dll"]), output_dll)

    # Compile the C# code
    results = code_provider.CompileAssemblyFromSource(parameters, csharp_code)

    # Check for compilation errors
    if results.Errors.Count > 0:
        for error in results.Errors:
            print("Error: {0}".format(error))
    else:
        print("Compilation successful. DLL created: {0}".format(output_dll))


# Example C# code
csharp_code = """
using System;

public class ExampleClass
{
    public static void HelloWorld()
    {
        Console.WriteLine("Hello, World!");
    }
}
"""


def compile_multiple_csharp_codes(csharp_codes, output_dll):
    code_provider = CSharpCodeProvider()

    # Concatenate all C# codes
    full_code = "\n".join(csharp_codes)

    parameters = CompilerParameters(System.Array[str](["System.dll"]), output_dll)

    # Compile the concatenated C# code
    results = code_provider.CompileAssemblyFromSource(parameters, full_code)

    # Check for compilation errors
    if results.Errors.Count > 0:
        for error in results.Errors:
            print("Error: {0}".format(error))
    else:
        print("Compilation successful. DLL created: {0}".format(output_dll))


# Example C# codes (multiple classes)
csharp_codes = [
    """
    using System;

    public class ExampleClass1
    {
        public static void HelloWorld()
        {
            Console.WriteLine("Hello from ExampleClass1!");
        }
    }
    """,
    """
    using System;

    public class ExampleClass2
    {
        public static void Greet()
        {
            Console.WriteLine("Greetings from ExampleClass2!");
        }
    }
    """
]

if __name__ == "__main__":
    # Output DLL path
    output_dll = "CombinedDLL.dll"

    # Compile the multiple C# codes into a single DLL
    compile_multiple_csharp_codes(csharp_codes, output_dll)

if __name__ == "__main__":
    # Output DLL path
    output_dll = "ExampleDLL.dll"

    # Compile the C# code to a DLL
    compile_csharp_code(csharp_code, output_dll)
