<?php
if ($_POST['station'] and $_POST['lines']) {
    $station = $_POST['station'];
    $lines = $_POST['lines'];
    $command = "./mbta_signs.py $station $lines 2>&1";
    //$command = "python3 mbta_signs.cpython-310.pyc $station $lines 2>&1";
    $output = shell_exec($command);
} else if($_POST['lines']) {
    $lines = $_POST['lines'];
    $command = "./mbta_stops.py $lines 2>&1";
    //$command = "python3 mbta_stops.cpython-310.pyc $lines 2>&1";
    $output = shell_exec($command);
} else if($_POST['station']) {
    $station = $_POST['station'];
    $command = "./mbta_lines.py $station 2>&1";
    //$command = "python3 mbta_lines.cpython-310.pyc $station 2>&1";
    $output = shell_exec($command);
} else if($_POST['vehicle']) {
    $vehicle = $_POST['vehicle'];
    $command = "./mbta_vehicles_id.py $vehicle 2>&1";
    //$command = "python3 mbta_vehicles_id.cpython-310.pyc $vehicle 2>&1";
    $output = shell_exec($command);
}
?>

<!DOCTYPE html>
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
<br>Station =  <input name="station" value="<?php echo $station;?>" placeholder="station" size="12" maxlength="30" type="text" id="EntryStation">
<br><br>Lines =  <input name="lines" value="<?php echo $lines;?>" placeholder="lines" size="12" maxlength="50" type="text" id="EntryLines">
<br><br>Vehicle ID =  <input name="vehicle" value="<?php echo $vehicle;?>" placeholder="vehicle id" size="12" maxlength="50" type="text" id="EntryVehicle">
<br><br><input type = "submit" name ="submit" id="Submit" value = "Submit">
</form>

<text_area><pre><?php echo $output; ?></pre></text_area>
</body></html>
