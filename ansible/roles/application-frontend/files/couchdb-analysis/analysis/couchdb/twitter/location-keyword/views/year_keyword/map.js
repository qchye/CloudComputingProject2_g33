function (doc) {
    var date = doc.created_at;
    var date_array = date.split(" ");
    var year = date_array[date_array.length - 1];
    emit([year, doc.keyword], 1);
  }