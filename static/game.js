
var table, turn;
var last_turn = -1;

function init()
{
    table = document.getElementById("table");
    turn = document.getElementById("turn");

    for (var i = 0; i < height; i++)
    {
        var row = document.createElement("tr");
        for (let j = 0; j < width; j++)
        {
            var data = document.createElement("td");
            data.onclick = () => { column_click(j); };

            var blank = document.createElement("div");
            blank.className = "blank";
            data.appendChild(blank);
            row.appendChild(data);
        }
        table.appendChild(row);
    }

    update();
    setInterval(update, 500);
}

function request(page, callback)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            callback(xhttp.responseText);
        }
    };
    xhttp.open("GET", page, true);
    xhttp.send();
}

function update()
{
    request("/curr_turn", (data) => {
        if (data != "false")
        {
            var info = JSON.parse(data);
            var board = info["data"];
            for (var y = 0; y < height; y++)
            {
                for (var x = 0; x < width; x++)
                {
                    var p = board[y][x];
                    if (p != null)
                        set(x, y, p);
                }
            }

            var turn_text = info["turn_text"];
            turn.innerHTML = turn_text;
        }
    });
}

function column_click(id)
{
    request("/place/" + id, (data) => {
        if (data == "true")
            place(id, player_colour);
    });
}

function get_space(x, y)
{
    var row = table.childNodes[y];
    var space = row.childNodes[x];
    return space;
}

function set(x, y, player)
{
    var space = get_space(x, y);
    if (space.childNodes[0].className == "blank")
    {
        var img = document.createElement("img");
        img.src = "static/" + player;
        space.innerHTML = "";
        space.appendChild(img);
    }
}

function place(x, player)
{
    for (var y = height - 1; y >= 0; y--)
    {
        var space = get_space(x, y);
        if (space.childNodes[0].className == "blank")
        {
            set(x, y, player);
            break;
        }
    }
}
