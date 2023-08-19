'use strict';
// Javascript for main.html

// Event listener to handle user entering a room code 
// and clicking Join button
function activeRoom(evt) {
    evt.preventDefault();
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
            console.log("Redirecting");
            redirectPost(`/room/${joinRoomJSON.roomcode}`);
        }
    });
}

document.querySelector('#join-button').addEventListener('click', activeRoom);

// Event listener to handle user clicking create room button
function createRoom(evt) {
    evt.preventDefault();
    // console.log("calling fetch");
    fetch("/create-room", {
        method: "POST"
      })
    .then((response) => response.json())
    .then((createRoomJSON) => {
        // console.log(`in response, createRoom = ${createRoomJSON.status} roomcode = ${createRoomJSON.roomcode}`);
        if(createRoomJSON.status === 'fail') {
            alert("failed to create room. Please try again later.");
        }
        else {
            console.log("Redirecting");
            redirectPost(`/room/${createRoomJSON.roomcode}`);
        }
    })
    .catch((error) => {
        console.error("An error occurred:", error);
        alert("An error occurred while creating the room. Please try again later.");
    });
    // console.log("Waiting for response");
}

document.querySelector('#create-button').addEventListener("click", createRoom);


/*****************************
        Hepler Functions
******************************/

function redirectPost(url) {
    var form = document.createElement('form');
    document.body.appendChild(form);
    form.method = 'post';
    form.action = url;
    // for (var name in data) {
    //     var input = document.createElement('input');
    //     input.type = 'hidden';
    //     input.name = name;
    //     input.value = data[name];
    //     form.appendChild(input);
    // }
    form.submit();
}