
var socket;
var player_list;
var width, height;
var connect;

function init()
{
    socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() 
    {
        socket.emit('join', lobby);
    });

    socket.on('message', function (players)
    {
        player_list.innerHTML = players;
    });

    socket.on('goto_game', function()
    {
        window.location = '/game';
    });

    player_list = document.getElementById('player_list');
    width = document.getElementById('width');
    height = document.getElementById('height');
    connect = document.getElementById('connect');
}

function send_start()
{
    socket.emit('start_game', width.value, 
        height.value, connect.value);
}
