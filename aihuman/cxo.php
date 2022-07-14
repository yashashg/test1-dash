<?php
include("./db.php");
$cur_dir = basename(getcwd());
$user = mysqli_query($db, "SELECT * FROM user WHERE slug = '$cur_dir' ");
$row = mysqli_fetch_array($user);

if ($row["payment"] == "No") {
    $access = "no";
} else
    $access = "yes";

$type = mysqli_query($db, "SELECT * FROM dhcxo WHERE slug = '$cur_dir' ");
$row2 = mysqli_fetch_array($type);

$avatar = $row2["avatar"];

?>


<!doctype html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css" integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn" crossorigin="anonymous">


    <!-- Title needs to be dynamic -->
    <title>Digital CXO</title>
</head>

<body class="UI">
    <!-- Chatbot UI starts -->
    <section id="chatbot" class="main-card collapsed">
        <link rel="stylesheet" href="http://localhost/cxofinal/assets/css/style.css">
        <script src="http://localhost/cxofinal/font-awesome-pro-v6/js/pro.js" crossorigin="anonymous"></script>
        <link rel='stylesheet' href='http://localhost/cxofinal/font-awesome-pro-v6/css/all.css'>
        <!-- Chatbot opning buttons -->
        <button id="chatbot_toggle">
            <i class="fa-solid fa-messages fa-xl"></i>
            <i class="fa-solid fa-xmark fa-xl" style="display:none;"></i>
        </button>
        <!-- Nav Bar -->
        <div class="main-title">
            <div class="nav">
                <div id="mySidenav" class="sidenav">
                    <div class="sides">
                        <a href="javascript:void(0)" class="closebtn" onclick="closeNav()"> <i class="fa-solid fa-xmark"></i></a>
                        <div class="detail">
                            <h3>Services</h3>
                        </div>
                    </div>
                    <div class="nav-item">
                        <button class="btn"> Login/Registration</button>
                        <button class="btn"> Restart conversation</button>
                        <button class="btn"> Find your service</button>
                        <button class="btn"> Book a service</button>
                    </div>
                </div>
                <span onclick="openNav()"> <i class="fa-solid fa-bars fa-lg" style="display:none;" id="bars"></i></span>
            </div>
        </div>
        <!-- Chat area -->
        <div class="chat-area" id="message-box">
            <div class="video">
                <video id="idle" autoplay loop style="visibility: visible;">
                    <source src="https://thriftywebsite.s3.ap-south-1.amazonaws.com/assets/Videos/idle2.mp4" type="video/mp4">
                </video>
                <video id="intro" style="visibility: hidden;">
                    <source src="https://thriftywebsite.s3.ap-south-1.amazonaws.com/assets/Videos/hi2.mp4" type="video/mp4">
                </video>
                <video id="noted" style="visibility: hidden;">
                    <source src="https://thriftywebsite.s3.ap-south-1.amazonaws.com/assets/Videos/2.mp4" type="video/mp4">
                </video>

                <video id="happy" style="visibility: hidden;">
                    <source src="https://thriftywebsite.s3.ap-south-1.amazonaws.com/assets/Videos/good_rating.mp4" type="video/mp4">
                </video>
                <video id="sad" style="visibility: hidden;">
                    <source src="https://thriftywebsite.s3.ap-south-1.amazonaws.com/assets/Videos/good_rating.mp4" type="video/mp4">
                </video>
            </div>
            <div class="chat" id="chats">

            </div>
            <div class="mic">
                <button id="mics" class="btn voices"><i class="fas fa-microphone-alt fa-2x"></i></button>
                <div id="bar" class="" style="visibility: hidden;">
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                </div>
            </div>
        </div>
    </section>
    <script src="https://kit.fontawesome.com/5c58e8e06c.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.min.js" integrity="sha384-VHvPCCyXqtD5DqJeNxl2dtTyhF78xXNXdkwX1CZeRusQfRKp+tA7hAShOK/B/fQ2" crossorigin="anonymous"></script>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/gsap/3.7.0/gsap.min.js'></script>
    <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    <script src="http://localhost/cxofinal/assets/script/script.js"></script>
    <script>
        access = "<?php echo $access ?>";
        console.log(access)
        if (access == "no") {
            x = 5;
        } else {
            x = 9;
        }
        close();
    </script>
</body>

</html>