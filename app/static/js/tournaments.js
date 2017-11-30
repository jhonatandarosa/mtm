
function createTournament() {
    const name = $('#name').val();
    const tier = $('#tier').val();
    const type = parseInt($('#type').val());
    const players = $('[id*=player_]:checked');
    const pids = [];
    for (let player of players) {
        let id = player.id;
        id = parseInt(id.replace('player_', ''));
        pids.push(id);
    }

    const payload = {
        name,
        type,
        tier,
        players: pids
    };

    $.ajax({
        type: 'POST',
        url: '/api/tournaments',
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8",
        success: () => {
            Materialize.toast('Tournament created!', 4000);
            window.location.reload()
        },
        error: (xhr, status, error) => {
            Materialize.toast('Error creating tournament!', 4000);
        }
    });
}