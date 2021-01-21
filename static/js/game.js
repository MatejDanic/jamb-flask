var dice;
window.onload = function () {

    dice = document.getElementsByTagName("dice");
    for (key in dice) {
        dice[key].held = false;
        dice[key].onclick = function () {
            console.log(this.getAttribute("id"));
        }
    }
    restart = document.getElementById("restart")
    restart.onclick = function () {
        fetch("http://localhost:8080/game/" + sessionStorage.getItem("game_id") + "/restart", {
            method: "PUT",
            headers: { "Content-type": "application/json; charset=UTF-8" }
        }).then(response => response.json())
        window.location.reload();
    }
    console.log("Loaded");
};


function roll() {
    let dice_to_roll = [];
    for (key in dice) if (dice[key].held) dice_to_roll.push(key);
    console.log(dice_to_roll);
    // fetch("http://localhost:8080/game/" + sessionStorage.getItem("game_id") + "/roll", {
    //     method: "PUT",
    //     body: JSON.stringify({ dice_to_roll }),
    //     headers: { "Content-type": "application/json; charset=UTF-8" }
    // }).then(response => response.json())
    //     .then(json => {
    //         for (dice in json.message[0]) {
    //             console.log(json.message[0][dice]);
    //         }
    //     })
}

function hold(ordinal) {
    console.log(ordinal);
    dice[ordinal].held = !dice[ordinal].held;
    console.log(ordinal + " held: " + dice[ordinal].held);
}