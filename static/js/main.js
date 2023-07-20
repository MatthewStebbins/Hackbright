'use strict';
// Javascript for main.html

// Event listener to handle user entering a room code 
// and clicking Join button
function activeRoom(evt) {
    console.log('in isActiveRoom');
    const roomcode = document.querySelector('#room').value;
 //   console.log(roomcode);
    const queryString = new URLSearchParams({room:roomcode}).toString();
    const url = `/join-room?${queryString}`;
    
    fetch(url)
    .then((response) => response.json())
    .then((joinRoomJSON) => {
 //       console.log(joinRoomJSON)
        if (joinRoomJSON.status === 'inactive') {
            alert(`Room code ${joinRoomJSON.roomcode} is not avalible`);
        }
        else {
            window.location.replace(`/room/${joinRoomJSON.roomcode}`);
        }
    });
}

document.querySelector('#join-button').addEventListener('click', activeRoom);

// Event listener to handle user clicking create room button
function createRoom(evt) {
    fetch('/create-room')
    .then((response) => response.json())
    .then((createRoomJSON) => {
        if(createRoom.status === 'fail') {
            alert("failed to create room. Please try again later.");
        }
        else {
            window.location.replace("/todo");
        }
    });
}