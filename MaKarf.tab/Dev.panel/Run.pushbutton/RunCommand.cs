using System;
using System.IO;
using System.Text;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;


namespace CodeskBIMRevit
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    [Journaling(JournalingMode.NoCommandData)]

    public class RunCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {

            // Create a StringBuilder to build the final string
            StringBuilder stringBuilder = new StringBuilder();

            try
            {
                
                UIApplication _revit = commandData.Application;
                string _basePath = FilesPath.extension_path;
                string _WpfPath = Path.Combine(FilesPath.ironPython_engine_dll_lib_path, "IronPython.Wpf.dll");
                string _codeskDLL = Path.Combine(FilesPath.addins_folder, "2021", FilesPath.namespaceName, $"{FilesPath.namespaceName}2021.dll");
                
                // Create an IronPython runtime
                //var flags = new Dictionary<string, object>() { { "Frames", true }, { "FullFrames", true } };
                
                // Create a IronPython runtime and engine
                var runtime = Python.CreateRuntime();
                var engine = runtime.GetEngine("python");


                // Create a Python script scope
                var scope = engine.CreateScope();

                // Redirect the standard output and error streams
                var output = new MemoryStream();
                var error = new MemoryStream();
                engine.Runtime.IO.SetOutput(output, Encoding.UTF8);
                engine.Runtime.IO.SetErrorOutput(error, Encoding.UTF8);



                // Add IronPython's Lib folder to sys.path  
                engine.Execute("import sys\nsys.path.append(r'E:\\CodeskBIMRevitAddinSetup\\pyCodeskKitchen\\niddativermibksedoc\\IronPythonEngine\\\\IronPython 2.7\\Lib')\nsys.path.append(r'E:\\CodeskBIMRevitAddinSetup\\pyCodeskKitchen\\niddativermibksedoc\\CodeskBIM.extension')", scope);
                
                

                //add special variable: __revit__ to be globally visible everywhere:
                var builtin = Python.GetBuiltinModule(engine);
                builtin.SetVariable("__revit__", _revit);

                engine.Runtime.LoadAssembly(typeof(Document).Assembly);
                engine.Runtime.LoadAssembly(typeof(TaskDialog).Assembly);

                builtin.SetVariable("__basePath__", _basePath);
                builtin.SetVariable("__WpfPath__", _WpfPath);
                builtin.SetVariable("__codeskDLL__", _codeskDLL);
                
                    try
                    {
                        var global_variable = AppMethods.GetFromRegistry(FilesPath.global_variable_key);

                        if (AppMethods.BinaryStringToDate(global_variable) == "True")
                        {                          

                            try
                            {
                                // Execute the Python script
                                var result = engine.ExecuteFile(@"E:\CodeskBIMRevitAddinSetup\pyCodeskKitchen\niddativermibksedoc\CodeskBIM.extension\MaKarf.tab\Dev.panel\Run.pushbutton\codesk.py", scope);

                                // Get the captured print messages
                                var outputText = Encoding.UTF8.GetString(output.ToArray());
                                //var errorText = Encoding.UTF8.GetString(error.ToArray());

                                if (outputText.Length != 0)
                                {
                                    AppMethods.Print(commandData: commandData, printText: outputText);
                                } 
                            }

                            catch (Exception ex)
                            {                                
                                // Capture and write the traceback
                                var traceback = engine.GetService<ExceptionOperations>().FormatException(ex);
                                
                                if (traceback.Length != 0)
                                {
                                    AppMethods.Print(commandData: commandData, errorText: traceback);;
                                }

                                //AppMethods.ErrorEngine(@"E:\CodeskBIMRevitAddinSetup\pyCodeskKitchen\niddativermibksedoc\CodeskBIM.extension\MaKarf.tab\Dev.panel\Run.pushbutton\codesk.py");

                            }   
                        }

                        else
                        {
                            AppMethods.LicenseFailure();
                        }
                        
                    }

                    catch (Exception ex)
                    {
                        AppMethods.ExceptionErrorMessage(ex);
                    }


                return Result.Succeeded;
            }
            catch (Exception e)
            {            

                AppMethods.ExceptionErrorMessage(e);
                return Result.Failed;

            }
        }




    }
}
