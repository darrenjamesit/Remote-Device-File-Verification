$user = Read-Host "enter the desired username here"
$device = Read-Host "enter the hostname here, it's best if you use the FQHN"

#modified to not need to modify the script with the username and device name but rather input them when running the script

#run the script with: 
#.\\total_files_remote.ps1 -user "abc" -device "123.host.com"

$extensions = @(
    #put all the extensions you want to count here
    #by default i have these, just uncomment them
    #    ".pdf",".ppt",".pptx",".csv",".xls",".xlsx",".doc",".docx",".rtf",
    #".zip",".7z",".txt",".asc",".mpp",".wri",".msg",".one",".vsd",
    #".vsdx",".pst",".jpg",".mp4"
)
 
Invoke-Command -ComputerName $device -ScriptBlock {
    param($user, $exts)
 
    $path = "C:\Users\$user"
 
    $count = Get-ChildItem $path -Recurse -File -ErrorAction SilentlyContinue |
             Where-Object { $exts -contains $_.Extension.ToLower() } |
             Measure-Object |
             Select-Object -ExpandProperty Count
 
    [PSCustomObject]@{
        User  = $user
        Path  = $path
        Files = $count
    }
 
} -ArgumentList $user, $extensions
