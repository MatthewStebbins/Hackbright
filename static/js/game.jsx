function Game() {
    const [portrait, setPortrait] = React.useState("");
    const [crew, setCrew] = React.useState("");
    const [equipment, setEquipment] = React.useState({});
    const [roomLoaded, setRoomLoaded] = React.useState(false);

    React.useEffect(() => {
        fetch('/api/load_room')
        .then((response) => response.json())
        .then((gameData) => {
            console.log(gameData.image);
            console.log(gameData.crew);
            console.log(gameData.equipment);
            setPortrait(gameData.image);
            setCrew(gameData.crew);
            setEquipment(gameData.equipment)
        })
        .finally(() => {
            setRoomLoaded(true);
        });
    }, []);

    function Equipment() {
        const equipmentList = [];

        if(roomLoaded) {
            for(const index of Array(6).keys()) {
                const text = equipment[`${index}`];
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

    return (
        <React.Fragment>
             <div className="main">
                 <div className="game">
                    <Portrait portrait={portrait} crew={crew} />
                     <Equipment equipment={equipment} roomLoaded={roomLoaded} />
                     <div id="deck-container">
                         <div id="buttons">
                             <a href="#" className="myButton2">DRAW</a>

                             <a href="#" className="myButton">PASS</a>
                         </div>
                         <img id="deck" src="/static/img/deck_back_2.jpg"/>
                         <img id="deck" src="/static/img/deck_back_1.jpg"/> 
                     </div>
                 </div>
             </div>
        </React.Fragment>
    )
}

ReactDOM.render(<Game />, document.querySelector('#root'));