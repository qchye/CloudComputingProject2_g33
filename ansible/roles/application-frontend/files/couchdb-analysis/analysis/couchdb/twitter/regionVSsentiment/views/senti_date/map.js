function (doc) {
    emit([doc.location,doc.created_at],doc.sentimental);
}