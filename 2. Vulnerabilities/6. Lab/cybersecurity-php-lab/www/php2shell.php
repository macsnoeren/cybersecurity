<?php
// PHP2Shell (CVE-2026-109618 / CVE-2026-109619) DEFENSIVE assessment page.
//
// This is a teaching / self-assessment tool: it reports whether the PHP build
// running this lab is in the vulnerable range, checks the relevant mitigation
// settings, and gives remediation guidance. It contains NO exploit code -- it
// only inspects the local runtime, the same way a defender would.
//
// Written to run even on very old PHP (5.x) so the assessment still works if
// you pin an ancient tag, hence no null-coalescing / arrow functions.

$version = phpversion();
$sapi    = php_sapi_name();

// Branch -> first fixed patch release (published 2026-10-21).
$fixed = array(
    '8.5' => '8.5.12',
    '8.4' => '8.4.27',
    '8.3' => '8.3.36',
    '8.2' => '8.2.35',
);

// Work out major.minor branch, e.g. "8.3".
$parts  = explode('.', $version);
$branch = (count($parts) >= 2) ? ($parts[0] . '.' . $parts[1]) : $version;

$status  = 'unknown';   // vulnerable | patched | eol | unknown
$detail  = '';

if (isset($fixed[$branch])) {
    if (version_compare($version, $fixed[$branch], '>=')) {
        $status = 'patched';
        $detail = 'This build is at or above the fixed release ' . $fixed[$branch] . ' for the ' . $branch . ' branch.';
    } else {
        $status = 'vulnerable';
        $detail = 'This build is below the fixed release ' . $fixed[$branch] . ' for the ' . $branch . ' branch.';
    }
} else {
    // Branches 8.1 and older are end-of-life. PHP published only minimal
    // source backports for 7.4 / 8.0 / 8.1; everything older gets nothing.
    if (version_compare($version, '8.2.0', '<')) {
        $status = 'eol';
        $detail = 'The ' . $branch . ' branch is end-of-life. It receives no regular fix; only manual source backports exist for 7.4 / 8.0 / 8.1. Treat as affected unless you applied one.';
    }
}

// Mitigation-relevant settings (these reduce, not eliminate, exposure).
$upload_progress = ini_get('session.upload_progress.enabled');
$file_uploads    = ini_get('file_uploads');

function badge($status) {
    switch ($status) {
        case 'patched':    return array('#0a0', 'PATCHED');
        case 'vulnerable': return array('#c00', 'VULNERABLE');
        case 'eol':        return array('#c60', 'END-OF-LIFE / AFFECTED');
        default:           return array('#888', 'UNKNOWN');
    }
}
$b = badge($status);

function h($s) { return htmlspecialchars($s, ENT_QUOTES); }
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PHP2Shell assessment</title>
  <style>
    :root { color-scheme: light dark; }
    body { font: 16px/1.5 system-ui, sans-serif; max-width: 48rem; margin: 2rem auto; padding: 0 1rem; }
    h1 { margin-bottom: .25rem; }
    .sub { color: #888; margin-top: 0; }
    .badge { display: inline-block; color: #fff; padding: .25rem .6rem; border-radius: 4px; font-weight: 700; letter-spacing: .03em; }
    table { border-collapse: collapse; width: 100%; margin: 1.25rem 0; }
    th, td { text-align: left; padding: .5rem .75rem; border-bottom: 1px solid #8884; vertical-align: top; }
    th { width: 15rem; }
    code { background: #8882; padding: .1rem .35rem; border-radius: 3px; }
    .note { background: #8881; border-left: 4px solid #888; padding: .75rem 1rem; border-radius: 4px; margin: 1rem 0; }
    a { color: #37f; }
    ul { margin: .4rem 0; }
  </style>
</head>
<body>
  <h1>PHP2Shell assessment</h1>
  <p class="sub">CVE-2026-109618 &amp; CVE-2026-109619 &mdash; local self-check, no exploit.</p>

  <p><span class="badge" style="background:<?= h($b[0]) ?>"><?= h($b[1]) ?></span></p>

  <table>
    <tr><th>Running PHP</th>        <td><code><?= h($version) ?></code> (branch <code><?= h($branch) ?></code>)</td></tr>
    <tr><th>SAPI</th>               <td><code><?= h($sapi) ?></code><?= $sapi === 'apache2handler' ? ' (Apache mod_php)' : '' ?></td></tr>
    <tr><th>Assessment</th>         <td><?= h($detail !== '' ? $detail : 'Could not map this version to a known branch; verify manually against the advisories.') ?></td></tr>
    <tr><th>Fixed releases</th>     <td>8.2.35 &middot; 8.3.36 &middot; 8.4.27 &middot; 8.5.12 (published 2026-10-21)</td></tr>
    <tr><th>session.upload_progress.enabled</th>
        <td><code><?= $upload_progress ? 'On' : 'Off' ?></code> &mdash; one of the CVE-2026-109618 vectors; disabling it reduces (does not remove) exposure.</td></tr>
    <tr><th>file_uploads</th>
        <td><code><?= $file_uploads ? 'On' : 'Off' ?></code> &mdash; multipart upload parsing is the CVE-2026-109619 surface.</td></tr>
  </table>

  <div class="note">
    <strong>Remediation (the only complete fix is patching):</strong>
    <ul>
      <li>Upgrade to <strong>8.2.35 / 8.3.36 / 8.4.27 / 8.5.12</strong> or later for your branch.</li>
      <li>If you are on an end-of-life branch (8.1 or older), move to a supported branch; only minimal source backports exist for 7.4 / 8.0 / 8.1.</li>
      <li>Interim, partial mitigation only: <code>session.upload_progress.enabled = Off</code>. This touches one CVE-2026-109618 vector and does nothing for CVE-2026-109619.</li>
    </ul>
  </div>

  <p><a href="/">&larr; back to the lab</a></p>
</body>
</html>
