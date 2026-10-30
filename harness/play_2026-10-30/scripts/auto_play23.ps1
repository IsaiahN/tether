# auto_play21.ps1 carried to PLAY22 -> PLAY23, started ONCE after the reviewer's merge post: PLAY23 prepared on the
# arc tip, PLAY_END awaited (STOP placed in PLAY22 before its round 2 END (r430); nothing killed), the verified
# lineage backup taken, PLAY23's head/want/precheck set, and PLAY23 launched detached only if every precheck line is
# green. Every step is logged to PLAY23\auto.log; any failure stops the script before launch.
# argv: -H <arc-solver-agent tip sha (40)> -G <general-agent tip sha (40)> -Note <what the tree carries>
param([Parameter(Mandatory = $true)][string]$H, [Parameter(Mandatory = $true)][string]$G,
      [Parameter(Mandatory = $true)][string]$Note)
$ErrorActionPreference = 'Stop'
$R = 'C:\TETHER_RUNS\S6_2026-10-19'
$P21 = "$R\PLAY22"; $P22 = "$R\PLAY23"
$CLONE = "$R\split\fresh_r29"; $T = "$CLONE\arc-solver-agent"
$BASH = 'C:\Program Files\Git\bin\bash.exe'
$PY = 'C:\Users\Admin\Documents\GitHub\tether\.venv\Scripts\python.exe'
$SP = 'C:\Users\Admin\AppData\Local\Temp\claude\c--Users-Admin-Documents-GitHub-tether\b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf\scratchpad'
if (Test-Path $P22) { throw "PLAY23 exists" }
New-Item -ItemType Directory -Path $P22 | Out-Null
$LOG = "$P22\auto.log"
function Say($m) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $m" | Out-File -FilePath $LOG -Append -Encoding utf8 }
function Bash($cmd) { & $BASH -c $cmd; if ($LASTEXITCODE -ne 0) { throw "bash rc $LASTEXITCODE : $cmd" } }
try {
    Say "START H=$H G=$G NOTE=$Note"
    # 1. the clone at the arc tip, with M3 and the two junctions (PowerShell, literal paths)
    if (Test-Path $CLONE) { throw "fresh_r29 exists" }
    New-Item -ItemType Directory -Path $CLONE | Out-Null
    Bash "cd /c/TETHER_RUNS/S6_2026-10-19/split/fresh_r29 && git clone --quiet --branch arc-solver-agent https://github.com/IsaiahN/tether.git arc-solver-agent"
    $head = (& git -C $T rev-parse HEAD).Trim()
    if ($head -ne $H) { throw "clone HEAD $head != H $H" }
    $diff = (& git -C $T diff --name-only $G HEAD) -join ','
    if ($diff -ne 'README.md') { throw "diff vs G is [$diff], not README.md" }
    Copy-Item 'C:\Users\Admin\Documents\GitHub\tether\.git\hooks\commit-msg' "$T\.git\hooks\commit-msg"
    New-Item -ItemType Junction -Path "$T\.venv" -Target 'C:\Users\Admin\Documents\GitHub\tether\.venv' | Out-Null
    New-Item -ItemType Junction -Path "$T\environment_files" -Target "$R\wt_ivv\environment_files" | Out-Null
    Say "CLONE fresh_r29 at $head, diff vs G README.md, hook copied, junctions made"
    # 2. PLAY23's files from PLAY22's, with P/T/G/H replaced (FIRST_ROUND=1 already)
    $oldG = 'e7a1c8ebe4a5e1eca3ce0b9978221cfcc1a0f6fb'; $oldH = 'a3ad3eff6a738c4e057afb613bde9b638b7fe55c'
    foreach ($f in 'play_chain.sh', 'precheck.sh') {
        $s = [IO.File]::ReadAllText("$P21\$f")
        $s = $s.Replace('S6_2026-10-19/PLAY22"', 'S6_2026-10-19/PLAY23"').Replace('split/fresh_r28/', 'split/fresh_r29/')
        $s = $s.Replace("G=$oldG", "G=$G").Replace("H=$oldH", "H=$H")
        $s = $s.Replace('# PLAY22 = PLAY21 on the tree', "# PLAY23 = PLAY22 on the tree arc-solver-agent $($H.Substring(0,7)) ($Note). PLAY22 = PLAY21 on the tree")
        [IO.File]::WriteAllText("$P22\$f", $s)
    }
    Copy-Item "$P21\play_across.py" "$P22\play_across.py"
    foreach ($f in 'play_chain.sh', 'precheck.sh') {
        $s = [IO.File]::ReadAllText("$P22\$f")
        if ($s.Contains('PLAY22"') -or $s.Contains("fresh_r28/") -or ($oldG -ne $G -and $s.Contains("G=$oldG")) -or ($oldH -ne $H -and $s.Contains("H=$oldH"))) { throw "$f still names PLAY22 / fresh_r28 / old G or H" }
        if (-not $s.Contains("G=$G") -or -not $s.Contains("H=$H")) { throw "$f lacks the new G or H" }
    }
    Say "FILES play_chain.sh, precheck.sh (P/T/G/H replaced), play_across.py copied"
    # 3. PLAY22's STOP (placed before round 2 END on the reviewer verify) and its own PLAY_END
    if (-not (Test-Path "$P21\STOP")) { throw "PLAY22 has no STOP file" }
    Say "waiting for PLAY22's PLAY_END"
    while (-not (Select-String -Path "$P21\chain.log" -Pattern 'PLAY_END' -Quiet)) { Start-Sleep -Seconds 30 }
    $tail = (Get-Content "$P21\chain.log" -Tail 4) -join ' | '
    Say "PLAY22 ended: $tail"
    if ((Get-Content "$P21\chain.log" -Tail 6) -match 'STOP round|STOP free disk') { throw "PLAY22 ended on a STOP condition, not the STOP file" }
    # 4. the verified backup at PLAY22's last verified head
    $hd = (Get-Content "$P21\head.txt" -Raw).Trim()
    $stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $out = & $PY -B -I "$SP\backup_lineage.py" $stamp $hd "PLAY22's last kept generation, the chain stopped clean on the STOP file at the round boundary (the reviewer r430); before PLAY23" 2>&1
    if ($LASTEXITCODE -ne 0) { throw "backup rc $LASTEXITCODE : $out" }
    Say "BACKUP $out"
    # 5. head, HW, want
    Set-Content -Path "$P22\head.txt" -Value $hd -NoNewline -Encoding ascii
    $s = [IO.File]::ReadAllText("$P22\precheck.sh")
    $s = [regex]::Replace($s, '(?m)^HW=\S+', "HW=$hd")
    $last = (Get-ChildItem "$P21" -Directory -Filter 'round_*' | Where-Object { Test-Path "$($_.FullName)\read.out" } |
             Sort-Object Name | Select-Object -Last 1).Name
    if (-not $last) { throw "no finished PLAY22 round" }
    $s2 = [regex]::Replace($s, 'PLAY21/round_\d+/stream\.jsonl', "PLAY22/$last/stream.jsonl")
    if ($s2 -eq $s -or -not $s2.Contains("PLAY22/$last/stream.jsonl")) { throw "log_index verify path not replaced" }
    [IO.File]::WriteAllText("$P22\precheck.sh", $s2)
    Bash "bash /c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/want23.sh"
    Say "HEAD $hd; HW set; log_index verify on PLAY22/$last; want $((Get-Content "$P22\play_chain.want" -Raw).Trim())"
    # 6. the precheck, BelowNormal, waited here (this script is itself detached), every line green
    $pc = Start-Process -FilePath $BASH -ArgumentList "C:/TETHER_RUNS/S6_2026-10-19/PLAY23/precheck.sh" -WindowStyle Hidden -PassThru
    $pc.PriorityClass = 'BelowNormal'
    $pc.WaitForExit()
    $pl = Get-Content "$P22\precheck.log"
    Say "PRECHECK $($pl.Count) lines"
    if (-not ($pl -match ' END$')) { throw "precheck has no END" }
    if ($pl -match 'GATE FAIL') { throw "precheck GATE FAIL: $(($pl -match 'GATE FAIL') -join ' | ')" }
    foreach ($l in ($pl -match ' rc ')) { if ($l -notmatch ' rc 0 ') { throw "precheck red: $l" } }
    # 7. the launch copy, detached, BelowNormal, no wait
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
