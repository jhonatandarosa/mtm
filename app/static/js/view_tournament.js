function editGame(gameId, p1Name, p1Wins, p2Name, p2Wins) {
    $('#p1Name').text(p1Name);
    $('#p1Wins').val(p1Wins);
    $('#p2Name').text(p2Name);
    $('#p2Wins').val(p2Wins);

    $('#editGame').attr('gameId', gameId);

    $('#p1Name').addClass('active');
    $('#p2Name').addClass('active');

    $('#editGame').modal('open');

}

function saveGame() {
    const gameId = $('#editGame').attr('gameId');
    const p1Wins = parseInt($('#p1Wins').val());
    const p2Wins = parseInt($('#p2Wins').val());

    const payload = {
        p1Wins,
        p2Wins
    };

    $.ajax({
        type: 'PUT',
        url: '/api/games/'+gameId,
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8",
        success: () => {
            Materialize.toast('Game edited!', 4000);
            window.location.reload()
        },
        error: (xhr, status, error) => {
            Materialize.toast('Error editing game!', 4000);
        }
    });
}

function finishTournament(tid) {
    const payload = {
        status: 'finished'
    };

    $.ajax({
        type: 'PUT',
        url: '/api/tournaments/'+tid +'/status',
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8",
        success: () => {
            Materialize.toast('Finished!', 4000);
            window.location.reload()
        },
        error: (xhr, status, error) => {
            Materialize.toast('Error changing status!', 4000);
        }
    });
}