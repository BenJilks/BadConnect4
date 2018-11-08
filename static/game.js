
var table;
var last_turn = -1;
const width = 7;
const height = 6;

function init()
{
    table = document.getElementById("table");
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

    setInterval(update, 100);
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
            if (last_turn != info["last_turn"] && info["is_turn"])
            {
                last_turn = info["last_turn"];
                place(last_turn, "yellow.png");
            }
        }
    });
}

function column_click(id)
{
    request("/place/" + id, (data) => {
        if (data == "true")
            place(id, "red.png");
    });
}

function get_space(x, y)
{
    var row = table.childNodes[y];
    var space = row.childNodes[x];
    return space;
}

function place(x, player)
{
    for (var i = height - 1; i >= 0; i--)
    {
        var space = get_space(x, i);
        if (space.childNodes[0].className == "blank")
        {
            var img = document.createElement("img");
            img.src = "static/" + player;
            space.innerHTML = "";
            space.appendChild(img);
            return true;
        }
    }

    return false;
}
