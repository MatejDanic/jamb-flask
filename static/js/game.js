var dice = document.querySelectorAll('[id^="DICE"]');
var boxes = document.querySelectorAll('[id^="BOX"]');
var roll_count = game.roll_count;
var announcement = game.announcement;
window.onload = function () {
    for (key in dice) {
        dice[key].onclick = function () {
            if (this.classList.contains("dice-border-black")) {
                this.classList.remove("dice-border-black");
                this.classList.add("dice-border-red");
            } else {
                this.classList.remove("dice-border-red");
                this.classList.add("dice-border-black");
            }
        }
    }
    for (key in boxes) {
        boxes[key].onclick = function () {
            console.log(this.getAttribute("id"));
        }
    }
    let restart = document.getElementById("restart");
    restart.onclick = function () {
        const Http = new XMLHttpRequest();
        const url="http://localhost:5000/game/" + game_id + "/restart";
        Http.open("PUT", url);
        Http.send();

        Http.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                game = JSON.parse(Http.response);
                console.log(game);
                initialize(game)
            }
        }
    }
    console.log("Loaded");
};

function initialize(game) {
    for (key in dice) {
        if (dice[key].classList.contains("dice-border-red")) {
            dice[key].classList.remove("dice-border-red")
            dice[key].classList.add("dice-border-black")
        }
        dice[key].setAttribute("style", "background-image: url(../static/images/dice/" + game.dice[key].value + ".png);");
    }
}
