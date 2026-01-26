$readyFile = "$env:LOCALAPPDATA\PixelPouch\.debugpy_ready"

$timeout = 60
$elapsed = 0

while (-not (Test-Path $readyFile)) {
    Start-Sleep -Milliseconds 500
    $elapsed += 0.5

    if ($elapsed -ge $timeout) {
        throw "Timeout waiting for debugpy ready: $readyFile"
    }
}
