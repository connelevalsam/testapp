
var slide_index = 1;  
displaySlides(slide_index);  

function nextSlide(n) {  
    displaySlides(slide_index += n);
}  

setInterval(() => nextSlide(1), 5000)

function currentSlide(n) {  
    displaySlides(slide_index = n);  
}  

function displaySlides(n) {  
    var i;  
    var slides = document.getElementsByClassName("showSlide");  
    if (n > slides.length) { slide_index = 1 }  
    if (n < 1) { slide_index = slides.length }  
    for (i = 0; i < slides.length; i++) {  
        slides[i].style.display = "none";  
    }  
    slides[slide_index - 1].style.display = "block";  
} 


/*
using promise
const list = Array.from(document.querySelector('#foo').children);

const maxLimit = list.length;
const delay = 1000;

// look mah, fancy preloading
Promise.all(list.map(li => 
    preloadTheThings(li.firstChild.src)
)).then(doTheThings);

async function preloadTheThings(thing) {
    const res = await fetch(thing, {
        mode: 'no-cors'
    });
    return res;
}

function doTheThings() {
    let current = 0;
    return setInterval(next, 1000);

    function next() {
        list[current].classList.remove('visible');
        current = ++current % maxLimit;
        list[current].classList.add('visible');
    }
}

doTheThings();

*/