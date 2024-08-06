const text = document.querySelectorAll('h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li', 'td', 'caption', 'span', 'a');
console.log(text);

for (let i = 0; i <text.length; i++){
    text[i].innerHTML = "fuck Off";
}