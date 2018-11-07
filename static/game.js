
var table;
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
}

function request(page, callback)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
        if (this.readyState == 4 && this.status == 200) {
            callback(this.responseText);
        }
    };
    xhttp.open("GET", page, true);
    xhttp.send();
}

function column_click(id)
{
    request("/place/" + id, () => {
        
    });
    place(id, "red.png");
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
