function roll() {
    fetch("http://localhost:5000/game/roll", {
        method: "PUT",
        body: JSON.stringify({ game_id: "6006afd20a2acbdae5d2d69a" }),
        headers: { "Content-type": "application/json; charset=UTF-8" }
    }).then(response => response.json())
        .then(json => {
            for (dice in json.message[0]) {
                console.log(json.message[0][dice]);
            }
        })
}