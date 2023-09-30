////////////////////////////////////////////////////////////////////////////////////////////////
//                 Socket code                                                                //
////////////////////////////////////////////////////////////////////////////////////////////////

const socket = io.connect('http://localhost:5000', {
    transports: ['websocket'], // Use WebSocket transport for development
    upgrade: false, // Prevent automatic transport upgrade
    reconnection: true, // Enable reconnection
    reconnectionDelay: 1000, // Reconnect after 1 second (adjust as needed)
});

socket.on('connect', () => {
    console.log('Connected to Flask-SocketIO server');
});

socket.on('disconnect', () => {
    console.log('disconnected from Flask-SocketIO server')
});

socket.once('start game', () => {
    document.getElementById("myModal").style = "display: none";
});

function joinRoom(user) {
    socket.emit('join', user, (response) => {
        console.log(response);
    });
}

function startGameEmit(user) {
    // console.log("In startGame")
    socket.emit('start', user, () => {
    });
}

function discardEquipEmit(equipment_name, room_id) {
    socket.emit('discardEquip', equipment_name, room_id, () => {
    });
}

function increaseCount(room_id) {
    socket.emit('addcard', room_id, () => {

    });
}


////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////
//                 React code                                                                 //
////////////////////////////////////////////////////////////////////////////////////////////////


