var dice_buttons, box_buttons, roll_count, announcement, roll_dice_button, restart_button;
window.onload = function () {
    initialize(game);
};

function initialize(game) {
    console.log("Initializing...")
    dice_buttons = document.querySelectorAll('[id^="DICE"]');
    box_buttons = document.querySelectorAll('[id^="BOX"]');
    roll_dice_button = document.getElementById("ROLL-DICE-BUTTON");
    restart_button = document.getElementById("RESTART-BUTTON");
    roll_count = game.roll_count;
    announcement = game.announcement;

    for (dice_button of dice_buttons) {
        if (dice_button.classList.contains("dice-border-red")) {
            dice_button.classList.remove("dice-border-red")
            dice_button.classList.add("dice-border-black")
        }

        dice_button.onclick = function () {
            if (this.classList.contains("dice-border-black")) {
                this.classList.remove("dice-border-black");
                this.classList.add("dice-border-red");
            } else {
                this.classList.remove("dice-border-red");
                this.classList.add("dice-border-black");
            }
        }
    }

    for (box_button of box_buttons) {
        box_button.onclick = function () {
            console.log(this.id);
        }
    }

    roll_dice_button.onclick = function() {
        console.log("Rolling dice...");
        const Http = new XMLHttpRequest();
        const url = "http://localhost:5000/game/" + game_id + "/roll";
        Http.open("PUT", url);
        let dice_to_roll = [];
        for (dice_button of dice_buttons) {
            if (dice_button.classList.contains("dice-border-black")) {
                dice_to_roll.push(dice_button.id.split("-")[1]);
            }
        }
        data = {};
        Http.send(JSON.stringify(dice_to_roll));

        Http.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                dice = JSON.parse(Http.response);
                console.log(dice);
                for (dice_button of dice_buttons) {
                    dice_button.setAttribute("style", "background-image: url(../static/images/dice/" + dice[dice_button.id.split("-")[1] - 1].value + ".png);");
                }
            }
        }
    }

    restart_button.onclick = function() {
        console.log("Restarting...")
        const Http = new XMLHttpRequest();
        const url = "http://localhost:5000/game/" + game_id + "/restart";
        Http.open("PUT", url);
        Http.send();

        Http.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                game = JSON.parse(Http.response);
                console.log(game);
                initialize(game)
            }
        }
    }
    console.log("Initialization finished!");
}
