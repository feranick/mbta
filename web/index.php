<?php
$station = $_POST['station'];
$lines = $_POST['lines'];

//$command = "sudo python3 piRC_manual.cpython-34.pyc $status 2>&1";y
$command = "./mbta.py $station $lines 2>&1";
$output = shell_exec($command);
?>

<html manifest="mbta.manifest">
<html><head>

<title>MBTA</title>

    		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=0" />
            
            <!-- Eliminate url and button bars if added to home screen -->
            <meta name="apple-mobile-web-app-capable" content="yes" />
            
            <!-- Choose how to handle the phone status bar -->
            <meta names="apple-mobile-web-app-status-bar-style" content="black-translucent" />
            
            <link rel="stylesheet" type="text/css" href="mbta.css" media="screen" />
            
            <!-- Choose a 57x57 image for the icon -->
            <link rel="apple-touch-icon" href="mbta_icon.png" />
            
</head>
<body>

<form name = "MBTA" action = "index.php" method = "POST">
<br>Station =  <input name="station" value="<?php echo $station;?>" placeholder="station" size="12" maxlength="30" type="text" id="Entry">
<br><br>Lines =  <input name="lines" value="<?php echo $lines;?>" placeholder="lines" size="12" maxlength="50" type="text" id="Entry">
<br><br><input type = "submit" name ="submit" id="Submit" value = "Submit">
<text_area><pre><?php echo $output; ?></pre></text_area>
</form>
</body></html>
