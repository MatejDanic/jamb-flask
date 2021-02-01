var dice, boxes, roll_count, announcement;
window.onload = function () {
    console.log("Initializing...")
    initialize(game);
    console.log("Done!");
};

function initialize(game) {
    dice = document.querySelectorAll('[id^="DICE"]');
    boxes = document.querySelectorAll('[id^="BOX"]');
    roll_count = game.roll_count;
    announcement = game.announcement;

    for (d of dice) {
        if (d.classList.contains("dice-border-red")) {
            d.classList.remove("dice-border-red")
            d.classList.add("dice-border-black")
        }

        d.setAttribute("style", "background-image: url(../static/images/dice/" + game.dice[d.id.split("-")[1]-1].value + ".png);");
        
        d.onclick = function () {
            if (this.classList.contains("dice-border-black")) {
                this.classList.remove("dice-border-black");
                this.classList.add("dice-border-red");
            } else {
                this.classList.remove("dice-border-red");
                this.classList.add("dice-border-black");
            }
        }
    }

    for (box of boxes) {
        box.onclick = function () {
            console.log(this.id);
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
}
