function showOptions(){
    document.getElementById("game-options").innerHTML = getGameOptions();
}

function getGameOptions(){
    return( `<ul class="game-options">
    <li><a href="{{url_for('Engines.EngineCreation.engineConstructor.game_type1', game_name_='Game1', game_pin_='1234') }}">game type 1</a></li>
    <li><a href="{{url_for('Engines.EngineCreation.engineConstructor.game_type2', game_name_='Game2', game_pin_='5678') }}">game type 2</a></li>
    <li><a href="{{url_for('Engines.EngineCreation.engineConstructor.game_type3', game_name_='Game3', game_pin_='9101') }}">game type 3</a></li>
    <li><a href="{{url_for('Engines.EngineCreation.engineConstructor.game_type4', game_name_='Game4', game_pin_='1121') }}">game type 4</a></li>
</ul>`)
}
