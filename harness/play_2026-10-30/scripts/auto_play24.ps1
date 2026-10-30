# auto_play23.ps1 carried to PLAY23 -> PLAY24 (r440 item 4), started ONCE on the reviewer's verify of the spy fix: the
# SAME trees (G eadee1a, H 26a68e0), the SPY pin moved to the fixed kind_spy.py 0df3871e1b49935b; PLAY23 ended on its
# own fault rule at round 1 (the spy fault, ruled by r440) with its STOP file placed; the verified lineage backup
# taken, PLAY24's head/want/precheck set, and PLAY24 launched detached only if every precheck line is green. Every
# step is logged to PLAY24\auto.log; any failure stops the script before launch.
# argv: -H <arc-solver-agent tip sha (40)> -G <general-agent tip sha (40)> -Note <what the tree carries>
param([Parameter(Mandatory = $true)][string]$H, [Parameter(Mandatory = $true)][string]$G,
      [Parameter(Mandatory = $true)][string]$Note)
$ErrorActionPreference = 'Stop'
$R = 'C:\TETHER_RUNS\S6_2026-10-19'
$P21 = "$R\PLAY23"; $P22 = "$R\PLAY24"
$CLONE = "$R\split\fresh_r30"; $T = "$CLONE\arc-solver-agent"
$BASH = 'C:\Program Files\Git\bin\bash.exe'
$PY = 'C:\Users\Admin\Documents\GitHub\tether\.venv\Scripts\python.exe'
$SP = 'C:\Users\Admin\AppData\Local\Temp\claude\c--Users-Admin-Documents-GitHub-tether\b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf\scratchpad'
if (Test-Path $P22) { throw "PLAY24 exists" }
New-Item -ItemType Directory -Path $P22 | Out-Null
$LOG = "$P22\auto.log"
function Say($m) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $m" | Out-File -FilePath $LOG -Append -Encoding utf8 }
function Bash($cmd) { & $BASH -c $cmd; if ($LASTEXITCODE -ne 0) { throw "bash rc $LASTEXITCODE : $cmd" } }
try {
    Say "START H=$H G=$G NOTE=$Note"
    # 1. the clone at the arc tip, with M3 and the two junctions (PowerShell, literal paths)
    if (Test-Path $CLONE) { throw "fresh_r30 exists" }
    New-Item -ItemType Directory -Path $CLONE | Out-Null
    Bash "cd /c/TETHER_RUNS/S6_2026-10-19/split/fresh_r30 && git clone --quiet --branch arc-solver-agent https://github.com/IsaiahN/tether.git arc-solver-agent"
    $head = (& git -C $T rev-parse HEAD).Trim()
    if ($head -ne $H) { throw "clone HEAD $head != H $H" }
    $diff = (& git -C $T diff --name-only $G HEAD) -join ','
    if ($diff -ne 'README.md') { throw "diff vs G is [$diff], not README.md" }
    Copy-Item 'C:\Users\Admin\Documents\GitHub\tether\.git\hooks\commit-msg' "$T\.git\hooks\commit-msg"
    New-Item -ItemType Junction -Path "$T\.venv" -Target 'C:\Users\Admin\Documents\GitHub\tether\.venv' | Out-Null
    New-Item -ItemType Junction -Path "$T\environment_files" -Target "$R\wt_ivv\environment_files" | Out-Null
    Say "CLONE fresh_r30 at $head, diff vs G README.md, hook copied, junctions made"
    # 2. PLAY24's files from PLAY23's, with P/T/G/H replaced (FIRST_ROUND=1 already)
    $oldG = 'eadee1aa0c5c6f7e24381099d8573f28be254e04'; $oldH = '26a68e0e23bef27a622ccfa5f86bb01d83f04126'
    foreach ($f in 'play_chain.sh', 'precheck.sh') {
        $s = [IO.File]::ReadAllText("$P21\$f")
        $s = $s.Replace('S6_2026-10-19/PLAY23"', 'S6_2026-10-19/PLAY24"').Replace('split/fresh_r29/', 'split/fresh_r30/')
        $s = $s.Replace("G=$oldG", "G=$G").Replace("H=$oldH", "H=$H")
        $s = $s.Replace('# PLAY23 = PLAY22 on the tree', "# PLAY24 = PLAY23 on the tree arc-solver-agent $($H.Substring(0,7)) ($Note). PLAY23 = PLAY22 on the tree")
        $s = $s.Replace('SPY=0622d0e95995f3b4', 'SPY=0df3871e1b49935b').Replace('= "0622d0e95995f3b4" ] && say "GATE kind_spy.py 0622d0e95995f3b4"', '= "0df3871e1b49935b" ] && say "GATE kind_spy.py 0df3871e1b49935b"')
        if ($s.Contains('0622d0e9')) { throw "$f still pins the old spy 0622d0e9" }
        [IO.File]::WriteAllText("$P22\$f", $s)
    }
    if (-not ([IO.File]::ReadAllText("$P22\play_chain.sh")).Contains('SPY=0df3871e1b49935b')) { throw "play_chain.sh lacks the new SPY pin" }
    if (-not ([IO.File]::ReadAllText("$P22\precheck.sh")).Contains('GATE kind_spy.py 0df3871e1b49935b')) { throw "precheck.sh lacks the new spy gate" }
    Copy-Item "$P21\play_across.py" "$P22\play_across.py"
    # r441: the spy sweep joins the precheck (a frozen copy in PLAY24; red if any kind_spy wrapper is behind its original)
    Copy-Item "$SP\spy_sweep.py" "$P22\spy_sweep.py"
    $pk = [IO.File]::ReadAllText("$P22\precheck.sh")
    $line = 'run spy_sweep "$PY" -B "$P/spy_sweep.py" "$T" "$E/kind_spy.py"' + "`n"
    $pk2 = $pk.Replace('say "arms summary:', $line + 'say "arms summary:')
    if ($pk2 -eq $pk -or -not $pk2.Contains('run spy_sweep ')) { throw "precheck.sh: the spy_sweep line not inserted" }
    [IO.File]::WriteAllText("$P22\precheck.sh", $pk2)
    foreach ($f in 'play_chain.sh', 'precheck.sh') {
        $s = [IO.File]::ReadAllText("$P22\$f")
        if ($s.Contains('PLAY23"') -or $s.Contains("fresh_r29/") -or ($oldG -ne $G -and $s.Contains("G=$oldG")) -or ($oldH -ne $H -and $s.Contains("H=$oldH"))) { throw "$f still names PLAY23 / fresh_r29 / old G or H" }
        if (-not $s.Contains("G=$G") -or -not $s.Contains("H=$H")) { throw "$f lacks the new G or H" }
    }
    Say "FILES play_chain.sh, precheck.sh (P/T/G/H replaced), play_across.py copied"
    # 3. PLAY23's PLAY_END: it ended on its own fault rule at round 1 (the spy fault, r440), with the STOP file placed;
    #    exactly that one STOP line is accepted, any other STOP condition stops this script
    if (-not (Test-Path "$P21\STOP")) { throw "PLAY23 has no STOP file" }
    Say "waiting for PLAY23's PLAY_END"
    while (-not (Select-String -Path "$P21\chain.log" -Pattern 'PLAY_END' -Quiet)) { Start-Sleep -Seconds 30 }
    $tail = (Get-Content "$P21\chain.log" -Tail 4) -join ' | '
    Say "PLAY23 ended: $tail"
    $stops = @((Get-Content "$P21\chain.log" -Tail 6) -match 'STOP round|STOP free disk')
    if ($stops.Count -ne 1 -or $stops[0] -ne 'STOP round 1 agent_fault events 1') { throw "PLAY23 ended on an unexpected STOP condition: $($stops -join ' | ')" }
    # 4. the verified backup at PLAY23's last verified head
    $hd = (Get-Content "$P21\head.txt" -Raw).Trim()
    $stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $out = & $PY -B -I "$SP\backup_lineage.py" $stamp $hd "PLAY23's last kept generation (round 1 WRITE VERIFIED, 2bf2d6b6); the chain stopped on its fault rule (the spy fault, the reviewer r440); before PLAY24" 2>&1
    if ($LASTEXITCODE -ne 0) { throw "backup rc $LASTEXITCODE : $out" }
    Say "BACKUP $out"
    # 5. head, HW, want
    Set-Content -Path "$P22\head.txt" -Value $hd -NoNewline -Encoding ascii
    $s = [IO.File]::ReadAllText("$P22\precheck.sh")
    $s = [regex]::Replace($s, '(?m)^HW=\S+', "HW=$hd")
    $last = (Get-ChildItem "$P21" -Directory -Filter 'round_*' | Where-Object { Test-Path "$($_.FullName)\read.out" } |
             Sort-Object Name | Select-Object -Last 1).Name
    if (-not $last) { throw "no finished PLAY23 round" }
    $s2 = [regex]::Replace($s, 'PLAY22/round_\d+/stream\.jsonl', "PLAY23/$last/stream.jsonl")
    if ($s2 -eq $s -or -not $s2.Contains("PLAY23/$last/stream.jsonl")) { throw "log_index verify path not replaced" }
    [IO.File]::WriteAllText("$P22\precheck.sh", $s2)
    Bash "bash /c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/want24.sh"
    Say "HEAD $hd; HW set; log_index verify on PLAY23/$last; want $((Get-Content "$P22\play_chain.want" -Raw).Trim())"
    # 6. the precheck, BelowNormal, waited here (this script is itself detached), every line green
    $pc = Start-Process -FilePath $BASH -ArgumentList "C:/TETHER_RUNS/S6_2026-10-19/PLAY24/precheck.sh" -WindowStyle Hidden -PassThru
    $pc.PriorityClass = 'BelowNormal'
    $pc.WaitForExit()
    $pl = Get-Content "$P22\precheck.log"
    Say "PRECHECK $($pl.Count) lines"
    if (-not ($pl -match ' END$')) { throw "precheck has no END" }
    if ($pl -match 'GATE FAIL') { throw "precheck GATE FAIL: $(($pl -match 'GATE FAIL') -join ' | ')" }
    foreach ($l in ($pl -match ' rc ')) { if ($l -notmatch ' rc 0 ') { throw "precheck red: $l" } }
    # 7. the launch copy, detached, BelowNormal, no wait
    $u = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
    if (Test-Path "$P22\chain.log") { throw "PLAY24 chain.log exists" }
    Copy-Item "$P22\play_chain.sh" "$P22\play_chain.launched.$u.sh"
    $p = Start-Process -FilePath $BASH -ArgumentList "C:/TETHER_RUNS/S6_2026-10-19/PLAY24/play_chain.launched.$u.sh" -RedirectStandardOutput "$P22\play_chain.out" -RedirectStandardError "$P22\play_chain.err" -WindowStyle Hidden -PassThru
    $p.PriorityClass = 'BelowNormal'
    Say "LAUNCHED play_chain.launched.$u.sh pid $($p.Id)"
    Say "DONE"
} catch {
    Say "STOPPED: $($_.Exception.Message)"
    exit 2
}
