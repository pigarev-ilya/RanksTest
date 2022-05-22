const stripe = Stripe("Stripe Publishable key");
const elementID = window.location.href.split('/').pop();

document.querySelectorAll('#buyOrderBtn, #buyItemBtn').forEach(item => {
    item.addEventListener("click", event => {
        if (event.target === document.querySelector('#buyOrderBtn')) {
            fetch("/order/buy/" + elementID)
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    return stripe.redirectToCheckout({sessionId: data.sessionId})
                })
                .then((res) => {
                    console.log(res);
                });
        } else if (event.target === document.querySelector('#buyItemBtn')) {
            fetch("/buy/" + elementID)
                .then((result) => {
                    return result.json();
                })
                .then((data) => {
                    // Redirect to Stripe Checkout
                    return stripe.redirectToCheckout({sessionId: data.sessionId})
                })
                .then((res) => {
                    console.log(res);
                });
        }
    })
})

