Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the current directory
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Check if Python is installed
On Error Resume Next
WshShell.Run "python --version", 0, True
If Err.Number <> 0 Then
    MsgBox "ERROR: Python is not installed. Please install Python from https://python.org", vbCritical, "ProfilePop"
    WScript.Quit
End If
On Error GoTo 0

' Install required packages silently
WshShell.Run "cmd /c cd /d """ & currentDir & """ && pip install pillow winshell pywin32 --user --quiet", 0, True

' Launch ProfilePop without console window
WshShell.Run "pythonw """ & currentDir & "\ProfilePop.py""", 0, False

Set WshShell = Nothing
Set fso = Nothing
