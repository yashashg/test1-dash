<?php
$data = $_POST['review'];
$date = $_POST['date'];
$time = $_POST['time'];
$list = array(array($data, $date, $time));


$file = fopen('data.csv', 'a');  // 'a' for append to file - created if doesn't exit
foreach ($list as $line) {
    fputcsv($file, $line);
}
fclose($file);
// $file = fopen("test.csv", "a+");
// fputs($file, $list);
// fclose($file);
