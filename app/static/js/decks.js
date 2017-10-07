function createDeck() {
    const payload = {
        name: $('#name').val()
    };

    $.ajax({
        type: 'POST',
        url: '/api/decks',
        data: JSON.stringify(payload),
        contentType: "application/json; charset=utf-8",
        success: () => {
            // Materialize.toast(message, displayLength, className, completeCallback);
            Materialize.toast('Deck created!', 4000);
            window.location.reload()
        },
        error: (xhr, status, error) => {
            Materialize.toast('Error creating deck!', 4000);
        }
    });
}
