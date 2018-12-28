// for(i=1;i<9;i++){
//     var first=new String("p"+i);
//     var pic=new String("imgAnimate/"+i+"/");
//     for(y=1;y<4;y++){
//         var second=first.concat("-"+y);
//         $("#"+second).css({
//             "background-image":"url(\'"+pic.concat(y+"jpeg")+"\')"
//         })
//         console.log("url(\'"+pic.concat(y+".jpeg")+"\')");
//         console.log("#"+second);
//     }
// }

/*change image*/
// function setimage(id){
//     var first=filename.concat(id+"/");
//         $(".picContent1").css({
//             "background-image":"url(\'"+first.concat("1.jpeg")+"\')"
//         })
//         $(".picContent2").css({
//             "background-image":"url(\'"+first.concat("2.jpeg")+"\')"
//         })
//         $(".picContent3").css({
//             "background-image":"url(\'"+first.concat("3.jpeg")+"\')"
//         })    
// }
var judgeShow=false;
var judgeid=0;

function changeBac(id){
    /*
    var pic=new String("/media/"+id);
    //console.log(pic)
    $("#"+"").css({
      "background-image":"url(\'"+pic+"\')"
    })
    */
    if(judgeid!=id){
        $( ".picContent1" ).animate({
            height:"250px"
          }, 1000, function() {
            
          });
          $( ".picContent2" ).animate({
            width:"200px"
          }, 1000, function() {
            
          });
          $( ".picContent3" ).animate({
            height:"150px",
            width:"150px"
          }, 1000, function() {
          });
          judgeid=id;
    }   
    console.log(judgeid)
    // for(i=1;i<9;i++){
    //     judgeShow=false;
    //     if(i==1){
    //         $( ".picContent1" ).animate({
    //             width:"300px",
    //             height:"250px"
    //           }, 5000, function() {
    //             // Animation complete.
    //           });
    //     }
    // }
}
function resizepic(){
    $( ".picContent1" ).animate({
        height:"0px"
      }, 0, function() {
        
      });
      $( ".picContent2" ).animate({
        width:"0px"
      }, 0, function() {
        
      });
      $( ".picContent3" ).animate({
        height:"0px",
        width:"0px"
      }, 0, function() {
      });
}


