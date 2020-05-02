var entry;
var i;

db.collection("overspeed").orderBy("date", "desc").orderBy("time", "desc").get().then(function(querySnapshot) {
    i = 0;
    querySnapshot.forEach(function(doc) {
        // doc.data() is never undefined for query doc snapshots
        console.log(doc.id, " => ", doc.data());
        entry = doc.data()
        i = i+1;

        if ("imageLink" in entry){
            htmlcontent = `<div class="entry"><div class="serailNo">${i}</div><div class="date">${entry['date']}</div><div class="time">${entry['time']}</div><div class="speed">${entry['speed']}</div><div class="licNo">${entry['licNo']}</div><div class="licError">${entry['licError']}</div><div class="imageLink"><a class="viewButton" href = ${entry['imageLink']} target="_blank"><div>VIEW</div></a></div></div>`
        }

        else{
            htmlcontent = `<div class="entry"><div class="serailNo">${i}</div><div class="date">${entry['date']}</div><div class="time">${entry['time']}</div><div class="speed">${entry['speed']}</div><div class="licNo">${entry['licNo']}</div><div class="licError">${entry['licError']}</div><div class="imageLink"></div></div>`
        }
        document.querySelector('.resultSet').insertAdjacentHTML('beforeend',htmlcontent);
    });
});