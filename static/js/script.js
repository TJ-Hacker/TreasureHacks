let x;
fetch('/data')
.then(response => response.json())
.then(data => {
    console.log(data);
    for(i in data){
        console.log('Longitude: ' + data[i])
    }
})

