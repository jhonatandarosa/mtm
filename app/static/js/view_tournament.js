function createPlayer() {
    const payload = {
        name: $('#name').val()
    };

    $.ajax({
        type: 'POST',
        url: '/api/players',
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        success: () => {
            // Materialize.toast(message, displayLength, className, completeCallback);
            Materialize.toast('Player created!', 4000);
            window.location.reload()
        },
        error: () => {
            Materialize.toast('Error creating player!', 4000);
        }
    });
}


function editGame(gameId, p1Name, p1Wins, p2Name, p2Wins) {
    $('#p1Name').text(p1Name);
    $('#p1Wins').val(p1Wins);
    $('#p2Name').text(p2Name);
    $('#p2Wins').val(p2Wins);
    $('#editGame').modal('open');
}