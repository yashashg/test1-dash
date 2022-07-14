document.getElementById("chatbot_toggle").onclick = function () {
  let details = navigator.userAgent;
  let regexp = /android|iphone|kindle|ipad/i;
  let isMobileDevice = regexp.test(details);

  if (document.getElementById("chatbot").classList.contains("collapsed")) {
    document.getElementById("chatbot").classList.remove("collapsed");
    document.getElementById("chatbot_toggle").children[0].style.display =
      "none";
    document.getElementById("chatbot_toggle").children[1].style.display = "";
    document.getElementById("bar").style.display = "";
    document.getElementById("mics").style.display = "block";
    document.getElementById("chats").style.display = "block";
    if (isMobileDevice) {
      document.getElementById("thriftyai").style.width = "100%";
      document.getElementById("thriftyai").style.height = "100%";
    } else {
      document.getElementById("thriftyai").style.width = "24%";
      document.getElementById("thriftyai").style.height = "95vh";
    }
    initial();
    // setTimeout(addResponseMsg, 1000, "Hi")
  } else {
    document.getElementById("chatbot").classList.add("collapsed");
    document.getElementById("chatbot_toggle").children[0].style.display = "";
    document.getElementById("chatbot_toggle").children[1].style.display =
      "none";
    document.getElementById("bar").style.display = "none";
    document.getElementById("mics").style.display = "none";
    document.getElementById("chats").style.display = "none";
    document.getElementById("thriftyai").style.width = "auto";
    document.getElementById("thriftyai").style.height = "auto";
  }
};

/* Set the width of the side navigation to 250px */
function openNav() {
  document.getElementById("mySidenav").style.width = "100%";
}
/* Set the width of the side navigation to 0 */
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

function initial() {
  if (x == 9) {
    intro.style.visibility = "visible";
    intro.play();
    document
      .getElementById("intro")
      .addEventListener("ended", myHandler, false);
    function myHandler(e) {
      close();
    }
    var bot_response_html =
      '<p class="user_message"><span>Hi, I am Diksha, I would love to get your feedback on today’s interaction with us. </span></p>';
    $("#chats").append(bot_response_html);
    x = 1;
  }
}
var seconds = 0;
var cancel = setInterval(incrementSeconds, 1000);
function incrementSeconds() {
  seconds += 1;
  console.log(seconds);
}
var today = new Date();
var date =
  today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
var time =
  today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
var month = today.getMonth();

var mic = document.getElementById("mic");
const voice = document.querySelector(".voices");
var transcript;
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const recorder = new SpeechRecognition();
voice.addEventListener("click", () => {
  recorder.start();
});
recorder.onstart = () => {
  close();
  console.log("Voice1 activated");
  bar.style.visibility = "visible";
  mics.style.visibility = "hidden";
};
recorder.onresult = (event) => {
  const resultIndex = event.resultIndex;
  mics.style.visibility = "visible";
  bar.style.visibility = "hidden";
  transcript = event.results[resultIndex][0].transcript;
  console.log(transcript);
  console.log(access);
  console.log(x);
  if (x != 5) {
    recog(transcript);
  }
  return transcript;
};
recorder.addEventListener("end", function () {
  mics.style.visibility = "visible";
  bar.style.visibility = "hidden";
});
recorder.addEventListener("error", function (event) {
  mics.style.visibility = "visible";
  bar.style.visibility = "hidden";
});
function rate(l) {
  transcript = document.getElementById(l).value;
  x = 0;
  if (x != 5) {
    recog(transcript);
  }
}
function recog(transcript) {
  if (x == 1) {
    close();
    noted.style.visibility = "visible";
    noted.play();
    document
      .getElementById("noted")
      .addEventListener("ended", myHandler, false);
    text_review = transcript;
    console.log("direct svae");
    $.ajax({
      type: "POST",
      url: "data.php",
      data: { review: text_review, date: date, time: time },
      success: function (response) {
        console.log(response);
      },
    });
    var bot_response_html =
      '<div class="rate user_message"><span class="exception">Noted, how satisfied are you with your overall experience</span><br><input type="radio" id="star1" name="rate" value="1" onclick="rate(this.id)" /><label for="star1" title="text">1star</label><input type="radio" id="star2" name="rate" value="2" onclick="rate(this.id)" /><label for="star2" title="text">2stars</label><input type="radio" id="star3" name="rate" value="3" onclick="rate(this.id)" /><label for="star3"title="text">3stars</label><input type="radio" id="star4" name="rate" value="4" onclick="rate(this.id)" /><label for="star4"title="text">4stars</label><input type="radio" id="star5" name="rate" value="5" onclick="rate(this.id)" /><label for="star5"title="text">5 stars</label></div>';
    $("#chats").append(bot_response_html);
    x = 0;
  } else {
    var matches = transcript.match(/(\d+)/);
    console.log(matches);
    console.log(matches[0]);
    if (matches[0] >= 4) {
      close();
      happy.style.visibility = "visible";
      happy.play();
      document
        .getElementById("happy")
        .addEventListener("ended", myHandler, false);
      var bot_response_html =
        '<p class="user_message"><span>Thanks for your time. See you soon, bye!</span></p>';
      $("#chats").append(bot_response_html);
      $("#chats").animate(
        { scrollTop: $("#chats").prop("scrollHeight") },
        1000
      );
      $.ajax({
        type: "POST",
        url: "rating.php",
        data: {
          review: matches[0],
          text_review: text_review,
          duration: seconds,
          date: date,
          time: time,
          month: month,
        },
        success: function (response) {
          console.log(response);
        },
      });
    } else {
      close();
      sad.style.visibility = "visible";
      sad.play();
      document
        .getElementById("sad")
        .addEventListener("ended", myHandler, false);
      var bot_response_html =
        '<p class="user_message"><span>Thanks for your time. See you soon, bye!</span></p>';
      $("#chats").append(bot_response_html);
      $("#chats").animate(
        { scrollTop: $("#chats").prop("scrollHeight") },
        1000
      );
      $.ajax({
        type: "POST",
        url: "rating.php",
        data: {
          review: matches[0],
          text_review: text_review,
          duration: seconds,
          date: date,
          time: time,
          month: month,
        },
        success: function (response) {
          console.log(response);
        },
      });
    }
  }
}
function close() {
  intro.style.visibility = "hidden";
  noted.style.visibility = "hidden";
  happy.style.visibility = "hidden";
  sad.style.visibility = "hidden";

  intro.pause();
  noted.pause();
  happy.pause();
  sad.pause();
}
function myHandler(e) {
  idle.style.visibility = "visible";
  idle.play();
  close();
}
