
var socket;
var table, turn;
var last_turn = -1;

function init()
{
    socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function()
    {
        console.log('connected');
        socket.emit('game_started_connect4');
    });

    socket.on('json', function (data)
    {
        console.log('got update');
        var info = JSON.parse(data);
        var board = info['data'];
        for (var y = 0; y < height; y++)
        {
            for (var x = 0; x < width; x++)
            {
                var p = board[y][x];
                if (p != null)
                    set(x, y, p);
            }
        }

        var turn_text = info['turn_text'];
        if (turn_text == player_name + '\'s turn')
            turn.innerHTML = 'your turn';
        else
            turn.innerHTML = turn_text;

        var has_won = info['has_won'];
        if (has_won != null)
        {
            setTimeout(function () 
            {
                alert(has_won + ' won!');
                window.location = '/lobby';
            }, 100);
        }
    });

    table = document.getElementById('table');
    turn = document.getElementById('turn');

    for (var i = 0; i < height; i++)
    {
        var row = document.createElement('tr');
        for (let j = 0; j < width; j++)
        {
            var data = document.createElement('td');
            data.onclick = () => { column_click(j); };

            var blank = document.createElement('div');
            blank.className = 'blank';
            data.appendChild(blank);
            row.appendChild(data);
        }
        table.appendChild(row);
    }
}

function column_click(id)
{
    socket.emit('place', id);
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
    if (space.childNodes[0].className == 'blank')
    {
        var img = document.createElement('img');
        img.src = 'static/' + player;
        space.innerHTML = '';
        space.appendChild(img);
    }
}

function place(x, player)
{
    for (var y = height - 1; y >= 0; y--)
    {
        var space = get_space(x, y);
        if (space.childNodes[0].className == 'blank')
        {
            set(x, y, player);
            break;
        }
    }
}
