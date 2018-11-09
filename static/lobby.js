
var player_list;
var width, height;
var connect;

function init()
{
    player_list = document.getElementById("player_list");
    width = document.getElementById("width");
    height = document.getElementById("height");
    connect = document.getElementById("connect");
    update();
    setInterval(update, 1000);
}

function request(page, callback)
{
    console.log("Request " + page);
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            callback(xhttp.responseText);
        }
    };
    xhttp.open("GET", page, true);
    xhttp.send();
}

function start_game()
{
    window.location = "/game";
}

function send_start()
{
    request("/start_game/" + width.value + "/" + 
        height.value + "/" + connect.value, (data) => 
    {
        if (data != "false")
            start_game();
    });
}

function update()
{
    request("/lobby_info", (data) => {
        var info = JSON.parse(data);
        var players = info["players"];

        player_list.innerHTML = "";
        for (var i = 0; i < players.length; i++)
            player_list.innerHTML += players[i] + "<br>";
        
        if (info["started"] == true)
            start_game();
    });
}
