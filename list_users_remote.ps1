$device = Read-Host "Enter the FQHN or ipv4 address"
wmic /node:"$device" path win32_userprofile get localpath

# run it .\\list_users_remote.ps1 -device "123.host.com" or "192.168.1.1"
