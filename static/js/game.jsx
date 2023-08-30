function Game() {
    const [portrait, setPortrait] = React.useState("");
    const [crew, setCrew] = React.useState("");
    const [equipment, setEquipment] = React.useState({});
    const [roomLoaded, setRoomLoaded] = React.useState(false);
    const [gameStarted, setGameStarted] = React.useState(false);
    const [drawCardImage, setDrawCardImage] = React.useState("/static/img/deck_back_1.jpg");
    const [drawCardStrength, setDrawCardStrength] = React.useState("");
    const [drawCardName, setDrawCardName] = React.useState("");
    const [userActive, setUserActive] = React.useState(0);
    const [userCurrent, setUserCurrent] = React.useState(0);
    const [count, setCount] = React.useState(0);

// Load webpage 
    
    React.useEffect(() => {
        fetch('/api/load_room')
        .then((response) => response.json())
        .then((gameData) => {
            console.log(gameData.image);
            console.log(gameData.crew);
            console.log(gameData.equipment);
            console.log(gameData.activeUser);
            console.log(gameData.currentUser);
            setPortrait(gameData.image);
            setCrew(gameData.crew);
            setEquipment(gameData.equipment);
            setUserActive(gameData.activeUser);
            setUserCurrent(gameData.currentUser);
            console.log(roomLoaded)
        })
        .finally(() => {
            setRoomLoaded(true);
        });
    }, []);

// Check for updates
    
    // React.useEffect(() => {
    //     if(roomLoaded === true) {
    //         setTimeout(() => {
    //         setCount((count) => count + 1);
    //         }, 5000);
    //         console.log(count);
    //     }
    // });

    function Equipment() {
        const equipmentList = [];
        var index = 0;
        console.log(equipment)

        if(roomLoaded) {
            for(const item of equipment) {
                console.log(item)
                const text = item[`discription`];
                equipmentList.push(
                    <div key={`div_${index}`} id="flex-cards">
                        <div className="container">
                            <img key={index} className="equipment_cards" id={`equipment_${index}`} src={`/static/img/${crew}/equipment_${index}.png`}/>
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
            </ React.Fragment>
        );
    }

    function Portrait(props) {
        const {portrait, crew} = props;
        return (
        <div id ="portrait">
            <img id="portrait_img" src={portrait}/>
            <h2 id="portrait_name">{crew}</h2>
        </div>
        );
    }

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
            }          
        });
    }

    function discardCard() {

    }

    function DrawDeck(props) {
        const {image, strength, name} = props;
        var text = "";

        if(strength > 0) {
            text = `STR ${strength}`
        };

        return (
        <div className="deck_container">
            <img id="drawDeck" className="deck" src={image}/> 
            <div className="top-right">{text}</div>
            <div className="top-left">{name}</div>
        </div>
            
        );
    }

    function drawCard() {
        // console.log('in drawCard()')
            fetch('/api/draw_card')
            .then((response) => response.json())
            .then((cardData) => {
                console.log(cardData.image);
                setDrawCardImage(cardData.image);
                console.log(cardData.name);
                setDrawCardName(cardData.name);
                console.log(cardData.strength);
                setDrawCardStrength(cardData.strength);
            });
      }
    
    function passTurn() {
        // alert('You just passed your turn!');
        if(userCurrent == userActive) {
            fetch('/api/pass')
            .then((response) => response.json())
            .then((responseData) => {
                console.log(responseData.success);
                if(responseData.success) {
                    setUserActive(responseData.activeUser);
                }
            });
        }
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
                                <p>Need to add some helpful text here</p>
                                <p>Some other text...</p>
                            </div>
                            <div className="modal-footer">
                                <a href="#" className="myButtonStart" onClick={startGame}>Start</a>
                                <h3>Modal Footer</h3>
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
            <div></div>
        )
    }

    function startGame() {
        var modal = document.getElementById("myModal");
        modal.style.display = "none";
        setGameStarted(true);
    }

    return (
        <React.Fragment>
             <div className="main">
                 <div className="game">
                    <Portrait portrait={portrait} crew={crew} />
                     <Equipment equipment={equipment} roomLoaded={roomLoaded} />
                     <div id="deck-container">
                        <Buttons drawCardImage={drawCardImage} />
                        <img id="shipDeck" className="deck" src="/static/img/deck_back_2.jpg"/>
                        <DrawDeck image ={drawCardImage} strength={drawCardStrength} name={drawCardName}/> 
                     </div>
                 </div>
                 <Modal userActive={userActive} userCurrent={userCurrent} gameStarted={gameStarted} />
             </div>
        </React.Fragment>
    )
}



ReactDOM.render(<Game />, document.querySelector('#root'));