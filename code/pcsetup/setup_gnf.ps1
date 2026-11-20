# GNF PC setup (Captain Spike, Nov 19 2026). Works ONLY inside the GNF folder on the Desktop.
# 1) checks the graphics card  2) installs ComfyUI portable into GNF  3) writes gnf_report.txt
# Nothing is bought, nothing outside GNF is touched. Models are added later, sized to the card.
$ErrorActionPreference = "Stop"
$GNF = Join-Path ([Environment]::GetFolderPath("Desktop")) "GNF"
if (!(Test-Path $GNF)) { $GNF = Join-Path $env:USERPROFILE "OneDrive\Desktop\GNF" }
if (!(Test-Path $GNF)) { Write-Host "GNF folder not found on the Desktop." -ForegroundColor Red; Read-Host "Press Enter"; exit 1 }
$R = Join-Path $GNF "gnf_report.txt"
"GNF setup report  $(Get-Date)" | Out-File $R
# --- 1. GPU
try {
  $g = & nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
  "GPU: $g" | Tee-Object -FilePath $R -Append
} catch {
  "GPU: nvidia-smi not found (no NVIDIA card or driver missing)" | Tee-Object -FilePath $R -Append
  Get-CimInstance Win32_VideoController | ForEach-Object { "Video: $($_.Name)  $([math]::Round($_.AdapterRAM/1GB,1)) GB" } | Tee-Object -FilePath $R -Append
}
"RAM: $([math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB)) GB" | Tee-Object -FilePath $R -Append
"Free space on GNF drive: $([math]::Round((Get-PSDrive ($GNF.Substring(0,1))).Free/1GB)) GB" | Tee-Object -FilePath $R -Append
# --- 2. ComfyUI portable (latest official release, found through the GitHub API)
$dst = Join-Path $GNF "ComfyUI_windows_portable"
if (Test-Path $dst) { "ComfyUI: already installed" | Tee-Object -FilePath $R -Append }
else {
  $rel = Invoke-RestMethod "https://api.github.com/repos/comfyanonymous/ComfyUI/releases/latest"
  $a = $rel.assets | Where-Object { $_.name -match "portable" -and $_.name -match "nvidia" -and $_.name -match "\.7z$" } | Select-Object -First 1
  if (!$a) { $a = $rel.assets | Where-Object { $_.name -match "portable.*\.7z$" } | Select-Object -First 1 }
  "ComfyUI: downloading $($a.name) ($([math]::Round($a.size/1MB)) MB) from release $($rel.tag_name)" | Tee-Object -FilePath $R -Append
  $z = Join-Path $GNF $a.name
  Invoke-WebRequest $a.browser_download_url -OutFile $z
  try { tar -xf $z -C $GNF } catch {
    winget install --id 7zip.7zip -e --accept-source-agreements --accept-package-agreements
    & "$env:ProgramFiles\7-Zip\7z.exe" x $z "-o$GNF" -y
  }
  Remove-Item $z
  "ComfyUI: installed to $dst" | Tee-Object -FilePath $R -Append
}
"DONE. Captain Spike picks the video model once he reads this report." | Tee-Object -FilePath $R -Append
Read-Host "All set. Press Enter to close"
