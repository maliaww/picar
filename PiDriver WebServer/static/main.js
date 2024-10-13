var hasGP = false;
var repGP;
var prevButtons = [];
function canGame() {
  return "getGamepads" in navigator;
}
async function reportOnGamepad() {
  var gp = navigator.getGamepads()[0];
  var html = "";
  html += "SPEED";
  html += "<br/>";
  if (gp.buttons[7].pressed) {
    html += (gp.buttons[7].value * 10).toFixed();
    html += "<br/>";
  } else if (gp.buttons[6].pressed) {
    html += -(gp.buttons[6].value * 10).toFixed();
    html += "<br/>";
  } else if (gp.buttons[6].pressed == false || gp.buttons[7].pressed == false) {
    html += "0";
    html += "<br/>";
  }

  for (var i = 0; i < gp.buttons.length; i++) {
    if (
      (prevButtons[i] !== undefined &&
        prevButtons[i] > 0 &&
        gp.buttons[i].value === 0 &&
        i + 1 === 7) ||
      (prevButtons[i] !== undefined &&
        prevButtons[i] > 0 &&
        gp.buttons[i].value === 0 &&
        i + 1 === 8)
    ) {
      let input = { buttonNum: i + 1, value: 0 };
      fetch("/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(input),
      })
        .then((resp) => resp.json())
        .then((data) => console.log(data));
    }

    if (gp.buttons[i].pressed) {
      var input = { buttonNum: i + 1, value: gp.buttons[i].value };
      fetch("/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(input),
      })
        .then((resp) => resp.json())
        .then((data) => console.log(data));
    }
    prevButtons[i] = gp.buttons[i].value;
  }

  for (var i = 0; i < gp.axes.length; i += 2) {
    if (gp.axes[i] < -0.5 || gp.axes[i] > 0.5) {
      console.log(gp.axes[i], Math.ceil(i / 2) + 1);
      var inputAxes = {
        axesNum: Math.ceil(i / 2) + 1,
        value: gp.axes[i],
      };
      fetch("/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputAxes),
      })
        .then((resp) => resp.json())
        .then((data) => console.log(data));
    }
  }
  $("#gamepadDisplay").html(html);
}
$(document).ready(function () {
  if (canGame()) {
    var prompt = "TO BEGIN USING YOUR WHEEL, CONNECT IT AND PRESS ANY BUTTON!";
    $("#gamepadPrompt").text(prompt);
    $(window).on("gamepadconnected", function () {
      hasGP = true;
      $("#gamepadPrompt").html("Gamepad connected!");

      console.log("connection event");
      repGP = window.setInterval(reportOnGamepad, 100);
    });
    $(window).on("gamepaddisconnected", function () {
      console.log("disconnection event");
      $("#gamepadPrompt").text(prompt);
      window.clearInterval(repGP);
    });
    //setup an interval for Chrome
    var checkGP = window.setInterval(function () {
      console.log("checkGP");
      if (navigator.getGamepads()[0]) {
        if (!hasGP) $(window).trigger("gamepadconnected");
        window.clearInterval(checkGP);
      }
    }, 1000);
  }
});
