$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$projectPrefix = $projectRoot.TrimEnd('\') + '\'
$releaseDir = Join-Path $projectRoot 'outputs'
$releaseZip = Join-Path $releaseDir 'veritas-genlayer-studio-tested.zip'
New-Item -ItemType Directory -Force -Path $releaseDir | Out-Null
if (Test-Path $releaseZip) { Remove-Item -LiteralPath $releaseZip }
$excluded = @('node_modules','dist','outputs','work','.git')
$files = Get-ChildItem -LiteralPath $projectRoot -File -Recurse | Where-Object {
  $relative = $_.FullName.Substring($projectPrefix.Length)
  -not ($excluded | Where-Object { $relative -eq $_ -or $relative.StartsWith("$_\") -or $relative.Contains("\$_\") }) -and
  -not $relative.EndsWith('.zip') -and -not $relative.EndsWith('.log') -and
  -not ($_.Name -eq '.env.local' -or $_.Name -eq '.env')
}
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [IO.Compression.ZipFile]::Open($releaseZip, 'Create')
try {
  foreach ($file in $files) {
    $entry = $file.FullName.Substring($projectPrefix.Length).Replace('\','/')
    [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $file.FullName, $entry, 'Optimal') | Out-Null
  }
} finally { $archive.Dispose() }
Write-Output $releaseZip

