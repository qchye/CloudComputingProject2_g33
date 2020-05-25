// JavaScript source code
function (doc) {
    emit([doc.location],doc.sentimental);
}

```
function (doc) {
    doc.created_at.forEach(function (item){
      var year=item.split(' ')[-1];
      emit([doc.location,year],doc.sentimental);
      
    })
  }
  function (doc) {
    doc.created_at.forEach(function (item){
      year=item.split(' ')[-1];
      emit([year],1);
    })
  }
  ```
