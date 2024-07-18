
// Afficher la div answer et cacher le bouton au clic
document.getElementById('submit-button').addEventListener('click', function() {
    var answer_div = document.getElementById('answer-container');
    var review_div = document.getElementById('review-container');
    var submit_div = document.getElementById('submit-container');
    answer_div.style.display = 'block';
    review_div.style.display = 'block';
    submit_div.style.display = 'none';
});