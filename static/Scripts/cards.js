
const width = 80;
const height = 130;
var curr_card = null;
var offsetX, offsetY;
var curr_z;

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

function init()
{
    curr_z = 0;
    for (var i = 0; i < 10; i++)
    {
        var card = make_card(getRandomInt(4), getRandomInt(12) + 1);
        card.style.left = (i * (width + 10) + 10) + "px";
        document.body.appendChild(card);
    }
}

function make_card(set, number)
{
    var card = document.createElement('div');
    card.className = 'card';
    card.onmousedown = () => { select_card(card) };

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
    curr_card = null;
}
