
$curDir = $PSScriptRoot
$curUser = $env:UserName

Write-Host "Installing Python 3.7.4, Paths, Dependancies and Launching App"
Write-Host "Current Working Directory: $curDir"
# This is the link to download Python 3.7.4 from Python.org
# See https://www.python.org/downloads/
$pythonUrl = "https://www.python.org/ftp/python/3.7.4/python-3.7.4-amd64.exe"

# This is the directory that the exe is downloaded to
$tempDirectory = "C:\temp_provision\"


# Installation Directory
# Some packages look for Python here
$targetDir = "C:\Users\$curUser\AppData\Local\Programs\Python\Python37"
Write-Host "Checking for Python 3.7.4 in" $targetDir
# create the download directory and get the exe file
$pythonNameLoc = $tempDirectory + "python-3.7.4-amd64.exe"
New-Item -ItemType directory -Path $tempDirectory -Force | Out-Null
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Write-Host "Downloading Python 3.7.4"
(New-Object System.Net.WebClient).DownloadFile($pythonUrl, $pythonNameLoc)

# These are the silent arguments for the install of python
# See https://docs.python.org/3/using/windows.html
$Arguments = @()
$Arguments += "/i"
$Arguments += 'InstallAllUsers=0 Include_launcher=1 Include_test=0 Include_pip=1 AssociateFiles=0'
$Arguments += "/passive"

#Install Python
Write-Host "Installing Python 3.7.4"
Start-Process $pythonNameLoc -ArgumentList $Arguments -Wait

Function Get-EnvVariableNameList {
    [cmdletbinding()]
    $allEnvVars = Get-ChildItem Env:
    $allEnvNamesArray = $allEnvVars.Name
    $pathEnvNamesList = New-Object System.Collections.ArrayList
    $pathEnvNamesList.AddRange($allEnvNamesArray)
    return ,$pathEnvNamesList
}

Function Add-EnvVarIfNotPresent {
Param (
[string]$variableNameToAdd,
[string]$variableValueToAdd
   ) 
    $nameList = Get-EnvVariableNameList
    $alreadyPresentCount = ($nameList | Where{$_ -like $variableNameToAdd}).Count
    if ($alreadyPresentCount -eq 0)
    {
    [System.Environment]::SetEnvironmentVariable($variableNameToAdd, $variableValueToAdd, [System.EnvironmentVariableTarget]::Machine)
    [System.Environment]::SetEnvironmentVariable($variableNameToAdd, $variableValueToAdd, [System.EnvironmentVariableTarget]::Process)
    [System.Environment]::SetEnvironmentVariable($variableNameToAdd, $variableValueToAdd, [System.EnvironmentVariableTarget]::User)
        $message = "Enviromental variable added to machine, process and user to include $variableNameToAdd"
    }
    else
    {
        $message = 'Environmental variable already exists. Consider using a different function to modify it'
    }
    Write-Information $message
}

Function Get-EnvExtensionList {
    [cmdletbinding()]
    $pathExtArray =  ($env:PATHEXT).Split("{;}")
    $pathExtList = New-Object System.Collections.ArrayList
    $pathExtList.AddRange($pathExtArray)
    return ,$pathExtList
}

Function Add-EnvExtension {
Param (
[string]$pathExtToAdd
   ) 
    $pathList = Get-EnvExtensionList
    $alreadyPresentCount = ($pathList | Where{$_ -like $pathToAdd}).Count
    if ($alreadyPresentCount -eq 0)
    {
        $pathList.Add($pathExtToAdd)
        $returnPath = $pathList -join ";"
        [System.Environment]::SetEnvironmentVariable('pathext', $returnPath, [System.EnvironmentVariableTarget]::Machine)
        [System.Environment]::SetEnvironmentVariable('pathext', $returnPath, [System.EnvironmentVariableTarget]::Process)
        [System.Environment]::SetEnvironmentVariable('pathext', $returnPath, [System.EnvironmentVariableTarget]::User)
        $message = "Path extension added to machine, process and user paths to include $pathExtToAdd"
    }
    else
    {
        $message = 'Path extension already exists'
    }
}

Function Get-EnvPathList {
    [cmdletbinding()]
    $pathArray =  ($env:PATH).Split("{;}")
    $pathList = New-Object System.Collections.ArrayList
    $pathList.AddRange($pathArray)
    return ,$pathList
}

Function Add-EnvPath {
Param (
[string]$pathToAdd
   ) 
    $pathList = Get-EnvPathList
    $alreadyPresentCount = ($pathList | Where{$_ -like $pathToAdd}).Count
    if ($alreadyPresentCount -eq 0)
    {
        $pathList.Add($pathToAdd)
        $returnPath = $pathList -join ";"
        [System.Environment]::SetEnvironmentVariable('path', $returnPath, [System.EnvironmentVariableTarget]::Machine)
        [System.Environment]::SetEnvironmentVariable('path', $returnPath, [System.EnvironmentVariableTarget]::Process)
        [System.Environment]::SetEnvironmentVariable('path', $returnPath, [System.EnvironmentVariableTarget]::User)
        $message = "Path added to machine, process and user paths to include $pathToAdd"
		Write-Host $returnPath
    }
    else
    {
        $message = 'Path already exists'
    }
    Write-Information $message
}

Write-Host "Adding environment extentions and paths"
Add-EnvExtension '.PY'
Add-EnvExtension '.PYW'
Add-EnvPath $targetDir
Add-EnvPath $targetDir"\Scripts"
Write-Host $message