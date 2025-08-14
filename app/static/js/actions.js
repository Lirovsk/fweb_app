function showOptions(){
    document.getElementById("game-options").innerHTML = getGameOptions();
}

function getGameOptions(){
    return( `<ul class="game-options">
    <li><a href="/auth/setting-room/gameType1">game type 1</a></li>
    <li><a href="/auth/setting-room/gameType2">game type 2</a></li>
    <li><a href="/auth/setting-room/gameType3">game type 3</a></li>
    <li><a href="/auth/setting-room/gameType4">game type 4</a></li>
</ul>`)
}
