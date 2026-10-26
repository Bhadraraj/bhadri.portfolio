# Regenerate delivery assets from original PNGs. Requires FFmpeg on PATH.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$htmlPath = Join-Path $root 'index.html'
$html = [IO.File]::ReadAllText($htmlPath)
$active = [regex]::Replace($html, '<!--[\s\S]*?-->', '')
$sources = [regex]::Matches($active, '(?:src|data-bg-src)="(?:\./)?(assets/img/[^"\s]+\.(?:png|webp))"') | ForEach-Object { $_.Groups[1].Value -replace '\.webp$', '.png' } | Sort-Object -Unique
$before = 0
$after = 0
foreach ($source in $sources) {
    $inputPath = Join-Path $root $source
    $output = $source -replace '\.png$', '.webp'
    $outputPath = Join-Path $root $output
    $arguments = @('-y', '-v', 'error', '-i', $inputPath)
    if ($source.Contains('/practice-projects/')) { $arguments += @('-vf', "scale='min(1200,iw)':-1") }
    $arguments += @('-c:v', 'libwebp', '-quality', '85', '-compression_level', '6', $outputPath)
    & ffmpeg @arguments
    if ($LASTEXITCODE -ne 0) { throw "Image conversion failed: $source" }
    $before += (Get-Item -LiteralPath $inputPath).Length
    $after += (Get-Item -LiteralPath $outputPath).Length
    $html = $html.Replace($source, $output)
}
[IO.File]::WriteAllText($htmlPath, $html, [Text.UTF8Encoding]::new($false))
[PSCustomObject]@{ Images = $sources.Count; OriginalBytes = $before; OptimizedBytes = $after; Reduction = [math]::Round((1 - $after / $before) * 100) }
