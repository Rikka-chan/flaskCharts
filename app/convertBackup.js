/**
 * Created by kamina on 2/20/16.
 */
var fs=require('fs');
var rr=fs.createReadStream('/home/kamina/new_ind1.json');


rr.setEncoding('utf8');
var brackets=0;
var flag=0;
rr.on('data',function(chunk){
    for (var i=0;i<chunk.length;i++){
        if(!flag && chunk[i]=='['){
            flag=1;
            continue;
        }
        if(chunk[i]=='{')brackets++;
        if(chunk[i]=='}')brackets--;
        if(brackets==0 && chunk[i]==',') continue;
        fs.appendFileSync('/home/kamina/new_ind12.json',chunk[i]);
    }
});