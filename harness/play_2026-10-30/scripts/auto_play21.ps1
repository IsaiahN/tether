# r394 automation, started ONCE after the reviewer's merge post: PLAY21 prepared on the merged arc tip,
# STOP placed for PLAY20, PLAY_END awaited (the chain's own exit; nothing killed), the verified lineage
# backup taken, PLAY21's head/want/precheck set, and PLAY21 launched detached only if every precheck
# line is green. Every step is logged to PLAY21\auto.log; any failure stops the script before launch.
# argv: -H <arc-solver-agent tip sha (40)> -G <general-agent tip sha (40)>
param([Parameter(Mandatory = $true)][string]$H, [Parameter(Mandatory = $true)][string]$G)
$ErrorActionPreference = 'Stop'
$R = 'C:\TETHER_RUNS\S6_2026-10-19'
$P20 = "$R\PLAY20"; $P21 = "$R\PLAY21"
$CLONE = "$R\split\fresh_r27"; $T = "$CLONE\arc-solver-agent"
$BASH = 'C:\Program Files\Git\bin\bash.exe'
$PY = 'C:\Users\Admin\Documents\GitHub\tether\.venv\Scripts\python.exe'
$SP = 'C:\Users\Admin\AppData\Local\Temp\claude\c--Users-Admin-Documents-GitHub-tether\b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf\scratchpad'
if (Test-Path $P21) { throw "PLAY21 exists" }
New-Item -ItemType Directory -Path $P21 | Out-Null
$LOG = "$P21\auto.log"
function Say($m) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $m" | Out-File -FilePath $LOG -Append -Encoding utf8 }
function Bash($cmd) { & $BASH -c $cmd; if ($LASTEXITCODE -ne 0) { throw "bash rc $LASTEXITCODE : $cmd" } }
try {
    Say "START H=$H G=$G"
    # 1. the clone at the merged arc tip, with M3 and the two junctions (PowerShell, literal paths)
    if (Test-Path $CLONE) { throw "fresh_r27 exists" }
    New-Item -ItemType Directory -Path $CLONE | Out-Null
    Bash "cd /c/TETHER_RUNS/S6_2026-10-19/split/fresh_r27 && git clone --quiet --branch arc-solver-agent https://github.com/IsaiahN/tether.git arc-solver-agent"
    $head = (& git -C $T rev-parse HEAD).Trim()
    if ($head -ne $H) { throw "clone HEAD $head != H $H" }
    $diff = (& git -C $T diff --name-only $G HEAD) -join ','
    if ($diff -ne 'README.md') { throw "diff vs G is [$diff], not README.md" }
    Copy-Item 'C:\Users\Admin\Documents\GitHub\tether\.git\hooks\commit-msg' "$T\.git\hooks\commit-msg"
    New-Item -ItemType Junction -Path "$T\.venv" -Target 'C:\Users\Admin\Documents\GitHub\tether\.venv' | Out-Null
    New-Item -ItemType Junction -Path "$T\environment_files" -Target "$R\wt_ivv\environment_files" | Out-Null
    Say "CLONE fresh_r27 at $head, diff vs G README.md, hook copied, junctions made"
    # 2. PLAY21's files from PLAY20's, with P/T/G/H replaced (FIRST_ROUND=1 already)
    $oldG = '9133034e2f3d691f31dad80dfc17503b7077ce39'; $oldH = '7b9a90f257d9e4f566e0fa86f562382cc3df2518'
    foreach ($f in 'play_chain.sh', 'precheck.sh') {
        $s = [IO.File]::ReadAllText("$P20\$f")
        $s = $s.Replace('S6_2026-10-19/PLAY20"', 'S6_2026-10-19/PLAY21"').Replace('split/fresh_r26/', 'split/fresh_r27/')
        $s = $s.Replace("G=$oldG", "G=$G").Replace("H=$oldH", "H=$H")
        $s = $s.Replace('# PLAY20 = PLAY19 on the NEW tree', "# PLAY21 = PLAY20 on the NEW tree arc-solver-agent $($H.Substring(0,7)) (wip/finish's five arms; the reviewer r392-r399). PLAY20 = PLAY19 on the NEW tree")
        [IO.File]::WriteAllText("$P21\$f", $s)
    }
    Copy-Item "$P20\play_across.py" "$P21\play_across.py"
    foreach ($f in 'play_chain.sh', 'precheck.sh') {
        $s = [IO.File]::ReadAllText("$P21\$f")
        if ($s.Contains('PLAY20"') -or $s.Contains("fresh_r26/") -or $s.Contains("G=$oldG") -or $s.Contains("H=$oldH")) { throw "$f still names PLAY20 / fresh_r26 / old G or H" }
    }
    Say "FILES play_chain.sh, precheck.sh (P/T/G/H replaced), play_across.py copied"
    # 3. STOP for PLAY20 and wait for its own PLAY_END
    if (-not (Test-Path "$P20\STOP")) { "STOP placed by auto_play21.ps1 (the reviewer's merge post; r392, r394)" | Out-File "$P20\STOP" -Encoding ascii }
    Say "STOP placed in PLAY20; waiting for PLAY_END"
    while (-not (Select-String -Path "$P20\chain.log" -Pattern 'PLAY_END' -Quiet)) { Start-Sleep -Seconds 30 }
    $tail = (Get-Content "$P20\chain.log" -Tail 4) -join ' | '
    Say "PLAY20 ended: $tail"
    if ((Get-Content "$P20\chain.log" -Tail 6) -match 'STOP round|STOP free disk') { throw "PLAY20 ended on a STOP condition, not the STOP file" }
    # 4. the verified backup at PLAY20's last verified head
    $hd = (Get-Content "$P20\head.txt" -Raw).Trim()
    $stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $out = & $PY -B -I "$SP\backup_lineage.py" $stamp $hd "PLAY20's last kept generation, the chain stopped clean on the STOP file after the reviewer's merge post; before PLAY21" 2>&1
    if ($LASTEXITCODE -ne 0) { throw "backup rc $LASTEXITCODE : $out" }
    Say "BACKUP $out"
    # 5. head, HW, want
    Set-Content -Path "$P21\head.txt" -Value $hd -NoNewline -Encoding ascii
    $s = [IO.File]::ReadAllText("$P21\precheck.sh")
    $s = [regex]::Replace($s, '(?m)^HW=\S+', "HW=$hd")
    $last = (Get-ChildItem "$P20" -Directory -Filter 'round_*' | Where-Object { Test-Path "$($_.FullName)\read.out" } |
             Sort-Object Name | Select-Object -Last 1).Name
    if (-not $last) { throw "no finished PLAY20 round" }
    $s = $s.Replace('PLAY19/round_08/stream.jsonl', "PLAY20/$last/stream.jsonl")
    [IO.File]::WriteAllText("$P21\precheck.sh", $s)
    Bash "bash /c/Users/Admin/AppData/Local/Temp/claude/c--Users-Admin-Documents-GitHub-tether/b5d0f0d4-c815-4bdb-a3b5-cbfc474103cf/scratchpad/want21.sh"
    Say "HEAD $hd; HW set; log_index verify on PLAY20/$last; want $((Get-Content "$P21\play_chain.want" -Raw).Trim())"
    # 6. the precheck, BelowNormal, waited here (this script is itself detached), every line green
    $pc = Start-Process -FilePath $BASH -ArgumentList "C:/TETHER_RUNS/S6_2026-10-19/PLAY21/precheck.sh" -WindowStyle Hidden -PassThru
    $pc.PriorityClass = 'BelowNormal'
    $pc.WaitForExit()
    $pl = Get-Content "$P21\precheck.log"
    Say "PRECHECK $($pl.Count) lines"
    if (-not ($pl -match ' END$')) { throw "precheck has no END" }
    if ($pl -match 'GATE FAIL') { throw "precheck GATE FAIL: $(($pl -match 'GATE FAIL') -join ' | ')" }
    foreach ($l in ($pl -match ' rc ')) { if ($l -notmatch ' rc 0 ') { throw "precheck red: $l" } }
    # 7. the launch copy, detached, BelowNormal, no wait
    $u = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
    if (Test-Path "$P21\chain.log") { throw "PLAY21 chain.log exists" }
    Copy-Item "$P21\play_chain.sh" "$P21\play_chain.launched.$u.sh"
    $p = Start-Process -FilePath $BASH -ArgumentList "C:/TETHER_RUNS/S6_2026-10-19/PLAY21/play_chain.launched.$u.sh" -RedirectStandardOutput "$P21\play_chain.out" -RedirectStandardError "$P21\play_chain.err" -WindowStyle Hidden -PassThru
    $p.PriorityClass = 'BelowNormal'
    Say "LAUNCHED play_chain.launched.$u.sh pid $($p.Id)"
    Say "DONE"
} catch {
    Say "STOPPED: $($_.Exception.Message)"
    exit 2
}
