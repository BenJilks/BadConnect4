
var socket;
var player_list;
var mode;

var connect4;
var width, height;
var connect;

var cards;

function init()
{
    connect4 = document.getElementById('connect4');
    player_list = document.getElementById('player_list');
    width = document.getElementById('width');
    height = document.getElementById('height');
    connect = document.getElementById('connect');

    cards = document.getElementById('cards');
    mode = 'Connect4';

    socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() 
    {
        socket.emit('join', lobby);
    });

    socket.on('message', function (players)
    {
        player_list.innerHTML = players;
    });

    socket.on('goto_game', function(page)
    {
        window.location = page;
    });
}

function send_start()
{
    if (mode == 'Connect4')
    {
        socket.emit('start_connect4', width.value, 
            height.value, connect.value);
    }
    else
    {
        socket.emit('start_cards');
    }
}

function mode_change(select)
{
    mode = select.value;
    if (mode == "Connect4")
    {
        console.log(connect4);
        connect4.style.display = "block";
        cards.style.display = "none";
    }
    else
    {
        connect4.style.display = "none";
        cards.style.display = "block";
    }
}
