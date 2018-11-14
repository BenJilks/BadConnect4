
var socket;
const width = 80;
const height = 130;
var curr_card = null;
var offsetX, offsetY;
var curr_z;
var curr_cards;
var players;

function init()
{
    curr_cards = [];
    curr_z = 0;

    socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() 
    {
        socket.emit('game_started_cards');
    });

    socket.on('give_card', function(data_json) 
    {
        var data = JSON.parse(data_json);
        if (data['for'] == player)
        {
            var card_data = data['card'];
            new_card(card_data);
        }
    });

    socket.on('reset_cards', function(data_json)
    {
        var data = JSON.parse(data_json);
        console.log(data['for'] + ", " + player);
        if (data['for'] == player)
        {
            for (var i = 0; i < curr_cards.length; i++)
            curr_cards[i].remove();
            curr_cards = [];
            
            var cards = data['data'];
            for (var i = 0; i < cards.length; i++)
            {
                var card_data = cards[i];
                var card = new_card(card_data);
                card.style.left = card_data['x'] + 'px';
                card.style.top = card_data['y'] + 'px';
                card.pos_x = card_data['x'];
                card.pos_y = card_data['y'];
            }

            var give_area = document.getElementById('give_area');
            give_area.innerHTML = "";
            players = data['players'];
            for (var i = 0; i < players.length; i++)
            {
                var p = players[i];
                var name = p['name'];
                var id = p['id'];
                var row = document.createElement('tr');
                var data = document.createElement('td');
                var title = document.createElement('h1');
                title.innerHTML = name;
                data.appendChild(title);
                row.appendChild(data);
                give_area.appendChild(row);
            }
        }
    });
}

function hide_card(card)
{
    var img = card.childNodes[0];
    img.src = "static/Cards/back.png";

    if (card.childNodes.length > 1)
    {
        card.childNodes[1].style = "display: none";
        card.childNodes[2].style = "display: none";
    }
}

function show_card(card)
{
    var img = card.childNodes[0];
    img.src = "static/Cards/" + card.card_set + "_" + card.card_number + ".svg";

    if (card.childNodes.length > 1)
    {
        card.childNodes[1].style = "display: inline";
        card.childNodes[2].style = "display: inline";
    }
}

function flip_card(card)
{
    if (card.card_back)
        show_card(card);
    else
        hide_card(card);
    card.card_back = !card.card_back;

    socket.emit('update_position', card.card_id, 
        card.pos_x, card.pos_y, card.card_back);
}

function new_card(card_data)
{
    var card = make_card(card_data['set'], card_data['number'], card_data['id']);
    if (card_data['back'])
        flip_card(card);

    document.body.appendChild(card);
    curr_cards.push(card);
    return card;
}

function make_card(set, number, id)
{
    var card = document.createElement('div');
    card.className = 'card';
    card.onmousedown = () => { select_card(card) };
    card.ondblclick = () => { flip_card(card); };
    card.card_id = id;
    card.card_set = set;
    card.card_number = number;
    card.card_back = false;

    var img = document.createElement('img');
    img.src = "static/Cards/" + set + "_" + number + ".svg";
    card.appendChild(img);

    if (number <= 10)
    {
        var top = document.createElement('text');
        top.id = "top";
        top.innerHTML = number;
        card.appendChild(top);

        var bottom = document.createElement('text');
        bottom.id = "bottom";
        bottom.innerHTML = number;
        card.appendChild(bottom);
    }
    return card;
}

function card_drag(event)
{
    if (curr_card != null)
    {
        var x = event.x - width / 2;
        var y = event.y - height / 2;
        curr_card.pos_x = x;
        curr_card.pos_y = y;
        curr_card.style.left = x + "px" 
        curr_card.style.top = y + "px";
    }
}

function select_card(card)
{
    card.style.zIndex = ++curr_z;
    curr_card = card;
}

function deselect_card()
{
    if (curr_card != null)
    {
        if (curr_card.pos_x >= window.innerWidth - 200 && players.length >= 1)
        {
            var id = parseInt(curr_card.pos_y / (window.innerHeight / players.length));
            var p = players[id];
            curr_card.remove();
            socket.emit('give_card_to', curr_card.card_id, p['id']);
        }
        else
        {
            socket.emit('update_position', curr_card.card_id, 
                curr_card.pos_x, curr_card.pos_y, curr_card.card_back);
        }
        curr_card = null;
    }
}

function draw_card()
{
    socket.emit('draw_card');
}

function draw_card_down()
{
    socket.emit('draw_card_down');
}
