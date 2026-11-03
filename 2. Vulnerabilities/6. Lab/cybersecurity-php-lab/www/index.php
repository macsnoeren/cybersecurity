<?php
// Simple PHP landing page for the lab. Intentionally benign: it just proves
// that PHP is running under Apache mod_php and reports the facts you need when
// studying this environment.

$php_version   = phpversion();
$sapi          = php_sapi_name();                 // "apache2handler" for mod_php
$server        = isset($_SERVER['SERVER_SOFTWARE']) ? $_SERVER['SERVER_SOFTWARE'] : 'unknown';
$now           = date('Y-m-d H:i:s');

// PHP2Shell range check, same table as php2shell.php: a supported branch below
// its fixed release, or any end-of-life branch (8.1 and older).
$fixed         = array('8.5' => '8.5.12', '8.4' => '8.4.27', '8.3' => '8.3.36', '8.2' => '8.2.35');
$parts         = explode('.', $php_version);
$branch        = (count($parts) >= 2) ? ($parts[0] . '.' . $parts[1]) : $php_version;
$is_eol        = version_compare($php_version, '8.2.0', '<');
$is_vulnerable = $is_eol || (isset($fixed[$branch]) && version_compare($php_version, $fixed[$branch], '<'));
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PHP Security Lab</title>
  <style>
    :root { color-scheme: light dark; }
    body { font: 16px/1.5 system-ui, sans-serif; max-width: 48rem; margin: 2rem auto; padding: 0 1rem; }
    h1 { margin-bottom: .25rem; }
    .sub { color: #888; margin-top: 0; }
    table { border-collapse: collapse; width: 100%; margin: 1.5rem 0; }
    th, td { text-align: left; padding: .5rem .75rem; border-bottom: 1px solid #8884; }
    th { width: 14rem; }
    .warn { background: #ffb; color: #000; border-left: 4px solid #c90; padding: .75rem 1rem; border-radius: 4px; }
    code { background: #8882; padding: .1rem .35rem; border-radius: 3px; }
    a { color: #37f; }
  </style>
</head>
<body>
  <h1>PHP Security Lab</h1>
  <p class="sub">Local, isolated research environment &mdash; not for production.</p>

  <?php if ($is_vulnerable): ?>
    <p class="warn">
      <strong>Heads up:</strong> this PHP build
      (<code><?= htmlspecialchars($php_version) ?></code>) is
      <?= $is_eol ? 'end-of-life and' : '' ?> in the PHP2Shell range
      (CVE-2026-109618 / -109619, unauthenticated RCE). It is intentionally
      insecure. Keep it bound to <code>127.0.0.1</code> and never expose it to
      a real network.
    </p>
  <?php endif; ?>

  <table>
    <tr><th>PHP version</th>      <td><code><?= htmlspecialchars($php_version) ?></code></td></tr>
    <tr><th>SAPI</th>             <td><code><?= htmlspecialchars($sapi) ?></code> <?= $sapi === 'apache2handler' ? '(Apache mod_php)' : '' ?></td></tr>
    <tr><th>Server</th>          <td><code><?= htmlspecialchars($server) ?></code></td></tr>
    <tr><th>Server time</th>     <td><?= htmlspecialchars($now) ?></td></tr>
  </table>

  <p>
    PHP2Shell self-assessment (CVE-2026-109618 / -109619):
    <a href="php2shell.php">php2shell.php</a>
  </p>
  <p>
    Full interpreter configuration: <a href="info.php">info.php</a>
    (<code>phpinfo()</code>).
  </p>
</body>
</html>
