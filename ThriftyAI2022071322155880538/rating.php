<?php
$rate = $_POST['review'];
$date = $_POST['date'];
$time = $_POST['time'];
$duration = $_POST['duration'];
$text_review = $_POST['text_review'];
$month = $_POST['month'];
$detractor = 0;
$promoter = 0;
$passive = 0;


if ($rate <= 3) {
    $detractor = 1;
} elseif ($rate == 5) {
    $promoter = 1;
} else {
    $passive = 1;
}
$list = array(array($rate, $text_review, $date, $time, $month, $duration, $detractor, $passive, $promoter));
$file = fopen('rating.csv', 'a');  // 'a' for append to file - created if doesn't exit
foreach ($list as $line) {
    fputcsv($file, $line);
}
fclose($file);
