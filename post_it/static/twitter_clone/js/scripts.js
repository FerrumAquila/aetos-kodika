<!--=== Follow Animation and Process - Start ===-->
  followUser = function(thisLOL, url){
    thisLOL.switchClass("glyphicon-plus", "glyphicon-ok")
    console.log("Following URL Fucked UP" + url)
    $.get(url, function(data){
      console.log(data)
      responseJSON = jQuery.parseJSON(data)
      //location.reload()
    })
    //location.reload()
  }
<!--=== Follow Animation and Process - End ===-->

<!--=== Tweet Popup and Process - Start ===-->
  tweet = function(url){
    form = $("#tweetForm")
    form = form.serialize()
    console.log("Tweet URL " + url)
    $.post(url, form, function(data){
      console.log(data)
      responseJSON = jQuery.parseJSON(data)
      if(responseJSON.status == "success"){
        //alert(responseJSON.message)
        location.reload()
      }else{
        if(responseJSON.status == "error"){
          alert(responseJSON.message)
        }else{
          alert("Sorry cannot understand Server Error")
        }
      }
    })
    //location.reload()
  }
<!--=== Tweet Popup and Process - End ===-->

<!--=== Like Tweet and Process - Start ===-->
  likeTweet = function(thisLOL, url, tweet_id){
    console.log("Tweet Like URL " + url)
    /**/
    $.get(url, function(data){
      console.log(data)
      responseJSON = jQuery.parseJSON(data)
      if(responseJSON.status == "success"){
        //alert(responseJSON.message)
        //location.reload()
        likeCountID = "#likeCountID" + tweet_id
        likeTweetID = "#likeTweetID" + tweet_id
        if(responseJSON.instructions == "add"){

          if(parseInt($(likeCountID).html())){//first like
            likeCount = parseInt($(likeCountID).html()) + 1
          }else{//second and more likes
            likeCount = 1
          }
          $(likeTweetID).html('Unlike <span id="' + likeCountID + '" class="badge">' + likeCount + '</span>')
          console.log("Like Counts Increased To " + likeCount)

        }else{
        if(responseJSON.instructions == "remove"){

          if($(likeTweetID).children().html() == "1"){//first like
            $(likeTweetID).children().remove()
            $(likeTweetID).html('Like')
            console.log("Like Counts Decreased To Zero")
          }else{//second and more likes
            likeCount = parseInt($(likeCountID).html()) - 1
            $(likeTweetID).html('Like <span id="' + likeCountID + '" class="badge">' + likeCount + '</span>')
            console.log("Like Counts Decreased To " + likeCount)
          }

        }}

      }else{
        if(responseJSON.status == "error"){
          alert(responseJSON.message)
        }else{
          alert("Sorry cannot understand Server Error")
        }
      }
    })
    /**/
  }
<!--=== Like Tweet and Process - End ===-->

<!--=== Swipe Left - Start ===-->
  swipeLeft = function(url){
    loggedInUsername = "{{ request.user.username|escapejs }}"
    $("#main").swipe({
      swipeLeft:function(event, direction, distance, duration, fingerCount) {
        //alert("you swipeLeft and wanted to goto timeline")
        window.location.href = url
      }
    });
  }
<!--=== Swipe Left - End ===-->

<!--=== Swipe Right - Start ===-->
  swipeLeft = function(url){
    $("#main").swipe({
      swipeRight:function(event, direction, distance, duration, fingerCount) {
        //alert("you swipeRight and wanted to home")
        window.location.href = url
      }
    });
  }
<!--=== Swipe Right - End ===-->