function Game() {
    const [portrait, setPortrait] = React.useState("");
    const [crew, setCrew] = React.useState("");
    const [equipment, setEquipment] = React.useState({});
    const [roomLoaded, setRoomLoaded] = React.useState(false);
    const [gameStarted, setGameStarted] = React.useState(false);
    const [drawCardImage, setDrawCardImage] = React.useState("/static/img/deck_back_1.jpg");
    const [shipCardImage, setShipCardImage] = React.useState("/static/img/deck_back_2.jpg");
    const [drawCardStrength, setDrawCardStrength] = React.useState("");
    const [drawCardName, setDrawCardName] = React.useState("");
    const [userActive, setUserActive] = React.useState(0);
    const [userCurrent, setUserCurrent] = React.useState(0);
    // DISCARD
    const [discardEquipment, setDiscardEquipment] = React.useState(false);
    // SHIP
    const [shipCount, setShipCount] = React.useState(0);
    const [shipPhase, setShipPhase] = React.useState(false);
    const [shipImage, setShipImage] = React.useState("Empty");
    const [shipName, setShipName] = React.useState("");
    const [shipStrength, setShipStrength] = React.useState(0);
    const [shipEquipment, setShipEquipment] = React.useState({});
    const [HP, setHP] = React.useState(-99);

//////////////////////////////////////////////////////////////////
//          State based sockets                                 //
//////////////////////////////////////////////////////////////////

    socket.on('pass', (response) => {
        console.log(response.activeUser);
        setUserActive(response.activeUser);
        setShipPhase(response.phase);
    });

    socket.on('update deck', (update, user) => {
        console.log(`active user is now ${user}`)
        setUserActive(user);
        setShipCount(shipCount + update);
    });

    socket.once('start game', () => {
        setGameStarted(true);
        document.getElementById("myModal").style = "display: none";
    });
    
    socket.on('discard equipment', (response, user) => {
        console.log(`discarded equipment: ${response}`);
        document.getElementById(`equipment_${response}`).style.filter = "grayscale(100%)";
        setUserActive(user);
    });

    socket.on('activeUser', (user) => {
        setUserActive(user)
    });


// Load webpage 
    
    React.useEffect(() => {
        fetch('/api/load_room')
        .then((response) => response.json())
        .then((gameData) => {
            setPortrait(gameData.image);
            setCrew(gameData.crew);
            setEquipment(gameData.equipment);
            setUserActive(gameData.activeUser);
            setUserCurrent(gameData.currentUser);
            setGameStarted(gameData.started);
        })
        .finally(() => {
            setRoomLoaded(true);
        });
    }, []);

    React.useEffect(() => {
        if (gameStarted) {
            startGameEmit(userCurrent);;
        }
    }, [gameStarted])

    function Equipment() {
        const equipmentList = [];
        var index = 0;
        // console.log(equipment)

        if(roomLoaded) {
            joinRoom(userCurrent);
            for(const item in equipment) {
            //    console.log(equipment[item]);
                const text = equipment[item].discription;
                equipmentList.push(
                    <div key={`div_${index}`} id="flex-cards">
                        <div className="container">
                            <img key={index} className="equipment_cards" id={`equipment_${equipment[item].name}`} src={`/static/img/${crew}/equipment_${equipment[item].name}.png`}/>
                            <div className="overlay">
                                <div className="text">{text}</div>
                            </div>
                        </div>
                    </div>
                );
                index++; 
            }
        }
        else {
            for(const index of Array(6).keys()) {
                const text = "Loading...";
                equipmentList.push(
                    <div key={`div_${index}`} id="flex-cards">
                        <div className="container">
                            <img key={index} className="equipment_cards" id={`equipment_${index}`} src={`/static/img/Loading/equipment_loading.png`}/>
                            <div className="overlay">
                                <div className="text">{text}</div>
                            </div>
                        </div>
                    </div>
                );
            }            
        }
        return (
            <React.Fragment>
                {equipmentList}
            </React.Fragment>
        );
    }

    function Portrait(props) {
        const {portrait, crew, hp} = props;
        if(hp == -99) {
            return (
            <div id ="portrait">
                <img id="portrait_img" src={portrait}/>
                <h2 id="portrait_name">{crew}</h2>
            </div>
        );
        }
        else {
            return (
                <div id ="portrait">
                    <img id="portrait_img" src={portrait}/>
                    <h2 id="portrait_name">{crew} HP:{hp}</h2>
                </div>
                );  
        }
    }

    // Buttons and called functions

    function Buttons(props) {
        const {drawCardImage} = props;

        if(drawCardImage === "/static/img/deck_back_1.jpg") { // drawCardImage gets updated in DrawDeck() 
            return (
                <div id="buttons">
                    <a href="#" className="myButton2" onClick={drawCard}>DRAW</a>

                    <a href="#" className="myButton" onClick={passTurn}>PASS</a>
                </div>
            );
        }
        else {
            return (
                <div id="buttons">
                    <a href="#" className="myButton2" onClick={addCard}>ADD</a>

                    <a href="#" className="myButton" onClick={discardCard}>Discard</a>
                </div>
            );  
        }
    }

    function addCard() {
        if(userCurrent == userActive) {
            fetch(`/api/add/${drawCardName}`, {
                Method: 'POST'
            })
            .then((response) => response.json())
            .then((responseData) => {
                console.log(responseData.success);
                if(responseData.success === true) {
                    setUserActive(responseData.activeUser);
                    setDrawCardImage("/static/img/deck_back_1.jpg");
                    setDrawCardName("");
                    setDrawCardStrength("");
                    increaseCount(responseData.room_id);                
                }          
            });
        }
    }

    function discardCard() {
        if(userCurrent == userActive) {
            setDiscardEquipment(true);
            console.log(discardEquipment);
        }
    }

    function drawCard() {
        // console.log('in drawCard()')
        if(userCurrent == userActive) {
            fetch('/api/draw_card')
            .then((response) => response.json())
            .then((cardData) => {
                // console.log(cardData.image);
                setDrawCardImage(cardData.image);
                // console.log(cardData.name);
                setDrawCardName(cardData.name);
                // console.log(cardData.strength);
                setDrawCardStrength(cardData.strength);
            });
        }
    }
    
    function passTurn() {
        // alert('You just passed your turn!');
        if(userCurrent == userActive) {
            fetch('/api/pass')
            .then((response) => response.json())
            .then((responseData) => {
                // console.log(responseData.success);
                if(responseData.success) {
                    setUserActive(responseData.activeUser);
                }
                if(responseData.shipPhase) {
                    startShip()
                }
            });
        }
    }

    // Deck functions

    function DrawDeck(props) {
        const {image, strength, name} = props;
        var text = "";

        if(strength > 0) {
            text = `STR ${strength}`
        }

        return (
        <div className="deck_container">
            <img id="drawDeck" className="deck" src={image}/> 
            <div className="top-right">{text}</div>
            <div className="bottom">{name}</div>
        </div>
            
        );
    }

    function ShipDeck(props) {
        const {image, count} = props;

        return (
        <div className="deck_container">
            <img id="shipDeck" className="deck" src={image}/> 
            <div className="centered">{count}</div>
        </div>
            
        );
    }

    function Modal(props) {
        const {userActive, userCurrent, gameStarted} = props;
        if(!gameStarted) {
            if(userCurrent == userActive) {
                return (
                    <div id="myModal" className="modal">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h2>Press start when all users have joined</h2>
                            </div>
                            <div className="modal-body">
                            <center>
                            <div class="rules">
                                <center>
                                    <h2> How to play: </h2>
                                    <p><h4>How to win:</h4><br/>
                                    You win by defeating all the aliens in two ships. You do this by being the last player to not pass and using the equipment the crew person has left after the bidding phase.<br/>
                                    Or<br/>
                                    By being the last player to not fail two ships</p>
                                    
                                    <p><h4>How to Loss:</h4><br/>
                                    You can loss by another player winning or by failing twice when going into ships.</p>
                                </center>
                            </div>
                            </center>
                            </div>
                            <div className="modal-footer">
                                <button className="myButton2" onClick={startGame}>Start</button>
                            </div>
                        </div>
                    </div>
                );
            }
            else {
                return (
                    <div id="myModal" className="modal">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h2>Waiting for host to start game...</h2>
                            </div>
                            <div className="modal-body">
                                <p>Need to add some helpful text here</p>
                                <p>Some other text...</p>
                            </div>
                            <div className="modal-footer">
                                <h3>Modal Footer</h3>
                            </div>
                        </div>
                    </div>
                );
            }
        }
        return (
            <div id="myModal"></div>
        )
    }

    function DiscardModal() {
        // console.log("in discardModal")
        // console.log(discardEquipment)


        if(discardEquipment) {

            const optionList = [];

            for(const item of equipment) {
                // console.log(item);
                const text = item[`name`];
                // console.log(text);
                optionList.push(
                    <option key={text} value={text}>{text}</option>
                );
            }

            return (
                <div id="myModal" className="modal">
                    <div className="modal-content">
                    <form onSubmit={discard}>
                        <div className="modal-header">
                            <h2>Select equipment to discard</h2>
                        </div>
                        <div className="modal-body">
                            <div className="modal-equipment">
                            <Equipment equipment={equipment} roomLoaded={roomLoaded} />
                            </div>
                            
                                <label htmlFor="eqiupment-select">Choose a equipment to discard</label>
                                <select name="equipment" id="equipment-select">
                                    <React.Fragment>
                                        {optionList}
                                    </React.Fragment>
                                </select>
                            
                        </div>
                        <div className="modal-footer">
                            <button className="myButton2" type="submit">Submit</button>
                            <button className="myButton2" onClick={cancelDiscard}>Cancel</button>      
                        </div>
                    </form>
                    </div>
                </div>
            );
        }
        return (
            <div></div>
        );
    }

    function cancelDiscard() {
        setDiscardEquipment(false);
    }

    function discard(event) {
        console.log("in discard");
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const equipment = formData.get("equipment")

        console.log(equipment);
        fetch(`/api/discard_equipment/${equipment}`)
        .then((response) => response.json())
        .then((responseData) => {
            if(responseData.success === true) {
                setUserActive(responseData.activeUser);
                setDiscardEquipment(false);
                document.getElementById(`equipment_${responseData.equipment_name}`).style.filter = "grayscale(100%)";
                setDrawCardImage("/static/img/deck_back_1.jpg");
                setDrawCardName("");
                setDrawCardStrength("");
                discardEquipEmit(responseData.equipment_name, responseData.room_id);
            }          
        });

    }

    function startGame() {
        setGameStarted(true);
    }

    //////////////////////////////////////
    //           Ship phase             //
    //////////////////////////////////////

    function ShipModal(props) {
        const {shipEquipment} = props;        

        if(shipPhase) {
            console.log("in shipModal")
            // console.log(shipPhase)
            // console.log(shipImage)
            console.log(shipEquipment)

            const optionList = [];
            const equipmentList = [];
            var index = 0;

            optionList.push(
                <option key='damage' value='damage'>Take {shipStrength} damage</option>
            )
            
            for(const item in shipEquipment) {
                console.log(item);
                const text = shipEquipment[item].name;
                console.log(text);
                optionList.push(
                    <option key={text} value={text}>{text}</option>
                );
            }
            for(const item in shipEquipment) {
                console.log(shipEquipment[item].id);
                const text = shipEquipment[item].discription;
                equipmentList.push(
                    <div key={`div_${index}`} id="flex-cards">
                        <div className="container">
                            <img key={index} className="equipment_cards" id={`equipment_${index}`} src={`/static/img/${crew}/equipment_${shipEquipment[item].name}.png`}/>
                            <div className="overlay">
                                <div className="text">{text}</div>
                            </div>
                        </div>
                    </div>
                );
                index++; 
            }

            return (
                <div id="myModal" className="modal">
                    <div className="modal-content">
                    <form onSubmit={combat}>
                        <div className="modal-header">
                            <h2>Welcome to the Siren - Can you make it?</h2>
                        </div>
                        <div className="modal-body"> 
                            <div className="modal-equipment">
                                <div id="deck-container">
                                    <Portrait portrait={portrait} crew={crew} hp={HP} />
                                    <DrawDeck image ={shipImage} strength={shipStrength} name={shipName}/>
                                </div>
                            <React.Fragment>
                                {equipmentList}
                            </React.Fragment>
                            </div> 
                        </div>
                        <div className="modal-footer">
                            <label htmlFor="eqiupment-select">Choose a equipment to discard</label>
                                <select name="equipment" id="equipment-select">
                                    <React.Fragment>
                                        {optionList}
                                    </React.Fragment>
                                </select>
                                <button type="submit">Select</button>
                        </div>
                    </form>
                    </div>
                </div>
            );
        }
        return (
            <div></div>
        );
    }

    function startShip() {
        
        console.log("getting ship data")
        fetch('/api/ship/start')
        .then((response) => response.json())
        .then((responseData) => {
            // console.log(responseData);
            // console.log(shipImage)
            // console.log(responseData.image)
            setShipImage((prevImage) => responseData.image);
            // console.log(shipImage)
            setShipName((prevName) => responseData.name)
            setShipStrength((prevStrength) => responseData.strength);
            setHP((prevHp) => responseData.hp);
            setShipEquipment((prevShipEquipment) => responseData.equipment);

        })
        .finally(() => {
            setShipPhase(true);
            // console.log(shipImage)
        });
    }

    function combat(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const equipment = formData.get("equipment");
        var queryString;

        console.log(equipment);
        if(equipment == 'damage') {
            queryString = new URLSearchParams({equipment:equipment, enemy:shipName, damage:String(shipStrength)}).toString();
        }
        else {
            queryString = new URLSearchParams({equipment:equipment, enemy:drawCardName, damage:'0'}).toString();            
        }
        const url = `/api/ship/combat?${queryString}`;
        console.log(url)
        fetch(url)
        .then((response) => response.json())
        .then((responseData) => {
            if(responseData.state != '') {
                window.location.replace(`http://127.0.0.1:5000/${responseData.state}`);
            }
            setShipImage(responseData.image)
            setShipName(responseData.name)
            setShipStrength(responseData.strength);
            setHP(responseData.hp);
            setShipEquipment(responseData.equipment);
            console.log(shipEquipment)
        });

    }

    //////////////////////////////////////
    //           Main window            //
    //////////////////////////////////////

    return (
        <React.Fragment>
            <div className="main">
                <div className="game">
                    <Portrait portrait={portrait} crew={crew} hp={HP} />
                    <Equipment equipment={equipment} roomLoaded={roomLoaded} />
                    <div id="deck-container">
                        <Buttons drawCardImage={drawCardImage} />
                        <ShipDeck image ={shipCardImage} count ={shipCount}/>
                        <DrawDeck image ={drawCardImage} strength={drawCardStrength} name={drawCardName}/> 
                    </div>
                </div>
                <Modal userActive={userActive} userCurrent={userCurrent} gameStarted={gameStarted} />
                <DiscardModal discardEquipment={discardEquipment} />
                <ShipModal shipEquipment={shipEquipment}/>
            </div>
        </React.Fragment>
    );
}



ReactDOM.render(<Game />, document.querySelector('#root'));

////////////////////////////////////////////////////////////////////////////////////////////////