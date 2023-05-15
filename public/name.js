let fs = require('fs')

fs.readdir('./Dataset', (err, file)=>{
    file.forEach(ele=>{
        console.log(ele)
    })
})
function listFiles(dir){
    fs.readdir('./Dataset/'+dir, (err, file)=>{
        file.forEach(ele=>{
            console.log(dir+'-Dataset/'+dir+'/'+ele)
        })
    })
}