$('.gridTabBtn').on('click', function(data){
    var gridId = $(this)[0].id;
    changeGridVal(gridId);
});

getGridVal = (function(){
    var gridData = {}
    $('.gridTabBtn').each(function(){
        var gridId = this.id;
        var gridInput = id_icon_map[$("#gridInput" + gridId).val() - 1]['pk'];
        gridData[gridId] = gridInput;
    })
    console.log(gridData);
    return gridData
})

changeGridVal = (function(id){
    console.log('changed')
    var gridIcon = $("#gridIcon" + id);
    var gridLoadout = $("#gridLoadout" + id);
    var gridInput = $("#gridInput" + id);

    var soldierCount = Object.keys(id_icon_map).length;
    var soldierId = gridInput.val() % soldierCount;

    gridIcon.attr('class', id_icon_map[soldierId]['icon_class']);
    gridLoadout.html(id_icon_map[soldierId]['loadout']);
    soldierId ++
    gridInput.val(soldierId);
})

throwChallenge = (function(hitmenGamerTag, blackBriarGamerTag){
    var postData = {};
    postData['hitmen_gamer_tag'] = hitmenGamerTag;
    postData['hitmen_strategy_grid'] = getGridVal();
    var data = {'post_data': JSON.stringify(postData)};
    var url = getChallengePlayerURL(blackBriarGamerTag);
    $.post(url, data, function(data){
        response = data;
        alert('challenge id ' + response['challenge_id'] + ' created')
    });
})

$('#makeWarAndLoveBtn').on('click', function(data){
    throwChallenge(HITMEN_GAMER_TAG, $('#blackBriarSelector').val())
});

$('.makeStrategyBtn').on('click', function(data){
    loadResponseGrid();
});

loadResponseGrid = (function(){
    $('#gridTable').remove();
    url = LOAD_GRID_URL;
    $.get(url, function(data){
        response = data;
        console.log(response);
        $('#fightChallengeGridHolder').html(response.rendered_html);
        gameInitScript();
    })
    $('#makeWarAndLoveBtn').on('click', function(data){
        fightChallenge(3)
    });
})


fightChallenge = (function(challengeId){
    var postData = {};
    postData['blackbriar_strategy_grid'] = getGridVal();
    var data = {'post_data': JSON.stringify(postData)};
    var url = getFightChallengeURL(challengeId);
    $.post(url, data, function(data){
        response = data;
        console.log(response);
    });
})

gameInitScript = (function(){
    $('.gridTabBtn').each(function(){changeGridVal(this.id)});
})

gameInitScript();
