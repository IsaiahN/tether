# auto_play23.ps1 stopped at 11:36:51 after step 5's want: line 74 ran want22.sh (my carry slip), which rewrote
# PLAY22's want (byte-identical to PLAY22's PLAY_START files line) and wrote none for PLAY23. Steps 1-4 and step 5's
# head / HW / log_index edits are done and are CHECKED here, not redone (no second backup). Then want23.sh, and steps
# 6-7 exactly as auto_play23.ps1: precheck BelowNormal and waited, every line green, the launch copy detached.
$ErrorActionPreference = 'Stop'
$R = 'C:\TETHER_RUNS\S6_2026-10-19'
$P22 = "$R\PLAY23"; $T = "$R\split\fresh_r29\arc-solver-agent"
$BASH = 'C:\Program Files\Git\bin\bash.exe'
$LOG = "$P22\auto.log"
$H = '26a68e0e23bef27a622ccfa5f86bb01d83f04126'; $G = 'eadee1aa0c5c6f7e24381099d8573f28be254e04'
$HD = 'ffee6c34b59167b6'
function Say($m) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $m" | Out-File -FilePath $LOG -Append -Encoding utf8 }
function Bash($cmd) { & $BASH -c $cmd; if ($LASTEXITCODE -ne 0) { throw "bash rc $LASTEXITCODE : $cmd" } }
try {
    Say "RESUME (want22.sh -> want23.sh at line 74; steps 1-5 checked, not redone)"
    if ((& git -C $T rev-parse HEAD).Trim() -ne $H) { throw "clone HEAD != H" }
    if (((& git -C $T diff --name-only $G HEAD) -join ',') -ne 'README.md') { throw "diff vs G not README.md" }
    if ((Get-Content "$P22\head.txt" -Raw).Trim() -ne $HD) { throw "head.txt != $HD" }
    $s = [IO.File]::ReadAllText("$P22\precheck.sh")
    if (-not ($s -match "(?m)^HW=$HD") -or -not $s.Contains('PLAY22/round_02/stream.jsonl')) { throw "precheck.sh HW / verify path not set" }
    if (Test-Path "$P22\play_chain.want") { throw "PLAY23 want exists" }
    Bash "bash /c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/want23.sh"
    Say "HEAD $HD; HW set; log_index verify on PLAY22/round_02; want $((Get-Content "$P22\play_chain.want" -Raw).Trim())"
    $pc = Start-Process -FilePath $BASH -ArgumentList "C:/TETHER_RUNS/S6_2026-10-19/PLAY23/precheck.sh" -WindowStyle Hidden -PassThru
    $pc.PriorityClass = 'BelowNormal'
    $pc.WaitForExit()
    $pl = Get-Content "$P22\precheck.log"
    Say "PRECHECK $($pl.Count) lines"
    if (-not ($pl -match ' END$')) { throw "precheck has no END" }
    if ($pl -match 'GATE FAIL') { throw "precheck GATE FAIL: $(($pl -match 'GATE FAIL') -join ' | ')" }
    foreach ($l in ($pl -match ' rc ')) { if ($l -notmatch ' rc 0 ') { throw "precheck red: $l" } }
    $u = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
    if (Test-Path "$P22\chain.log") { throw "PLAY23 chain.log exists" }
    Copy-Item "$P22\play_chain.sh" "$P22\play_chain.launched.$u.sh"
    $p = Start-Process -FilePath $BASH -ArgumentList "C:/TETHER_RUNS/S6_2026-10-19/PLAY23/play_chain.launched.$u.sh" -RedirectStandardOutput "$P22\play_chain.out" -RedirectStandardError "$P22\play_chain.err" -WindowStyle Hidden -PassThru
    $p.PriorityClass = 'BelowNormal'
    Say "LAUNCHED play_chain.launched.$u.sh pid $($p.Id)"
    Say "DONE"
} catch {
    Say "STOPPED: $($_.Exception.Message)"
    exit 2
}
