document.addEventListener("DOMContentLoaded", function () {
  const frontCards = document.querySelectorAll(".front-card");
  const behindCards = document.querySelectorAll(".behind-card");

  // Cuando el ratón entra en la tarjeta frontal
  frontCards.forEach(function (frontCard) {
    behindCards.forEach(function (behindCard) {
      frontCard.addEventListener("mouseenter", function () {
        frontCard.classList.add("show-front-card");
        frontCard.classList.add("flip-ani2");
        behindCard.classList.add("show-behind-card");
        behindCard.classList.add("flip-ani");
      });
    });
  });
  // Cuando el ratón sale de la tarjeta frontal
  behindCards.forEach(function (behindCard) {
    frontCards.forEach(function (frontCard) {
      behindCard.addEventListener("mouseleave", function () {
        frontCard.classList.remove("show-front-card");
        frontCard.classList.remove("flip-ani2");
        behindCard.classList.remove("show-behind-card");
        behindCard.classList.remove("flip-ani");
      });
    });
  });
});
