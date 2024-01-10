<?php
$station = $_POST['station'];
$lines = $_POST['lines'];

//$command = "sudo python3 piRC_manual.cpython-34.pyc $status 2>&1";y
$command = "./mbta.py $station $lines 2>&1";
$output = shell_exec($command);

print "
<html>
<title> MBTA</title>
<body>";

include('buttons.html');

print "
<text_area><pre>$output</pre></text_area>
<script>
console.log('PHP-input:" .$station. "');
</script>
</body>
</html>
";
?>
