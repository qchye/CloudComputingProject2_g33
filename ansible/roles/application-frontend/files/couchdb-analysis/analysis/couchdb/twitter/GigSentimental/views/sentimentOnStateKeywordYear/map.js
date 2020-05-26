function (doc) {
    emit([doc.location, doc.keyword, doc.created_at=doc.created_at.split(" ")[doc.created_at.split(" ").length - 1]], doc.sentimental);
  }