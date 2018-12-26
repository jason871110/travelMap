var judge = new Array(10);
for(i=0;i<10;i++){
    judge[i]=0;
}
var transport = new Array(6);
for(i=0;i<6;i++){
    transport[i]=0;
}
function changeBack(id){
    
    for(i=1;i<=10;i++){
        /*btn*/
        var s = new String("bt");
        var a = new String("un");
        var ju = a.concat(i);
        var change = s.concat(i);
        /*tran*/
        var s2 = new String("tran");
        var a2 = new String("atran");
        var ju2 = s2.concat(i);
        var change2 = a2.concat(i);
        if(id==ju){
            var e = document.getElementById(id);
            e.id = change;
            judge[i-1]=1;
        }
        if(id==change){
            var e = document.getElementById(id);
            e.id = ju;
            judge[i-1]=0;
        }
        if(i<=6){
            if(id==ju2){
                var e = document.getElementById(id);
                e.id = change2;
                transport[i-1]=1;
            }
            if(id==change2){
                var e = document.getElementById(id);
                e.id = ju2;
                transport[i-1]=0;
            }
        }
    }
    changeintNum(returnJudge());
    changeintNum2(returnTran());
}
function returnTran(){
    var sum=0;
    for(i=0;i<6;i++){
        sum+=transport[i];
    }
    return sum; 
    
}
function returnJudge(){
    var sum=0;
    for(i=0;i<10;i++){
        sum+=judge[i];
    }
    return sum;
   
}
function changeintNum(i){
    var str=new String(i);
    var str2=str.concat("/10");
    document.getElementById("intNum").textContent=str2;
}
function changeintNum2(i){
    var str=new String(i);
    var str2=str.concat("/6");
    document.getElementById("intNum2").textContent=str2;
}