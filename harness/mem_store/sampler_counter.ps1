# The 1 s commit sampler for a run that does not start one itself (the reviewer 2026-10-19 05:50: not Python).
# Finds OUR probe_counter process(es) whose command line names the given out dir (the venv launcher and the real
# interpreter both match; each is sampled), then writes every second: t_s, pid, private bytes. Read only; ends
# when every matched process has exited, or after 90 s if none appears. args: out_dir_fragment out_tsv
param([string]$Frag, [string]$Out)
$t0 = Get-Date
$procs = @()
while ($procs.Count -eq 0 -and ((Get-Date) - $t0).TotalSeconds -lt 90) {
    $ids = Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
        Where-Object { $_.CommandLine -like "*probe_counter.py*" -and $_.CommandLine -like "*$Frag*" } |
        ForEach-Object { $_.ProcessId }
    $procs = @($ids | ForEach-Object { [System.Diagnostics.Process]::GetProcessById($_) })
    if ($procs.Count -eq 0) { Start-Sleep -Milliseconds 500 }
}
"t_s`tpid`tprivate_B" | Out-File -FilePath $Out -Encoding ascii
while (@($procs | Where-Object { -not $_.HasExited }).Count -gt 0) {
    $t = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
    foreach ($p in $procs) {
        if (-not $p.HasExited) {
            $p.Refresh()
            "$t`t$($p.Id)`t$($p.PrivateMemorySize64)" | Out-File -FilePath $Out -Append -Encoding ascii
        }
    }
    Start-Sleep -Milliseconds 1000
}
