const socket = io.connect('http://localhost:5000', {
    // cors: {
    //     origin: "http://localhost:5002",
    //     credentials: true
    // },
    transports: ['websocket'], // Use WebSocket transport for development
    upgrade: false, // Prevent automatic transport upgrade
    reconnection: true, // Enable reconnection
    reconnectionDelay: 1000, // Reconnect after 1 second (adjust as needed)
});
// Event handler for when the client is successfully connected
socket.on('connect', () => {
    console.log('Connected to Flask-SocketIO server');
    // console.log(room)
    // socket.emit('join', 1, (response) => {
    //     console.log(response);
    // });
});

export function joinRoom() {
    socket.emit('join', (response) => {
        console.log(response);
    });
}

socket.on('disconnect', () => {
    console.log('disconnected from Flask-SocketIO server')
});

// Event handler for custom events sent from the server
// socket.on('custom_event_name', (data) => {
//     console.log('Received data from server:', data);
// });

// You can also send data to the server
// document.querySelector('#send-button').addEventListener('click', () => {
//     const message = 'Hello, server!';
//     socket.emit('custom_event_name', { message });
// });