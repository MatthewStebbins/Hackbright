'use strict';
// Javascript for main.html
console.log('In MAIN.JS');
// Event listener to handle user entering a room code 
// and clicking Join button
function activeRoom(evt) {

    console.log('in isActiveRoom');
    const roomcode = document.querySelector('#room').value;
    console.log(roomcode);
    alert(roomcode);
}

const button = document.querySelector('#join-button');
console.log(button);
button.addEventListener('click', activeRoom);