// index.js
document.addEventListener("DOMContentLoaded", function () {
  const frontCard1 = document.getElementById("frcard-1");
  const frontCard2 = document.getElementById("frcard-2");
  const frontCard3 = document.getElementById("frcard-3");
  const behindCard = document.getElementById("be-card");

  // Cuando el ratón entra en la tarjeta frontal
    frontCard1.addEventListener("mouseenter", function () {
      frontCard1.classList.add("show-front-card");
      frontCard1.classList.add("flip-ani2");
      behindCard.classList.add("show-behind-card");
      behindCard.classList.add("flip-ani");
    });
  // Cuando el ratón sale de la tarjeta frontal
    behindCard.addEventListener("mouseleave", function () {
      frontCard1.classList.remove("show-front-card");
      frontCard1.classList.remove("flip-ani2");
      behindCard.classList.remove("show-behind-card");
      behindCard.classList.remove("flip-ani");
    });

    frontCard2.addEventListener("mouseenter", function () {
      frontCard2.classList.add("show-front-card");
      frontCard2.classList.add("flip-ani2");
    });
    // Cuando el ratón sale de la tarjeta frontal
    frontCard2.addEventListener("mouseleave", function () {
      frontCard2.classList.remove("show-front-card");
      frontCard2.classList.remove("flip-ani2");
    });
    frontCard3.addEventListener("mouseenter", function () {
      frontCard3.classList.add("show-front-card");
      frontCard3.classList.add("flip-ani2");
    });
    // Cuando el ratón sale de la tarjeta frontal
    frontCard3.addEventListener("mouseleave", function () {
      frontCard3.classList.remove("show-front-card");
      frontCard3.classList.remove("flip-ani2");
    });
});
